import logging
from datetime import timedelta
from typing import Any  # noqa: F401

from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago

logging.warning("Inside the DAG")

args = {"owner": "airflow", "start_date": days_ago(10)}

dag = DAG(
    dag_id="bq_mvp",
    default_args=args,
    schedule_interval="0 0 1 * *",
    dagrun_timeout=timedelta(minutes=60),
)

# On GCP Compose "bigquery_default" works, so we call it like this
# instead of "test_fernet"
ALVIN_GCP_CONN_ID = "bigquery_default"


BQ_SQL_QUERY = "SELECT * FROM alvin_test_dataset_eu.WineQualityEU"


taskBQ = BigQueryOperator(
    dag=dag,
    task_id="taskBQ",
    sql=BQ_SQL_QUERY,
    bigquery_conn_id=ALVIN_GCP_CONN_ID,
)
