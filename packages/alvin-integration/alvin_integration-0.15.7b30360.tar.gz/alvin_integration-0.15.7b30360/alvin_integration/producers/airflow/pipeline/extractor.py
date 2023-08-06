import os

import requests

from alvin_integration.producers.airflow.config import (
    ALVIN_BACKEND_API_KEY,
    ALVIN_BACKEND_API_URL,
)

ALVIN_PLATFORM_ID = os.getenv("ALVIN_PLATFORM_ID")


def get_airflow_version():
    import airflow

    return airflow.__version__


def get_dag_source_code(dag_location):
    if dag_location:
        with open(dag_location, "r") as f:
            content = f.read()
        return content


def extract_dag_metadata(session):
    from airflow.models.serialized_dag import SerializedDagModel
    from airflow.serialization.serialized_objects import SerializedDAG

    dag_metadata = SerializedDagModel.read_all_dags()

    alvin_backend_metadata_url = f"{ALVIN_BACKEND_API_URL}/api/v1/metadata"
    entities = []
    for dag_id, serialized_dag in dag_metadata.items():
        row = SerializedDagModel.get(dag_id, session)
        dag = row.dag
        dag_metadata = SerializedDAG.to_dict(dag)
        dag_metadata["dag"]["source_code"] = get_dag_source_code(
            dag_metadata["dag"].get("fileloc")
        )
        entities.append(dag_metadata["dag"])
    payload = {
        "alvin_platform_id": ALVIN_PLATFORM_ID,
        "facets": {
            "airflow_version": get_airflow_version(),
            "platform_type": "AIRFLOW",
        },
        "entities": entities,
    }
    requests.post(
        alvin_backend_metadata_url,
        json=payload,
        headers={"X-API-KEY": ALVIN_BACKEND_API_KEY},
    )
    print(f"Metadata extracted: {payload}")
