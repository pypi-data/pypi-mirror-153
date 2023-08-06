import logging
from datetime import timedelta
from typing import Any  # noqa: F401

from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago

logging.warning("Inside the DAG")

args = {"owner": "airflow", "start_date": days_ago(10)}

dag = DAG(
    dag_id="snowflake_dag",
    default_args=args,
    schedule_interval="0 0 1 * *",
    dagrun_timeout=timedelta(minutes=60),
)


task_snowflake = SnowflakeOperator(
    dag=dag,
    task_id="task_snowflake",
    sql="SELECT 1;",
    snowflake_conn_id="snowflake_db",
)
