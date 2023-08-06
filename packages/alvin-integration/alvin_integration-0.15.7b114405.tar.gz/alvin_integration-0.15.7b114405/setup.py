import setuptools

__base_version__ = "0.15.7"
__version__ ="0.15.7-beta.114405"

requirements = ["gorilla==0.4.0", "openlineage-airflow==0.6.1"]


setuptools.setup(
    name="alvin_integration",
    version=__version__,
    author="Alvin",
    author_email="tech@alvin.ai",
    description="Alvin lineage python library for integrations",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.7",
)
