import time
from datetime import timedelta
from typing import Any, List, NoReturn, Optional, Union  # noqa: F401

from airflow.models import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin  # type: ignore

log = LoggingMixin().log
SNOWFLAKE_CONN_ID = "snowflake_db"

args = {
    "owner": "airflow",
    "start_date": days_ago(10),
    "snowflake_conn_id": SNOWFLAKE_CONN_ID,
}

dag = DAG(
    dag_id="snowflake_demo",
    default_args=args,
    schedule_interval="0 0 1 * *",
    dagrun_timeout=timedelta(minutes=60),
)


task1 = SnowflakeOperator(
    task_id="task1",
    dag=dag,
    sql='SELECT SYMBOL FROM "FINSERVAM"."PROD"."FRAUDULENT_TRADE" limit 1',
    warehouse="COMPUTE_WH",
    database="FINSERVAM",
    schema="PROD",
    role="ACCOUNTADMIN",
)

task2 = SnowflakeOperator(
    task_id="task2",
    dag=dag,
    sql='create or replace table fraudulent_trade_airflow as (select date, symbol, exchange, action, close, trader, pm, 0 as fraud from "FINSERVAM"."PROD"."TRADE")',
    warehouse="COMPUTE_WH",
    database="FINSERVAM",
    schema="PROD",
    role="ACCOUNTADMIN",
)


task1 >> task2
