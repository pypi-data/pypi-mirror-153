import logging
from typing import List

from openlineage.airflow.extractors.base import TaskMetadata
from openlineage.airflow.extractors.bigquery_extractor import BigQueryExtractor
from openlineage.airflow.utils import get_job_name
from openlineage.client.facet import SqlJobFacet
from openlineage.common.provider.bigquery import (
    BigQueryDatasetsProvider,
    BigQueryErrorRunFacet,
    BigQueryFacets,
)

from alvin_integration.helper import AlvinLoggerAdapter
from alvin_integration.models import AlvinBigQueryLineageDetails, AlvinFacet
from alvin_integration.producers.airflow.lineage.extractors.mixins import (
    AlvinAirflowExtractorMixin,
)

log = AlvinLoggerAdapter(logging.getLogger(__name__), {})


class AlvinBigQueryBaseExtractor(AlvinAirflowExtractorMixin, BigQueryExtractor):
    """
    This class contains common logic to handle extraction of BigQuery lineage
    for both Airflow 1 and 2.

    https://cloud.google.com/bigquery/docs/information-schema-jobs
    """

    def __init__(self, operator, *args, **kwargs):
        super().__init__(operator, *args, **kwargs)

    @classmethod
    def get_operator_classnames(cls) -> List[str]:
        raise NotImplementedError

    def get_bigquery_job_id(self, task_instance):
        return self._get_xcom_bigquery_job_id(task_instance)

    def build_task_metadata(self, task_instance):
        if not self.operator.hook:
            return TaskMetadata(
                name=get_job_name(task=self.operator),
                inputs=[],
                outputs=[],
                run_facets={},
            )
        bigquery_job_id = self.get_bigquery_job_id(task_instance)
        context = self.parse_sql_context()
        big_query_client = self.operator.hook.get_client(
            project_id=self.operator.hook.project_id
        )

        stats = BigQueryDatasetsProvider(big_query_client).get_facets(bigquery_job_id)

        return TaskMetadata(
            name=get_job_name(task=self.operator),
            inputs=[ds.to_openlineage_dataset() for ds in stats.inputs],
            outputs=[stats.output.to_openlineage_dataset()] if stats.output else [],
            run_facets=stats.run_facets,
            job_facets={"sql": SqlJobFacet(context.sql)},
        )

    def build_facet(self, task_instance):
        bigquery_job_id = self.get_bigquery_job_id(task_instance)

        return AlvinFacet(
            alvin=AlvinBigQueryLineageDetails(
                job_id=bigquery_job_id,
                project_id=self.operator.hook.project_id
                if self.operator.hook
                else None,
                execution=self.get_execution_details(task_instance),
                connection_id=self.get_connection_id(),
            )
        )


class AlvinBigQueryExtractor(AlvinBigQueryBaseExtractor):
    """
    This class contains logic for Airflow 2.

    Note that on this version, the BigQuery operator class is
    part of this package: apache-airflow-providers-google.

    https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow#custom-extractors

    The following env var needs to be set in the airflow host environment:
    OPENLINEAGE_EXTRACTOR_BigQueryExecuteQueryOperator
        =alvin_airflow.lineage.extractors.bigquery.AlvinBigQueryExtractor
    """

    # We override this method because not all Operators has the
    # the sql attribute, if the user is using a BigQueryInsertJobOperator
    # a bunch of stacktraces would show up in their logs, which we should avoid.
    # Only override this logic for AirflowV2 to reduce the chance to impact something.
    def parse_sql_context(self):
        try:
            if hasattr(self.operator, "sql"):

                # Here we just call the parent method, so we dont have to
                # copy all the code here.
                return super().parse_sql_context()
        except Exception as e:
            log.debug("Cannot parse sql context!")

        # Only import this SqlContext if we really need to!
        # This object is required and used down the code chain,
        # so we must return something from this method to not break
        from openlineage.airflow.extractors.bigquery_extractor import SqlContext

        return SqlContext(sql="", parser_error="Cannot parse sql context!")

    def get_bigquery_job_id(self, task_instance):
        bigquery_job_id = self._get_xcom_bigquery_job_id(task_instance)

        # we have a fallback logic that takes the job_id from the operator if its not filled
        # inside the xcom, doing some tests we saw this happen in the BigQueryInsertJobOperator
        if not bigquery_job_id and self.operator and hasattr(self.operator, "job_id"):
            bigquery_job_id = self.operator.job_id
        return bigquery_job_id

    def get_airflow_run_id(self, task_instance):
        dag_run = task_instance.get_dagrun()
        return dag_run.run_id

    def get_connection_id(self):
        return self.operator.gcp_conn_id if self.operator else None

    @classmethod
    def get_operator_classnames(cls) -> List[str]:
        return [
            "BigQueryExecuteQueryOperator",
            "BigQueryInsertJobOperator",
            "BigQueryOperator",
        ]


class AlvinBigQueryLegacyExtractor(AlvinBigQueryBaseExtractor):
    """
    This class contains logic for Airflow 1.

    Note that on this version, the BigQuery operator class part of the
    Airflow contrib google module.

    https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow#custom-extractors

    The following env var needs to be set in the airflow host environment:
    OPENLINEAGE_EXTRACTOR_BigQueryOperator
        =alvin_airflow.lineage.extractors.bigquery.AlvinBigQueryLegacyExtractor
    """

    def get_airflow_run_id(self, task_instance):
        return task_instance.get_dagrun().run_id

    def get_connection_id(self):
        return self.operator.bigquery_conn_id if self.operator else None

    @classmethod
    def get_operator_classnames(cls) -> List[str]:
        return ["BigQueryOperator"]
