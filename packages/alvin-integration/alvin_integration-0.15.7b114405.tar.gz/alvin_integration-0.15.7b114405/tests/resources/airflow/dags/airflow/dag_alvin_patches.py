from datetime import datetime, timedelta

from airflow.exceptions import AirflowException
from airflow.models import DAG
from airflow.operators.python import PythonOperator

seven_days_ago = datetime.combine(
    datetime.today() - timedelta(7), datetime.min.time()
)  # noqa

args = {
    "owner": "airflow",
    "start_date": seven_days_ago,
}


def raise_exception():
    raise AirflowException("This task has failed.")


def print_log():
    print("Task executed successfully")


####################################################################################
# DAG with one task that should fail. Dag should fail.
####################################################################################
dag_simple_task_failure = DAG(
    dag_id="simgle_task_failure", default_args=args, schedule_interval=None
)  # noqa

fail_task = PythonOperator(
    task_id="raise_exception",
    provide_context=True,
    python_callable=raise_exception,
    dag=dag_simple_task_failure,
)

####################################################################################
# DAG with one task that should succeed. Dag should succeed
####################################################################################

dag_simple_task_success = DAG(
    dag_id="simgle_task_success", default_args=args, schedule_interval=None
)  # noqa

sucess_task = PythonOperator(
    task_id="print_log",
    provide_context=True,
    python_callable=print_log,
    dag=dag_simple_task_success,
)

####################################################################################
# DAG with two failed tasks that should fail. Dag should fail.
####################################################################################

dag_double_task_fail = DAG(
    dag_id="double_task_fail", default_args=args, schedule_interval=None
)  # noqa

fail_task_two = PythonOperator(
    task_id="raise_exception_two",
    provide_context=True,
    python_callable=raise_exception,
    dag=dag_double_task_fail,
)

fail_task_three = PythonOperator(
    task_id="raise_exception_three",
    provide_context=True,
    python_callable=raise_exception,
    dag=dag_double_task_fail,
)


####################################################################################
# DAG with one failed task and one succeed task. DAG should fail.
####################################################################################

dag_double_task_fail = DAG(
    dag_id="double_task_mix", default_args=args, schedule_interval=None
)  # noqa

mix_task_fail = PythonOperator(
    task_id="raise_exception_four",
    provide_context=True,
    python_callable=raise_exception,
    dag=dag_double_task_fail,
)

mix_task_success = PythonOperator(
    task_id="print_log_two",
    provide_context=True,
    python_callable=print_log,
    dag=dag_double_task_fail,
)


####################################################################################
# DAG with two succeed tasks. DAG should succeed.
####################################################################################

dag_double_task_succeed = DAG(
    dag_id="double_task_success", default_args=args, schedule_interval=None
)  # noqa

task_success_one = PythonOperator(
    task_id="print_log_four",
    provide_context=True,
    python_callable=print_log,
    dag=dag_double_task_succeed,
)

task_success_two = PythonOperator(
    task_id="print_log_five",
    provide_context=True,
    python_callable=print_log,
    dag=dag_double_task_succeed,
)
