"""
This module contains the data models that will be produced
and sent to the Alvin Backend.
"""
import importlib
import os
from dataclasses import dataclass
from typing import List


@dataclass
class AlvinAirflowTaskExecution:
    task_id: str
    dag_id: str
    run_id: str
    start_date: str
    end_date: str
    duration: float
    try_number: int
    pool: str
    operator: str
    state: str
    run_id: str
    platform_id: str
    max_tries: int
    alvin_package_version: str


@dataclass
class AlvinBaseLineageDetails:
    execution: AlvinAirflowTaskExecution
    connection_id: str


@dataclass
class AlvinBigQueryLineageDetails(AlvinBaseLineageDetails):
    job_id: str
    project_id: str


@dataclass
class AlvinSnowflakeLineageDetails(AlvinBaseLineageDetails):
    query_ids: List[str]


@dataclass
class AlvinFacet:
    alvin: AlvinBaseLineageDetails


@dataclass
class AlvinPatch:
    package_name: str
    function: any
    supported_versions: List[str]
    destination_path: str
    is_required: bool = False

    @property
    def destination(self):
        module_name, class_name = self.destination_path.rsplit(".", 1)
        return getattr(importlib.import_module(module_name), class_name)

    def __repr__(self):
        return (
            f"package_name: {self.package_name}, "
            f"patch: {self.function}, "
            f"supported_versions: {self.supported_versions}, "
            f"destination: {self.destination}"
        )


@dataclass
class AlvinLineageConfig:
    package_name: str
    env_name: str
    env_value: str
    supported_versions: List[str]

    def set_lineage(self):
        os.environ[self.env_name] = self.env_value

    def __repr__(self):
        return (
            f"package_name: {self.package_name}, "
            f"env_name: {self.env_name}, "
            f"env_value: {self.env_value}, "
            f"supported_versions: {self.supported_versions}, "
        )


@dataclass
class AlvinPipelineCreator:
    package_name: str
    function: any
    supported_versions: List[str]

    def __repr__(self):
        return (
            f"function: {self.function}, "
            f"supported_versions: {self.supported_versions}"
        )
