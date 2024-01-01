
DOCKER_IMAGE_FULL_NAME=twsc

lock:
	poetry lock

build:
	docker build . -t ${DOCKER_IMAGE_FULL_NAME}

dev:
	docker run --rm -it --env-file .env -p 8000:8000 -v ./src/:/app/ -v ./data/:/data/ ${DOCKER_IMAGE_FULL_NAME}

format:
	isort .
	flake8 --config setup.cfg
	black --config pyproject.toml .


lint:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .
