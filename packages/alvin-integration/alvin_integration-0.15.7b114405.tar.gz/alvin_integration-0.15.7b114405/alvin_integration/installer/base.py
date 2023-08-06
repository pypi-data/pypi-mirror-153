import logging
import traceback

import gorilla
import pkg_resources

from alvin_integration.helper import AlvinLoggerAdapter
from alvin_integration.interfaces.config import AbstractProducerConfig

log = AlvinLoggerAdapter(logging.getLogger(__name__), {})


class AlvinBaseInstaller:
    """
    Class responsible to manage the installation of Alvin
    components in the Producer host environment.
    """

    def __init__(self, provider_config: AbstractProducerConfig):
        self.provider_config = provider_config
        self.host_package_map = dict()

    def _load_supported_patches(self):
        log.info("Start load_supported_patches")
        """Load patches compatible with host environment."""
        supported_patches = []
        for patch in self.provider_config.get_patching_list():
            try:
                log.info(f"Looking at patch: {patch}")

                host_package = self.host_package_map.get(patch.package_name)

                log.info(f"Found this package: {host_package}")

                if host_package.version in patch.supported_versions:
                    supported_patches.append(patch)
                    log.info(f"Adding patch: {patch}")
            except ModuleNotFoundError as err:
                log.warning(
                    f"Error loading patch for destination: {patch.destination_path}: {err}"
                )
        return supported_patches

    def install_patches(self):
        """
        Install patches for compatible with the target
        packages of the host environment
        """
        supported_patches = self._load_supported_patches()

        log.info(f"Installing {len(supported_patches)} patches")

        settings = gorilla.Settings(allow_hit=True)

        for patch_config in supported_patches:
            patch = gorilla.Patch(
                patch_config.destination,
                patch_config.function.__name__,
                patch_config.function,
                settings=settings,
            )

            log.info(f"Installing: {patch}")

            gorilla.apply(patch)

            log.info(
                f"Patched {patch.destination.__module__} "
                f"{patch.destination.__name__} {patch.name}"
            )

    def load_host_packages(self):
        """Load host environment packages based on the Producer config"""
        target_packages = self.provider_config.get_target_packages()
        log.info(
            f"Matching host packages {target_packages} for {self.provider_config.producer_name}"
        )
        for target_package in target_packages:
            host_package = pkg_resources.get_distribution(target_package)
            log.info(f"Host package match: {host_package}")
            if host_package:
                self.host_package_map[target_package] = host_package

    def install_pipelines(self):
        """Install pipelines based on teh Producer config."""
        target_pipelines = self.provider_config.get_target_pipelines()
        for target_pipeline in target_pipelines:
            host_package = self.host_package_map.get(target_pipeline.package_name)
            log.info(f"Host Package {host_package}")
            log.info(f"Target Pipeline {target_pipeline}")
            if host_package.version in target_pipeline.supported_versions:
                log.info(f"Installing dag {target_pipeline}")
                pipeline = target_pipeline.function
                pipeline()
                log.info(f"Pipeline {pipeline} creation executed.")

    def install_lineage(self):
        """Install lineage components based on the Producer config."""
        lineage_config = self.provider_config.get_lineage_config()
        for config in lineage_config:
            host_package = self.host_package_map.get(config.package_name)
            log.info(f"Lineage: {config}")
            log.info(f"Host Package: {host_package}")
            if host_package.version in config.supported_versions:
                log.info(f"Installing lineage: {config.env_name} - {config.env_value}")
                config.set_lineage()
                log.info(f"Lineage {config} installed successfully.")

    def install(self):
        """Install Alvin components in the Producer environment."""
        try:
            log.info("Starting Alvin Integration Package installation.")

            self.load_host_packages()

            self.install_patches()

            self.install_lineage()

            self.install_pipelines()

            log.info("Alvin Integration Package completed successfully.")

        except Exception:
            log.error(f"Installation failed with error: {traceback.format_exc()}")
