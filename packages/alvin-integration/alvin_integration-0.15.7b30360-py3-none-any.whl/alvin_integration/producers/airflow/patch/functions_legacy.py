import airflow


def update_state(self, session=None):
    """
    Determines the overall state of the DagRun based on the state
    of its TaskInstances.
    :return: ready_tis: the tis that can be scheduled in the current loop
    :rtype ready_tis: list[airflow.models.TaskInstance]
    """
    import logging

    from airflow.settings import Stats
    from airflow.ti_deps.dep_context import SCHEDULEABLE_STATES
    from airflow.utils import timezone
    from airflow.utils.state import State

    from alvin_integration.helper import AlvinLoggerAdapter
    from alvin_integration.producers.airflow.lineage.backend import (
        alvin_dag_run_extractor,
    )

    log = AlvinLoggerAdapter(logging.getLogger(__name__), {})

    @airflow.utils.db.provide_session
    def get_session(session):
        return session

    if not session:
        session = get_session()

    dag = self.get_dag()
    ready_tis = []
    tis = [
        ti
        for ti in self.get_task_instances(
            session=session, state=State.task_states + (State.SHUTDOWN,)
        )
    ]
    log.debug("number of tis tasks for %s: %s task(s)", self, len(tis))
    for ti in list(tis):
        ti.task = dag.get_task(ti.task_id)

    start_dttm = timezone.utcnow()
    unfinished_tasks = [t for t in tis if t.state in State.unfinished()]
    finished_tasks = [
        t for t in tis if t.state in State.finished() + [State.UPSTREAM_FAILED]
    ]
    none_depends_on_past = all(not t.task.depends_on_past for t in unfinished_tasks)
    none_task_concurrency = all(
        t.task.task_concurrency is None for t in unfinished_tasks
    )
    # small speed up
    if unfinished_tasks:
        scheduleable_tasks = [
            ut for ut in unfinished_tasks if ut.state in SCHEDULEABLE_STATES
        ]
        log.debug(
            "number of scheduleable tasks for %s: %s task(s)",
            self,
            len(scheduleable_tasks),
        )
        ready_tis, changed_tis = self._get_ready_tis(
            scheduleable_tasks, finished_tasks, session
        )
        log.debug("ready tis length for %s: %s task(s)", self, len(ready_tis))
        if none_depends_on_past and none_task_concurrency:
            # small speed up
            are_runnable_tasks = (
                ready_tis
                or self._are_premature_tis(unfinished_tasks, finished_tasks, session)
                or changed_tis
            )

    duration = timezone.utcnow() - start_dttm
    Stats.timing("dagrun.dependency-check.{}".format(self.dag_id), duration)

    leaf_task_ids = {t.task_id for t in dag.leaves}
    leaf_tis = [ti for ti in tis if ti.task_id in leaf_task_ids]

    # if all roots finished and at least one failed, the run failed
    if not unfinished_tasks and any(
        leaf_ti.state in {State.FAILED, State.UPSTREAM_FAILED} for leaf_ti in leaf_tis
    ):
        log.info("Marking run %s failed", self)
        self.set_state(State.FAILED)
        dag.handle_callback(self, success=False, reason="task_failure", session=session)

    # if all leafs succeeded and no unfinished tasks, the run succeeded
    elif not unfinished_tasks and all(
        leaf_ti.state in {State.SUCCESS, State.SKIPPED} for leaf_ti in leaf_tis
    ):
        log.info("Marking run %s successful", self)
        self.set_state(State.SUCCESS)
        dag.handle_callback(self, success=True, reason="success", session=session)

    # if *all tasks* are deadlocked, the run failed
    elif (
        unfinished_tasks
        and none_depends_on_past
        and none_task_concurrency
        and not are_runnable_tasks
    ):
        log.info("Deadlock; marking run %s failed", self)
        self.set_state(State.FAILED)
        dag.handle_callback(
            self, success=False, reason="all_tasks_deadlocked", session=session
        )

    # finally, if the roots aren't done, the dag is still running
    else:
        self.set_state(State.RUNNING)

    self._emit_true_scheduling_delay_stats_for_finished_state(finished_tasks)
    self._emit_duration_stats_for_finished_state()
    alvin_dag_run_extractor(dag_run=self)
    # todo: determine we want to use with_for_update to make sure to lock the run
    session.merge(self)
    session.commit()

    return ready_tis
