import logging
import os
import pathlib
import traceback

from airflow.lineage.backend import LineageBackend
from openlineage.lineage_backend import Backend

from alvin_integration.helper import AlvinLoggerAdapter

log = AlvinLoggerAdapter(logging.getLogger(__name__), {})


class AlvinAirflowBackend(Backend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


ALVIN_STATE_NOT_STARTED = "NOT_STARTED"
ALVIN_STATE_FINISHED = "FINISHED"


class AlvinStateSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AlvinStateSingleton, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        self._state = ALVIN_STATE_NOT_STARTED

    def set_state(self, new_value):
        self._state = new_value

    def get_state(self):
        return self._state


class AlvinBackendMeta(type):
    def __init__(cls, *args, **kwargs):
        from airflow.configuration import conf

        backend_str = conf.get("lineage", "backend")
        cls.alvin_state = AlvinStateSingleton()
        if backend_str and cls.__name__ in backend_str:
            cls.copy_alvin_plugin()

    @staticmethod
    def read_alvin_plugin():
        """Returns the alvin plugin path."""
        filepath = os.path.join(
            f"{pathlib.Path(__file__).resolve().parent}", "alvin_plugin.py"
        )

        return filepath

    def is_plugin_not_copied(cls, path):
        if cls.alvin_state.get_state() == ALVIN_STATE_NOT_STARTED:
            cls.alvin_state.set_state(ALVIN_STATE_FINISHED)
            return True
        return False

    def copy_alvin_plugin(cls):
        """Copy the Alvin plugin to the airflow plugins folder."""
        filepath = cls.read_alvin_plugin()
        plugin_path = os.path.join(f'{os.getenv("AIRFLOW_HOME")}', "plugins")
        if not os.path.exists(plugin_path):
            log.info(f"Creating plugins folder: {plugin_path}")
            os.makedirs(plugin_path)
        full_path = os.path.join(f"{plugin_path}", "alvin_plugin.py")
        if cls.is_plugin_not_copied(full_path):
            with open(full_path, "w") as plugin_file:
                with open(filepath, "r") as f:
                    content = f.read()
                    plugin_file.write(content)
            log.info(f"Plugin copied successfully to: {full_path}")
        else:
            log.info(f"Plugin already copied: {full_path}")


class AlvinBackendComposerMeta(AlvinBackendMeta):
    def __init__(self, *args, **kwargs):
        super(AlvinBackendComposerMeta, self).__init__(*args, **kwargs)
        self.patch_scheduler_functions()

    def copy_alvin_plugin(cls):
        plugin_path = os.path.join(f'{os.getenv("AIRFLOW_HOME")}', "plugins")
        full_path = os.path.join(f"{plugin_path}", "alvin_plugin.py")
        if cls.is_plugin_not_copied(full_path):
            from google.cloud import storage

            from alvin_integration.producers.airflow.config import (
                GOOGLE_COMPOSER_BUCKET,
            )

            print(
                f"Creating Alvin DAGs on Google Composer path {GOOGLE_COMPOSER_BUCKET}....."
            )

            filepath = cls.read_alvin_plugin()

            with open(filepath, "r") as f:
                content = f.read()

                client = storage.Client()

                bucket = client.get_bucket(GOOGLE_COMPOSER_BUCKET)

                blob = bucket.blob("plugins/alvin_plugin.py")

                blob.upload_from_string(content)

            print(
                f"Plugin copied successfully to: {GOOGLE_COMPOSER_BUCKET}/plugins/alvin_plugin.py"
            )
        else:
            log.info(f"Plugin already copied: {full_path}")

    def patch_scheduler_functions(cls):
        import gorilla
        import pkg_resources
        from airflow.models.dagrun import DagRun

        airflow_package = pkg_resources.get_distribution("apache-airflow")

        if airflow_package.version in ("2.1.4", "2.1.4+composer"):
            from alvin_integration.producers.airflow.patch.functions_214 import (
                update_state,
            )
        elif airflow_package.version in ("2.2.3", "2.2.5", "2.2.3+composer"):
            from alvin_integration.producers.airflow.patch.functions import update_state
        elif airflow_package.version in ("1.10.15", "1.10.15+composer"):
            from alvin_integration.producers.airflow.patch.functions_legacy import (
                update_state,
            )

        settings = gorilla.Settings(allow_hit=True)
        patch = gorilla.Patch(
            DagRun,
            update_state.__name__,
            update_state,
            settings=settings,
        )

        log.info(f"Installing: {patch}")

        gorilla.apply(patch)

        log.info(f"Patch: {patch} installed successfully.")


class AlvinAirflowLineageBackend(LineageBackend, metaclass=AlvinBackendMeta):
    backend: AlvinAirflowBackend = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def send_lineage(cls, *args, **kwargs):
        """Alvin implementation of the send_lineage backend."""
        log.info("calling send lineage with args and kwargs")
        if not cls.backend:
            log.info("Lineage backend is none, creating it")
            cls.backend = AlvinAirflowBackend()
        return cls.backend.send_lineage(*args, **kwargs)


class AlvinAirflowLineageBackendComposer(
    AlvinAirflowLineageBackend, metaclass=AlvinBackendComposerMeta
):
    pass


def alvin_callback(context, operator, is_airflow_legacy=False):
    """Alvin callback implementation.

    This function use the OpenLineage implementation of
    the Airflow Backend and call send_lineage with the
    given context.
    """
    try:
        if is_airflow_legacy:
            AlvinAirflowLineageBackend.send_lineage(
                context=context, operator=operator
            )  # noqa
        else:
            lineage_backend = AlvinAirflowLineageBackend()
            lineage_backend.send_lineage(context=context, operator=operator)
    except Exception:
        log.error(f"Alvin Callback Error: {traceback.format_exc()}")


def alvin_dag_run_extractor(dag_run):
    import os

    import requests

    from alvin_integration.producers.airflow.config import (
        ALVIN_BACKEND_API_KEY,
        ALVIN_BACKEND_API_URL,
    )

    if dag_run:
        log.info(
            f"Extracting and sending DagRun information for dag_id={dag_run.dag_id} and run_id={dag_run.run_id}"
        )
        try:
            ALVIN_PLATFORM_ID = os.getenv("ALVIN_PLATFORM_ID")
            alvin_backend_metadata_url = f"{ALVIN_BACKEND_API_URL}/api/v1/lineage"

            payload = {
                "alvin_platform_id": ALVIN_PLATFORM_ID,
                "facets": {
                    "dag_run": {
                        "dag_id": dag_run.dag_id,
                        "run_id": dag_run.run_id,
                        "queued_at": (
                            dag_run.queued_at.isoformat() if dag_run.queued_at else None
                        )
                        if hasattr(dag_run, "queued_at")
                        else None,
                        "execution_date": dag_run.execution_date.isoformat(),
                        "start_date": dag_run.start_date.isoformat(),
                        "end_date": dag_run.end_date.isoformat()
                        if dag_run.end_date
                        else None,
                        "state": dag_run.get_state(),
                    }
                },
            }
            requests.post(
                alvin_backend_metadata_url,
                json=payload,
                headers={"X-API-KEY": ALVIN_BACKEND_API_KEY},
            )
        except Exception as e:
            log.error(f"Error sending message to Alvin: {e}")
    else:
        log.info("Dag run not defined.")
