import logging

from openlineage.airflow.extractors.base import TaskMetadata
from openlineage.airflow.extractors.snowflake_extractor import SnowflakeExtractor
from openlineage.airflow.utils import (
    get_connection,
    get_normalized_postgres_connection_uri,
    safe_import_airflow,
)
from openlineage.client.facet import SqlJobFacet
from openlineage.common.dataset import Dataset, Source
from openlineage.common.sql import SqlMeta, SqlParser

from alvin_integration.models import AlvinFacet, AlvinSnowflakeLineageDetails
from alvin_integration.producers.airflow.lineage.extractors.mixins import (
    AlvinAirflowExtractorMixin,
)

logger = logging.getLogger(__name__)


class AlvinSnowflakeBaseExtractor(AlvinAirflowExtractorMixin, SnowflakeExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_hook(self):
        raise NotImplementedError

    def get_connection_id(self):
        return self.operator.snowflake_conn_id if self.operator else None

    def build_facet(self, task_instance):
        return AlvinFacet(
            alvin=AlvinSnowflakeLineageDetails(
                query_ids=self._get_query_ids(),
                execution=self.get_execution_details(task_instance),
                connection_id=self.get_connection_id(),
            )
        )

    def _get_database(self) -> str:
        return self._get_hook().database

    def _get_authority(self) -> str:
        return self._get_hook().snowflake_conn_id


class AlvinSnowflakeExtractor(AlvinSnowflakeBaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_hook(self):
        return self.operator.get_db_hook()

    def _get_query_ids(self):
        return self.operator.query_ids

    def get_airflow_run_id(self, task_instance):
        return task_instance.run_id


class AlvinSnowflakeLegacyExtractor(AlvinSnowflakeBaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("AlvinSnowflakeLegacyExtractor")

    def _get_hook(self):
        return self.operator.get_hook()

    def extract(self) -> TaskMetadata:

        sql_meta: SqlMeta = SqlParser.parse(self.operator.sql, self.default_schema)

        self.conn = get_connection(self._conn_id())

        source = Source(
            scheme=self._get_scheme(),
            authority=self._get_authority(),
            connection_url=self._get_connection_uri(),
        )

        database = self.operator.database
        if not database:
            database = self._get_database()

        inputs = [
            Dataset.from_table(
                source=source,
                table_name=in_table_schema.table_name.name,
                schema_name=in_table_schema.schema_name,
                database_name=database,
            )
            for in_table_schema in self._get_table_schemas(sql_meta.in_tables)
        ]
        outputs = [
            Dataset.from_table_schema(
                source=source, table_schema=out_table_schema, database_name=database
            )
            for out_table_schema in self._get_table_schemas(sql_meta.out_tables)
        ]
        query_ids = self._get_query_ids()

        return TaskMetadata(
            name=f"{self.operator.dag_id}.{self.operator.task_id}",
            inputs=[ds.to_openlineage_dataset() for ds in inputs],
            outputs=[ds.to_openlineage_dataset() for ds in outputs],
            job_facets={
                "sql": SqlJobFacet(self.operator.sql),
                "queries_ids": query_ids if query_ids else [],
            },
        )

    def _get_query_ids(self):
        hook = self.operator.get_hook()
        print(hook)
        if hasattr(hook, "query_ids"):
            print(f"Query ids found: {hook.query_ids}")
            return hook.query_ids
        else:
            print(f"Query ids not found")
            return []

    def get_airflow_run_id(self, task_instance):
        return task_instance.get_dagrun().run_id
