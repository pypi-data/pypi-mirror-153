import os
from dataclasses import asdict
from importlib.metadata import version
from typing import Optional

from openlineage.airflow.extractors.base import TaskMetadata

from alvin_integration.constants import ALVIN_PACKAGE_NAME
from alvin_integration.models import AlvinAirflowTaskExecution


class AlvinAirflowExtractorMixin:
    def build_facet(self, task_instance):
        raise NotImplementedError

    def build_task_metadata(self, task_instance):
        raise NotImplementedError

    def get_airflow_run_id(self, task_instance):
        raise NotImplementedError

    def get_connection_id(self):
        raise NotImplementedError

    def get_alvin_package_version(self):
        return version(ALVIN_PACKAGE_NAME)

    def get_alvin_platform_id(self):
        return os.getenv("ALVIN_PLATFORM_ID")

    def extract_on_complete(self, task_instance) -> Optional[TaskMetadata]:

        if not task_instance:
            return self.extract()

        alvin_facet = self.build_facet(task_instance)

        task_metadata = self.extract()

        if not task_metadata:
            task_metadata = self.build_task_metadata(task_instance)

        print(f"Alvin Facet: {asdict(alvin_facet)}")

        task_metadata.job_facets.update(asdict(alvin_facet))

        return task_metadata

    def get_execution_details(self, task_instance):
        return AlvinAirflowTaskExecution(
            task_id=task_instance.task_id,
            dag_id=task_instance.dag_id,
            run_id=self.get_airflow_run_id(task_instance),
            start_date=task_instance.start_date.isoformat(),
            end_date=task_instance.end_date.isoformat()
            if task_instance.end_date
            else None,
            duration=task_instance.duration,
            try_number=task_instance.try_number,
            pool=task_instance.pool,
            operator=task_instance.operator,
            state=task_instance.state,
            max_tries=task_instance.max_tries,
            platform_id=self.get_alvin_platform_id(),
            alvin_package_version=self.get_alvin_package_version(),
        )
