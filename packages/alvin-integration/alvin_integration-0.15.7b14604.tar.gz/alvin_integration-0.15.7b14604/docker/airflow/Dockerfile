ARG AIRFLOW_VERSION="2.2.2"

ARG PYTHON_BASE_IMAGE="python3.7"

FROM apache/airflow:${AIRFLOW_VERSION}

ENV AIRFLOW_VERSION=${AIRFLOW_VERSION}

ENV PYTHON_BASE_IMAGE=${PYTHON_BASE_IMAGE}

FROM apache/airflow:${AIRFLOW_VERSION}-${PYTHON_BASE_IMAGE}

RUN mkdir -p ${AIRFLOW_HOME}/alvin_integration

RUN chown airflow ${AIRFLOW_HOME}/alvin_integration

USER airflow

RUN pip install poetry

COPY ./../../poetry.lock ${AIRFLOW_HOME}/poetry.lock

COPY ./../../pyproject.toml ${AIRFLOW_HOME}/pyproject.toml

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./../../tests ${AIRFLOW_HOME}/tests

COPY ./../../alvin_integration ${AIRFLOW_HOME}/alvin_integration/alvin_integration

COPY ./../../setup.py ${AIRFLOW_HOME}/alvin_integration/setup.py

RUN cd ${AIRFLOW_HOME}/alvin_integration && pip install -e .

RUN pip install apache-airflow-providers-google

RUN pip install apache-airflow-providers-snowflake
