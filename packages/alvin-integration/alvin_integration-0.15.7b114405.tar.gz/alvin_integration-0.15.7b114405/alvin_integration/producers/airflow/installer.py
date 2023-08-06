from alvin_integration.installer.base import AlvinBaseInstaller
from alvin_integration.producers.airflow.config import AirflowProducerConfig


class AlvinAirflowInstaller(AlvinBaseInstaller):
    def __init__(self, *args, **kwargs):
        super(AlvinAirflowInstaller, self).__init__(
            provider_config=AirflowProducerConfig(), *args, **kwargs
        )
