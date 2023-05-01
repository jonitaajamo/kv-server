SHELL := /bin/bash

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
IMAGE = kv-server

.PHONY: run
run: $(VENV)/bin/activate
	uvicorn kv_server.main:app --reload


.PHONY: requirements
requirements: requirements-dev.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements-dev.txt


.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf $(VENV)

.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE) .

.PHONY: docker-run
docker-run:
	docker run -p 80:80 -v ./data:/kv_server/data -e KV_DATA_FILE_PATH=/kv_server/data/example.data $(IMAGE)

.PHONY: load_test
load_test:
	locust --host=http://localhost --users=1000 --headless --run-time=1m -f load_tests/locustfile.py