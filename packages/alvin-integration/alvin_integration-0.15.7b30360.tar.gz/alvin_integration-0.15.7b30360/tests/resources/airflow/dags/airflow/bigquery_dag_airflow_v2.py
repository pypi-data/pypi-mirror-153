import logging
from datetime import timedelta
from typing import Any  # noqa: F401

from airflow.models import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryExecuteQueryOperator,
    BigQueryInsertJobOperator,
)
from airflow.utils.dates import days_ago

logging.warning("Inside the DAG")

args = {"owner": "airflow", "start_date": days_ago(10)}

dag = DAG(
    dag_id="bigquery_dag_airflow_v2",
    default_args=args,
    schedule_interval="0 0 1 * *",
    dagrun_timeout=timedelta(minutes=60),
)

# On GCP Compose "bigquery_default" works, so we call it like this
# instead of "test_fernet"
ALVIN_GCP_CONN_ID = "bigquery_default"


def task_failure_func(context):
    print(f"Alvin callback - {task_failure_func.__name__}: {context}")


def task_success_func(context):
    print(f"Alvin callback - {task_success_func.__name__}: {context}")


def task_retry_func(context):
    print(f"Alvin callback - {task_retry_func.__name__}: {context}")


BQ_SQL_QUERY = "SELECT * FROM alvin_test_dataset_eu.WineQualityEU"


task_bq_af_v2 = BigQueryExecuteQueryOperator(
    dag=dag,
    task_id="task_bq_af_v2",
    sql=BQ_SQL_QUERY,
    gcp_conn_id=ALVIN_GCP_CONN_ID,
    on_failure_callback=task_failure_func,
    on_success_callback=task_success_func,
    on_retry_callback=task_retry_func,
)


task_bq_af_v2_2 = BigQueryExecuteQueryOperator(
    dag=dag,
    task_id="task_bq_af_v2_2",
    sql=BQ_SQL_QUERY,
    gcp_conn_id=ALVIN_GCP_CONN_ID,
    on_failure_callback=task_failure_func,
    on_success_callback=task_success_func,
    on_retry_callback=task_retry_func,
)
task_bq_af_v2 >> task_bq_af_v2_2
