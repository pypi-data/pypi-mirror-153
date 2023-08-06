import time
from datetime import timedelta
from typing import Any, List, NoReturn, Optional, Union  # noqa: F401

from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.models import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryExecuteQueryOperator,
    BigQueryInsertJobOperator,
)
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin  # type: ignore

log = LoggingMixin().log

args = {"owner": "airflow", "start_date": days_ago(10)}

dag = DAG(
    dag_id="bigq_demo",
    default_args=args,
    schedule_interval="0 0 1 * *",
    dagrun_timeout=timedelta(minutes=60),
)

task1 = BigQueryInsertJobOperator(
    dag=dag,
    task_id="task1",
    configuration={
        "query": {
            "query": "INSERT bigquery_demo.top_rising_term_max_min_airflow (region, term_name, score) SELECT region, term_name, cast(term_index as STRING), FROM bigquery_demo.top_rising_term_highest UNION ALL SELECT region, term_name, cast(term_index as STRING), FROM `alvinai.bigquery_demo.top_rising_term_lowest` limit 1",
            "useLegacySql": False,
        }
    },
)

task2 = BigQueryExecuteQueryOperator(
    dag=dag,
    task_id="task2",
    use_legacy_sql=False,
    sql="INSERT bigquery_demo.top_rising_term_region_airflow (region, term, term_index,term_gain) SELECT dma_name, term, cast(score as String), cast(percent_gain as String) FROM bigquery_demo.top_rising_term limit 1",
)

task3 = BigQueryOperator(
    dag=dag,
    task_id="task3",
    use_legacy_sql=False,
    sql="INSERT bigquery_demo.top_rising_term_max_min_airflow (region, term_name, score) SELECT region, term_name, cast(term_index as STRING), FROM bigquery_demo.top_rising_term_highest UNION ALL SELECT region, term_name, cast(term_index as STRING), FROM `alvinai.bigquery_demo.top_rising_term_lowest` limit 1",
)
task1 >> task2 >> task3
