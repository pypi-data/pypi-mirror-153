from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils import db

from alvin_integration.producers.airflow.pipeline.extractor import extract_dag_metadata

seven_days_ago = datetime.combine(
    datetime.today() - timedelta(1), datetime.min.time()
)  # noqa

args = {
    "owner": "airflow",
    "start_date": seven_days_ago,
}


@db.provide_session
def extract_metadata(session, **kwargs):
    """Extract metadata from DAG and send to Alvin Backend API."""
    extract_dag_metadata(session)


alvin_metadata_extractor = DAG(
    dag_id="alvin_metadata_extractor",
    default_args=args,
    schedule_interval="@hourly",
    catchup=False,
)  # noqa

task_success_one = PythonOperator(
    task_id="dag_metadata_extractor",
    provide_context=True,
    python_callable=extract_metadata,
    dag=alvin_metadata_extractor,
)
