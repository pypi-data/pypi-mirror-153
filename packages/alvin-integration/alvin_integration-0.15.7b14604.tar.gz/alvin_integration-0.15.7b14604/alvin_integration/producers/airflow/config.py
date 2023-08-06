import os

from alvin_integration.interfaces.config import AbstractProducerConfig
from alvin_integration.models import (
    AlvinLineageConfig,
    AlvinPatch,
    AlvinPipelineCreator,
)
from alvin_integration.producers.airflow.patch.functions import (
    _add_auth,
    _run_finished_callback,
    get_client,
    get_hook,
    get_or_create_openlineage_client,
    handle_callback,
    handle_failure,
    pre_execute,
    run,
    update_state,
)
from alvin_integration.producers.airflow.patch.functions_214 import (
    update_state as update_state_214,
)
from alvin_integration.producers.airflow.patch.functions_legacy import (
    update_state as update_state_legacy,
)
from alvin_integration.producers.airflow.pipeline import (
    create_alvin_dag_current,
    create_alvin_dag_google_composer,
    create_alvin_dag_legacy,
)

ALVIN_BACKEND_API_URL = os.getenv("ALVIN_URL")

ALVIN_BACKEND_API_KEY = os.getenv("ALVIN_API_KEY")

GOOGLE_COMPOSER_BUCKET = os.getenv("GCS_BUCKET")


class AirflowProducerConfig(AbstractProducerConfig):
    @property
    def producer_name(self):
        return "Airflow"

    def get_patching_list(self):
        return [
            AlvinPatch(
                package_name="apache-airflow",
                function=_run_finished_callback,
                supported_versions=[
                    "2.2.3",
                    "2.2.3+composer",
                    "2.1.4",
                    "2.2.5",
                    "2.1.4+composer",
                ],
                destination_path="airflow.models.taskinstance.TaskInstance",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=handle_failure,
                supported_versions=["1.10.15"],
                destination_path="airflow.models.taskinstance.TaskInstance",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=handle_callback,
                supported_versions=[
                    "1.10.15",
                    "2.2.3+composer",
                    "2.2.3",
                    "2.1.4",
                    "2.2.5",
                    "2.1.4+composer",
                ],
                destination_path="airflow.models.dag.DAG",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=pre_execute,
                supported_versions=["1.10.15", "1.10.15+composer"],
                destination_path="airflow.contrib.operators.bigquery_operator.BigQueryOperator",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=get_client,
                supported_versions=["1.10.15", "1.10.15+composer"],
                destination_path="airflow.contrib.hooks.bigquery_hook.BigQueryHook",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=run,
                supported_versions=["1.10.15", "1.10.15+composer"],
                destination_path="airflow.contrib.hooks.snowflake_hook.SnowflakeHook",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=get_hook,
                supported_versions=["1.10.15", "1.10.15+composer"],
                destination_path="airflow.contrib.operators.snowflake_operator.SnowflakeOperator",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=_add_auth,
                supported_versions=[
                    "1.10.15",
                    "1.10.15+composer",
                    "2.2.3",
                    "2.2.3+composer",
                    "2.1.4",
                    "2.2.5",
                    "2.1.4+composer",
                ],
                destination_path="openlineage.client.OpenLineageClient",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=get_or_create_openlineage_client,
                supported_versions=[
                    "1.10.15",
                    "1.10.15+composer",
                    "2.2.3",
                    "2.2.3+composer",
                    "2.1.4",
                    "2.2.5",
                    "2.1.4+composer",
                ],
                destination_path="openlineage.airflow.adapter.OpenLineageAdapter",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=update_state,
                supported_versions=["2.2.3", "2.2.5", "2.2.3+composer"],
                destination_path="airflow.models.dagrun.DagRun",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=update_state_214,
                supported_versions=["2.1.4", "2.1.4+composer"],
                destination_path="airflow.models.dagrun.DagRun",
            ),
            AlvinPatch(
                package_name="apache-airflow",
                function=update_state_legacy,
                supported_versions=[
                    "1.10.15",
                    "1.10.15+composer",
                    "2.1.4",
                    "2.1.4+composer",
                ],
                destination_path="airflow.models.dagrun.DagRun",
            ),
        ]

    def get_target_packages(self):
        return ["apache-airflow"]

    def get_target_pipelines(self):
        return [
            AlvinPipelineCreator(
                package_name="apache-airflow",
                function=create_alvin_dag_current,
                supported_versions=["2.2.3", "2.1.4", "2.2.5"],
            ),
            AlvinPipelineCreator(
                package_name="apache-airflow",
                function=create_alvin_dag_google_composer,
                supported_versions=["2.2.3+composer", "2.1.4+composer"],
            ),
            AlvinPipelineCreator(
                package_name="apache-airflow",
                function=create_alvin_dag_legacy,
                supported_versions=["1.10.15"],
            ),
        ]

    def get_lineage_config(self):
        return [
            AlvinLineageConfig(
                package_name="apache-airflow",
                env_name="OPENLINEAGE_EXTRACTOR_BigQueryExecuteQueryOperator",
                env_value="alvin_integration.producers.airflow.lineage.extractors.bigquery.AlvinBigQueryExtractor",
                supported_versions=[
                    "2.2.3",
                    "2.2.3+composer",
                    "2.1.4",
                    "2.2.5",
                    "2.1.4+composer",
                ],
            ),
            AlvinLineageConfig(
                package_name="apache-airflow",
                env_name="OPENLINEAGE_EXTRACTOR_BigQueryInsertJobOperator",
                env_value="alvin_integration.producers.airflow.lineage.extractors.bigquery.AlvinBigQueryExtractor",
                supported_versions=[
                    "2.2.3",
                    "2.2.3+composer",
                    "2.1.4",
                    "2.2.5",
                    "2.1.4+composer",
                ],
            ),
            # We have some customers that still use the BigQueryOperator on Airflow V2
            # also what is interesting is that the AlvinBigQueryExtractor in Airflow V2 uses similar
            # attributes as the BigQueryInsertJobOperator, like gcp_conn_id instead of bigquery_conn_id
            # so we have to use the AlvinBigQueryExtractor instead of the AlvinBigQueryLegacyExtractor one.
            AlvinLineageConfig(
                package_name="apache-airflow",
                env_name="OPENLINEAGE_EXTRACTOR_BigQueryOperator",
                env_value="alvin_integration.producers.airflow.lineage.extractors.bigquery.AlvinBigQueryExtractor",
                supported_versions=[
                    "2.2.3",
                    "2.2.3+composer",
                    "2.1.4",
                    "2.2.5",
                    "2.1.4+composer",
                ],
            ),
            AlvinLineageConfig(
                package_name="apache-airflow",
                env_name="OPENLINEAGE_EXTRACTOR_BigQueryOperator",
                env_value="alvin_integration.producers.airflow.lineage.extractors.bigquery.AlvinBigQueryLegacyExtractor",
                supported_versions=["1.10.15", "1.10.15+composer"],
            ),
            AlvinLineageConfig(
                package_name="apache-airflow",
                env_name="OPENLINEAGE_EXTRACTOR_SnowflakeOperator",
                env_value="alvin_integration.producers.airflow.lineage.extractors.snowflake.AlvinSnowflakeLegacyExtractor",
                supported_versions=["1.10.15", "1.10.15+composer"],
            ),
            AlvinLineageConfig(
                package_name="apache-airflow",
                env_name="OPENLINEAGE_EXTRACTOR_SnowflakeOperator",
                env_value="alvin_integration.producers.airflow.lineage.extractors.snowflake.AlvinSnowflakeExtractor",
                supported_versions=[
                    "2.2.3",
                    "2.2.3+composer",
                    "2.1.4",
                    "2.2.5",
                    "2.1.4+composer",
                ],
            ),
        ]
