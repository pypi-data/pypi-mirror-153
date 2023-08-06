import airflow


def update_state(self, session=None, execute_callbacks: bool = True):
    """
    Determines the overall state of the DagRun based on the state
    of its TaskInstances.
    :param session: Sqlalchemy ORM Session
    :type session: Session
    :param execute_callbacks: Should dag callbacks (success/failure, SLA etc) be invoked
        directly (default: true) or recorded as a pending request in the ``callback`` property
    :type execute_callbacks: bool
    :return: Tuple containing tis that can be scheduled in the current loop & `callback` that
        needs to be executed
    """
    from typing import Optional

    from airflow.stats import Stats
    from airflow.utils import callback_requests, timezone
    from airflow.utils.state import State

    from alvin_integration.producers.airflow.lineage.backend import (
        alvin_dag_run_extractor,
    )

    # Callback to execute in case of Task Failures
    callback: Optional[callback_requests.DagCallbackRequest] = None

    @airflow.utils.session.provide_session
    def get_session(session):
        return session

    if not session:
        session = get_session()

    start_dttm = timezone.utcnow()
    self.last_scheduling_decision = start_dttm
    with Stats.timer(f"dagrun.dependency-check.{self.dag_id}"):
        dag = self.get_dag()
        info = self.task_instance_scheduling_decisions(session)

        tis = info.tis
        schedulable_tis = info.schedulable_tis
        changed_tis = info.changed_tis
        finished_tasks = info.finished_tasks
        unfinished_tasks = info.unfinished_tasks

        none_depends_on_past = all(not t.task.depends_on_past for t in unfinished_tasks)
        none_task_concurrency = all(
            t.task.task_concurrency is None for t in unfinished_tasks
        )

        if unfinished_tasks and none_depends_on_past and none_task_concurrency:
            # small speed up
            are_runnable_tasks = (
                schedulable_tis
                or self._are_premature_tis(unfinished_tasks, finished_tasks, session)
                or changed_tis
            )

    leaf_task_ids = {t.task_id for t in dag.leaves}
    leaf_tis = [ti for ti in tis if ti.task_id in leaf_task_ids]

    # if all roots finished and at least one failed, the run failed
    if not unfinished_tasks and any(
        leaf_ti.state in State.failed_states for leaf_ti in leaf_tis
    ):
        self.log.error("Marking run %s failed", self)
        self.set_state(State.FAILED)
        if execute_callbacks:
            dag.handle_callback(
                self, success=False, reason="task_failure", session=session
            )
        elif dag.has_on_failure_callback:
            callback = callback_requests.DagCallbackRequest(
                full_filepath=dag.fileloc,
                dag_id=self.dag_id,
                execution_date=self.execution_date,
                is_failure_callback=True,
                msg="task_failure",
            )

    # if all leaves succeeded and no unfinished tasks, the run succeeded
    elif not unfinished_tasks and all(
        leaf_ti.state in State.success_states for leaf_ti in leaf_tis
    ):
        self.log.info("Marking run %s successful", self)
        self.set_state(State.SUCCESS)
        if execute_callbacks:
            dag.handle_callback(self, success=True, reason="success", session=session)
        elif dag.has_on_success_callback:
            callback = callback_requests.DagCallbackRequest(
                full_filepath=dag.fileloc,
                dag_id=self.dag_id,
                execution_date=self.execution_date,
                is_failure_callback=False,
                msg="success",
            )

    # if *all tasks* are deadlocked, the run failed
    elif (
        unfinished_tasks
        and none_depends_on_past
        and none_task_concurrency
        and not are_runnable_tasks
    ):
        self.log.error("Deadlock; marking run %s failed", self)
        self.set_state(State.FAILED)
        if execute_callbacks:
            dag.handle_callback(
                self, success=False, reason="all_tasks_deadlocked", session=session
            )
        elif dag.has_on_failure_callback:
            callback = callback_requests.DagCallbackRequest(
                full_filepath=dag.fileloc,
                dag_id=self.dag_id,
                execution_date=self.execution_date,
                is_failure_callback=True,
                msg="all_tasks_deadlocked",
            )

    # finally, if the roots aren't done, the dag is still running
    else:
        self.set_state(State.RUNNING)
    alvin_dag_run_extractor(dag_run=self)
    self._emit_true_scheduling_delay_stats_for_finished_state(finished_tasks)
    self._emit_duration_stats_for_finished_state()

    session.merge(self)

    return schedulable_tis, callback
