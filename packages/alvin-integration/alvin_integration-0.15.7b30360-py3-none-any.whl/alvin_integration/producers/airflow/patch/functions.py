import airflow


def _run_finished_callback(self, error=None):
    """
    Alvin patched version of _run_finished_callback from TaskInstance.

    This method will inject the call
    to alvin_callback in case the task has failed.
    """
    from alvin_integration.producers.airflow.lineage.backend import alvin_callback

    context = self.get_template_context()

    alvin_callback(context=context, operator=self.task)


def handle_failure(
    self,
    error,
    test_mode=None,
    context=None,
    force_fail=False,
    session=None,  # noqa
):
    """
    Alvin patched version of handle_failure from TaskInstance.

    This method will inject the call
    to alvin_callback in case the task has failed.
    """
    import logging

    from alvin_integration.helper import AlvinLoggerAdapter
    from alvin_integration.producers.airflow.lineage.backend import alvin_callback

    log = AlvinLoggerAdapter(logging.getLogger(__name__), {})

    @airflow.utils.db.provide_session
    def get_session(session):
        return session

    if not session:
        session = get_session()
    from airflow.models.log import Log
    from airflow.models.taskfail import TaskFail
    from airflow.settings import Stats
    from airflow.utils import timezone
    from airflow.utils.state import State

    if test_mode is None:
        test_mode = self.test_mode
    if context is None:
        context = self.get_template_context()

    log.exception(error)
    task = self.task
    self.end_date = timezone.utcnow()
    self.set_duration()
    Stats.incr("operator_failures_{}".format(task.__class__.__name__), 1, 1)
    Stats.incr("ti_failures")
    if not test_mode:
        session.add(Log(State.FAILED, self))

    # Log failure duration
    session.add(TaskFail(task, self.execution_date, self.start_date, self.end_date))

    if context is not None:
        context["exception"] = error

    # Set state correctly and figure out how to log it,
    # what callback to call if any, and how to decide whether to email

    # Since this function is called only when the TaskInstance state is running,
    # try_number contains the current try_number (not the next). We
    # only mark task instance as FAILED if the next task instance
    # try_number exceeds the max_tries ... or if force_fail is truthy

    if force_fail or not self.is_eligible_to_retry():
        self.state = State.FAILED
        if force_fail:
            log_message = "Immediate failure requested. Marking task as FAILED."
        else:
            log_message = "Marking task as FAILED."
        email_for_state = task.email_on_failure
        callback = task.on_failure_callback
    else:
        self.state = State.UP_FOR_RETRY
        log_message = "Marking task as UP_FOR_RETRY."
        email_for_state = task.email_on_retry
        callback = task.on_retry_callback

    log.info(
        "%s dag_id=%s, task_id=%s, execution_date=%s, start_date=%s, end_date=%s",
        log_message,
        self.dag_id,
        self.task_id,
        self._safe_date("execution_date", "%Y%m%dT%H%M%S"),
        self._safe_date("start_date", "%Y%m%dT%H%M%S"),
        self._safe_date("end_date", "%Y%m%dT%H%M%S"),
    )
    if email_for_state and task.email:
        try:
            self.email_alert(error)
        except Exception as e2:
            log.error("Failed to send email to: %s", task.email)
            log.exception(e2)

    # Handling callbacks pessimistically
    if callback:
        try:
            callback(context)
        except Exception as e3:
            log.error("Failed at executing callback")
            log.exception(e3)

    if not test_mode:
        session.merge(self)
    session.commit()

    alvin_callback(context=context, operator=self.task, is_airflow_legacy=True)  # noqa


def handle_callback(self, dagrun, success=True, reason=None, session=None):
    """
    Alvin patched version of handle_callback from DAG.

    This method will inject the call
    to alvin_callback in case the task has failed.
    """
    import logging

    from alvin_integration.helper import AlvinLoggerAdapter
    from alvin_integration.producers.airflow.lineage.backend import alvin_callback

    log = AlvinLoggerAdapter(logging.getLogger(__name__), {})

    task_instance_list = dagrun.get_task_instances()

    if not success:
        is_airlfow_legacy = True

        for ti in task_instance_list:
            ti.task = self.get_task(ti.task_id)
            context = ti.get_template_context(session=session)
            alvin_callback(
                context=context,
                operator=ti.task,
                is_airflow_legacy=is_airlfow_legacy,  # noqa
            )

    callback = self.on_success_callback if success else self.on_failure_callback  # noqa

    if callback:
        log.info("Executing dag callback function: {}".format(callback))
        task_instance_list = dagrun.get_task_instances()
        ti = task_instance_list[-1]  # get first TaskInstance of DagRun
        ti.task = self.get_task(ti.task_id)
        context = ti.get_template_context(session=session)
        context.update({"reason": reason})
        callback(context)


def pre_execute(self, context):
    """
    Alvin patched version of pre_execute from BigQueryOperator.

    This method will create the hook in the operator object
    and instantiate the bq_cursor.
    """
    from airflow.contrib.hooks.bigquery_hook import BigQueryHook

    @airflow.lineage.prepare_lineage
    def prepare_lineage(session):
        pass

    prepare_lineage()
    self.hook = BigQueryHook(
        bigquery_conn_id=self.bigquery_conn_id,
        use_legacy_sql=self.use_legacy_sql,
        delegate_to=self.delegate_to,
        location=self.location,
    )
    conn = self.hook.get_conn()
    self.bq_cursor = conn.cursor()


def get_client(self, project_id=None, location=None):
    """
    Alvin patched to add the method get_client to the BigQueryOperator.

    This method will create crate a Google Client using the
    reusing the Airflow Google connection.
    """
    from google.cloud.bigquery import Client

    return Client(
        project=project_id,
        location=location,
        credentials=self._get_credentials(),
    )


def run(self, sql, autocommit=False, parameters=None):
    """
    Runs a command or a list of commands. Pass a list of sql
    statements to the sql parameter to get them to execute
    sequentially
    :param sql: the sql statement to be executed (str) or a list of
        sql statements to execute
    :type sql: str or list
    :param autocommit: What to set the connection's autocommit setting to
        before executing the query.
    :type autocommit: bool
    :param parameters: The parameters to render the SQL query with.
    :type parameters: mapping or iterable
    """
    import logging
    import sys
    from contextlib import closing

    from past.builtins import basestring

    from alvin_integration.helper import AlvinLoggerAdapter

    log = AlvinLoggerAdapter(logging.getLogger(__name__), {})

    self.query_ids = []

    if isinstance(sql, basestring):
        sql = [sql]

    with closing(self.get_conn()) as conn:
        if self.supports_autocommit:
            self.set_autocommit(conn, autocommit)

        with closing(conn.cursor()) as cur:
            for s in sql:
                if sys.version_info[0] < 3:
                    s = s.encode("utf-8")
                if parameters is not None:
                    log.info("{} with parameters {}".format(s, parameters))
                    cur.execute(s, parameters)
                else:
                    log.info(s)
                    cur.execute(s)
                query_id = cur.sfqid
                log.info("Rows affected: %s", cur.rowcount)
                log.info("Snowflake query id: %s", query_id)
                self.query_ids.append(query_id)

        # If autocommit was set to False for db that supports autocommit,
        # or if db does not supports autocommit, we do a manual commit.
        if not self.get_autocommit(conn):
            conn.commit()


def get_hook(self):
    from airflow.contrib.hooks.snowflake_hook import SnowflakeHook

    if not hasattr(self, "hook"):
        self.hook = SnowflakeHook(
            snowflake_conn_id=self.snowflake_conn_id,
            warehouse=self.warehouse,
            database=self.database,
            role=self.role,
            schema=self.schema,
            authenticator=self.authenticator,
        )
    return self.hook


def _add_auth(self, api_key: str):
    if "alvin" in api_key:
        alvin_api_key = api_key.split("-alvin-")
        self.session.headers.update({"X-API-KEY": f"{alvin_api_key[1]}"})
    else:
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})


def get_or_create_openlineage_client(self):
    import logging
    import os

    from openlineage.client import OpenLineageClient, OpenLineageClientOptions

    from alvin_integration.helper import AlvinLoggerAdapter

    log = AlvinLoggerAdapter(logging.getLogger(__name__), {})

    if not self._client:
        alvin_url = os.getenv("ALVIN_URL")
        alvin_api_key = os.getenv("ALVIN_API_KEY")
        if alvin_url:
            log.info(f"Sending lineage events to Alvin Backend: {alvin_url}")
            self._client = OpenLineageClient(
                alvin_url,
                OpenLineageClientOptions(api_key=f"key-alvin-{alvin_api_key}"),
            )
            return self._client
        # Backcomp with Marquez integration
        marquez_url = os.getenv("MARQUEZ_URL")
        marquez_api_key = os.getenv("MARQUEZ_API_KEY")

        if marquez_url:
            log.info(f"Sending lineage events to {marquez_url}")
            self._client = OpenLineageClient(
                marquez_url, OpenLineageClientOptions(api_key=marquez_api_key)
            )
        else:
            self._client = OpenLineageClient.from_environment()
    return self._client


def update_state(self, session=None, execute_callbacks=True):
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
    import logging
    from typing import Optional

    from airflow.stats import Stats
    from airflow.utils import callback_requests, timezone
    from airflow.utils.state import DagRunState, State, TaskInstanceState

    from alvin_integration.helper import AlvinLoggerAdapter
    from alvin_integration.producers.airflow.lineage.backend import (
        alvin_dag_run_extractor,
    )

    log = AlvinLoggerAdapter(logging.getLogger(__name__), {})

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
            t.task.max_active_tis_per_dag is None for t in unfinished_tasks
        )
        none_deferred = all(t.state != State.DEFERRED for t in unfinished_tasks)

        if (
            unfinished_tasks
            and none_depends_on_past
            and none_task_concurrency
            and none_deferred
        ):
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
        log.error("Marking run %s failed", self)
        self.set_state(State.FAILED)
        if execute_callbacks:
            dag.handle_callback(
                self, success=False, reason="task_failure", session=session
            )
        elif dag.has_on_failure_callback:
            callback = callback_requests.DagCallbackRequest(
                full_filepath=dag.fileloc,
                dag_id=self.dag_id,
                run_id=self.run_id,
                is_failure_callback=True,
                msg="task_failure",
            )

    # if all leaves succeeded and no unfinished tasks, the run succeeded
    elif not unfinished_tasks and all(
        leaf_ti.state in State.success_states for leaf_ti in leaf_tis
    ):
        log.info("Marking run %s successful", self)
        self.set_state(State.SUCCESS)
        if execute_callbacks:
            dag.handle_callback(self, success=True, reason="success", session=session)
        elif dag.has_on_success_callback:
            callback = callback_requests.DagCallbackRequest(
                full_filepath=dag.fileloc,
                dag_id=self.dag_id,
                run_id=self.run_id,
                is_failure_callback=False,
                msg="success",
            )

    # if *all tasks* are deadlocked, the run failed
    elif (
        unfinished_tasks
        and none_depends_on_past
        and none_task_concurrency
        and none_deferred
        and not are_runnable_tasks
    ):
        log.error("Deadlock; marking run %s failed", self)
        self.set_state(State.FAILED)
        if execute_callbacks:
            dag.handle_callback(
                self, success=False, reason="all_tasks_deadlocked", session=session
            )
        elif dag.has_on_failure_callback:
            callback = callback_requests.DagCallbackRequest(
                full_filepath=dag.fileloc,
                dag_id=self.dag_id,
                run_id=self.run_id,
                is_failure_callback=True,
                msg="all_tasks_deadlocked",
            )

    # finally, if the roots aren't done, the dag is still running
    else:
        self.set_state(State.RUNNING)

    if self._state == State.FAILED or self._state == State.SUCCESS:
        msg = (
            "Alvin DagRun Finished: dag_id=%s, execution_date=%s, run_id=%s, "
            "run_start_date=%s, run_end_date=%s, run_duration=%s, "
            "state=%s, external_trigger=%s, run_type=%s, "
            "data_interval_start=%s, data_interval_end=%s, dag_hash=%s"
        )
        log.info(
            msg,
            self.dag_id,
            self.execution_date,
            self.run_id,
            self.start_date,
            self.end_date,
            (self.end_date - self.start_date).total_seconds()
            if self.start_date and self.end_date
            else None,
            self._state,
            self.external_trigger,
            self.run_type,
            self.data_interval_start,
            self.data_interval_end,
            self.dag_hash,
        )

    alvin_dag_run_extractor(dag_run=self)
    self._emit_true_scheduling_delay_stats_for_finished_state(finished_tasks)
    self._emit_duration_stats_for_finished_state()

    session.merge(self)

    return schedulable_tis, callback
