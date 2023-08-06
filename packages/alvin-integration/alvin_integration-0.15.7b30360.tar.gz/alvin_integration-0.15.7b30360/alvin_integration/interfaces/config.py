from abc import ABC, abstractmethod


class AbstractProducerConfig(ABC):
    @property
    @abstractmethod
    def producer_name(self):
        pass

    @abstractmethod
    def get_patching_list(self):
        pass

    @abstractmethod
    def get_target_packages(self):
        pass

    @abstractmethod
    def get_target_pipelines(self):
        pass

    @abstractmethod
    def get_lineage_config(self):
        pass
