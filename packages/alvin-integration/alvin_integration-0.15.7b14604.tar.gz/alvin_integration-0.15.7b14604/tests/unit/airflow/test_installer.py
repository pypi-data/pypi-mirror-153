import pkg_resources

from alvin_integration.producers.airflow.config import AirflowProducerConfig
from alvin_integration.producers.airflow.installer import AlvinAirflowInstaller


def test_setup_airflow_installer():

    alvin_airflow_installer = AlvinAirflowInstaller()

    assert alvin_airflow_installer.host_package_map == {
        "apache-airflow": pkg_resources.get_distribution("apache-airflow")
    }

    assert type(alvin_airflow_installer.provider_config) == AirflowProducerConfig

    assert alvin_airflow_installer.provider_config.producer_name == "Airflow"
