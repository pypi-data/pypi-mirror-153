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
    dag_id="bigquery_musicbrainz_etl",
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


TASK1_BQ_SQL_QUERY = """
CREATE OR REPLACE TABLE `alvinai.musicbrainz.recordings_by_artists_manual`
AS SELECT artist.id, artist.gid as artist_gid,
       artist.name as artist_name, artist.area,
       recording.name as recording_name, recording.length,
       recording.gid as recording_gid, recording.video
  FROM `alvinai.musicbrainz.artist` as artist
      INNER JOIN `alvinai.musicbrainz.artist_credit_name` AS artist_credit_name
           ON artist.id = artist_credit_name.artist
      INNER JOIN `alvinai.musicbrainz.recording` AS recording
           ON artist_credit_name.artist_credit = recording.artist_credit
"""

task1 = BigQueryInsertJobOperator(
    dag=dag,
    task_id="01_refresh_artists",
    configuration={"query": {"query": TASK1_BQ_SQL_QUERY, "useLegacySql": False}},
    gcp_conn_id=ALVIN_GCP_CONN_ID,
    on_failure_callback=task_failure_func,
    on_success_callback=task_success_func,
    on_retry_callback=task_retry_func,
)

TASK2_BQ_SQL_QUERY = """
CREATE OR REPLACE TABLE `alvinai.musicbrainz.healthcheck_recordings_01`
AS SELECT artist_name, artist_gender, artist_area, recording_name, recording_length
FROM musicbrainz.recordings_by_artists_dataflow
WHERE artist_area is NOT NULL
LIMIT 1000;
"""


task2 = BigQueryInsertJobOperator(
    dag=dag,
    task_id="02_healthcheck_recordings_by_artists_dataflow",
    configuration={"query": {"query": TASK2_BQ_SQL_QUERY, "useLegacySql": False}},
    gcp_conn_id=ALVIN_GCP_CONN_ID,
    on_failure_callback=task_failure_func,
    on_success_callback=task_success_func,
    on_retry_callback=task_retry_func,
)

TASK3_BQ_SQL_QUERY = """
CREATE OR REPLACE TABLE `alvinai.musicbrainz.healthcheck_recordings_02`
AS SELECT artist_name, artist_gender, artist_area, recording_name, recording_length
FROM musicbrainz.recordings_by_artists_dataflow
WHERE artist_gender IS NOT NULL
LIMIT 5000;
"""

task3 = BigQueryInsertJobOperator(
    dag=dag,
    task_id="03_healthcheck_recordings_by_artists_dataflow_nested",
    configuration={"query": {"query": TASK3_BQ_SQL_QUERY, "useLegacySql": False}},
    gcp_conn_id=ALVIN_GCP_CONN_ID,
    on_failure_callback=task_failure_func,
    on_success_callback=task_success_func,
    on_retry_callback=task_retry_func,
)

TASK4_BQ_SQL_QUERY = """
CREATE OR REPLACE TABLE `alvinai.musicbrainz.recordings_by_artists_curated` 
AS SELECT artist_name, artist_gender, artist_area, recording_name, recording_length 
FROM musicbrainz.recordings_by_artists_dataflow 
WHERE artist_area is NOT NULL 
AND artist_gender IS NOT NULL 
AND recording_length > 10000 
"""

task4 = BigQueryInsertJobOperator(
    dag=dag,
    task_id="04_refresh_artists_curated",
    configuration={"query": {"query": TASK4_BQ_SQL_QUERY, "useLegacySql": False}},
    gcp_conn_id=ALVIN_GCP_CONN_ID,
    on_failure_callback=task_failure_func,
    on_success_callback=task_success_func,
    on_retry_callback=task_retry_func,
)

TASK5_BQ_SQL_QUERY = """
CREATE OR REPLACE TABLE `musicbrainz.recordings_by_artists_with_area`
AS SELECT artist_name,
       artist_gender,
       artist_area,
       ARRAY(SELECT artist_credit_name_name
               FROM UNNEST(recordings_by_artists_dataflow_nested.artist_recordings)) AS artist_credit_name_name,
       ARRAY(SELECT recording_name
               FROM UNNEST(recordings_by_artists_dataflow_nested.artist_recordings)) AS recording_name
 FROM musicbrainz.recordings_by_artists_dataflow_nested,
      UNNEST(recordings_by_artists_dataflow_nested.artist_recordings) AS artist_recordings_struct
WHERE artist_area IS NOT NULL
LIMIT 1000;
"""

task5 = BigQueryInsertJobOperator(
    dag=dag,
    task_id="05_refresh_a_area",
    configuration={"query": {"query": TASK5_BQ_SQL_QUERY, "useLegacySql": False}},
    gcp_conn_id=ALVIN_GCP_CONN_ID,
    on_failure_callback=task_failure_func,
    on_success_callback=task_success_func,
    on_retry_callback=task_retry_func,
)


TASK6_BQ_SQL_QUERY = """
CREATE OR REPLACE TABLE `musicbrainz.recordings_by_artists_with_area_curated`
AS SELECT * FROM musicbrainz.recordings_by_artists_with_area rbawa
WHERE EXISTS (select 1 from alvinai.musicbrainz.recordings_by_artists_curated rbac where rbawa.artist_name = rbac.artist_name );
"""

task6 = BigQueryInsertJobOperator(
    dag=dag,
    task_id="06_refresh_a_curated",
    configuration={"query": {"query": TASK6_BQ_SQL_QUERY, "useLegacySql": False}},
    gcp_conn_id=ALVIN_GCP_CONN_ID,
    on_failure_callback=task_failure_func,
    on_success_callback=task_success_func,
    on_retry_callback=task_retry_func,
)

TASK7_BQ_SQL_QUERY = """
SELECT * FROM `musicbrainz.recordings_by_artists_with_area_curated` limit 10
"""

task7 = BigQueryExecuteQueryOperator(
    dag=dag, task_id="07_get_artists", use_legacy_sql=False, sql=TASK7_BQ_SQL_QUERY
)

task1 >> task2
task1 >> task3
task2 >> task4
task2 >> task5
task3 >> task5
task5 >> task6
task4 >> task6
task4 >> task7
