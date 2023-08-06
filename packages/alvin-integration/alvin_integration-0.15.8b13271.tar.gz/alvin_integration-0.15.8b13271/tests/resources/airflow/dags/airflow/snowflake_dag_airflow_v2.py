import datetime
import logging
from datetime import timedelta

from airflow.models import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

logging.warning("Inside the DAG")

dag = DAG(
    "snowflake_dag_airflow_v2",
    start_date=datetime.datetime.utcnow(),
    default_args={"snowflake_conn_id": "snowflake_db"},
    schedule_interval="0 0 1 * *",
    tags=["example"],
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
)

task_sf_af_v2 = SnowflakeOperator(
    task_id="task_sf_af_v2",
    dag=dag,
    sql="SELECT 1;",
)

task_sf_af_v2
