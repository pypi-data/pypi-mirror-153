AIRFLOW_V1=1.10.15
AIRFLOW_V2=2.2.3
AIRFLOW_VERSION?=$(AIRFLOW_V2)

install-dev:
	pip install poetry
	poetry install

lint:
	poetry run isort \
		--atomic \
		$(PWD)
	poetry run black \
		$(PWD)
	poetry run flake8 \
		--ignore=E501,
	poetry run bandit \
		--recursive \
		--number=3 \
		-ll \
		-ii \
		$(PWD)

clean:
	docker system prune -f
	rm --recursive --force $(PWD)/alvin_backend/*.egg-info
	rm --recursive --force $(PWD)/alvin_backend/build
	rm --recursive --force $(PWD)/alvin_backend/dist

# pip install wheel
build-dist:
	python setup.py sdist bdist_wheel
	ls -lah $(PWD)/dist

# pip install twine
pypi-publish:
	twine upload \
		--username alvindotai \
		--password $(PYPI_PSW) \
		$(PWD)/dist/*

build-airflow:
	docker build \
		--build-arg PYTHON_BASE_IMAGE="python3.8" \
		--build-arg AIRFLOW_VERSION=$(AIRFLOW_VERSION) \
		--tag $(AIRFLOW_VERSION) \
		--file docker/airflow/Dockerfile \
		.

run-airflow:
	export AIRFLOW_IMAGE_NAME=2.2.3 && cd $(PWD)/docker/airflow && docker compose up

stop-airflow:
	export AIRFLOW_IMAGE_NAME=2.2.3 && cd $(PWD)/docker/airflow && docker compose down

build-legacy:
	docker build \
		--build-arg PYTHON_BASE_IMAGE="python3.8" \
		--build-arg AIRFLOW_VERSION=$(AIRFLOW_V1) \
		--tag $(AIRFLOW_V1) \
		--file docker/airflow/Dockerfile.legacy \
		.

run-legacy:
	export AIRFLOW_IMAGE_NAME=2.2.3 && cd $(PWD)/docker/airflow && docker compose -f docker-compose.legacy.yaml up

stop-legacy:
	export AIRFLOW_IMAGE_NAME=2.2.3 && cd $(PWD)/docker/airflow && docker compose -f docker-compose.legacy.yaml down

test: build-airflow
	docker run \
		-it \
		--entrypoint=python \
		--user airflow $(AIRFLOW_VERSION) \
		-m pytest
