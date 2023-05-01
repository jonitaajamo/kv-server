# Key-Value Server

This is a small in-memory read-only Key-Value server implemented with Python, which serves users through HTTP REST API.
It reads a file with rows in format `<key> <value>`, where <key> cannot include any whitespace and value can contain whitespace.

## Developing

### Requirements

- Python 3.11 (verified)
- Python Venv*
- Docker*
- Cmake*

*Optional

### Installing

To install development requirements and run the application on most Unix-like systems, run:

```bash
make requirements
source venv/bin/activate
make run
```

A file of Key-Value pairs are used as data-source.
The file path can be configured by using `KV_DATA_FILE_PATH`, if it's not provided, [data/example.data](./data/example.data) is used.
[scripts/bix_example_generator.py](./scripts/bix_example_generator.py) can be used to generate large sample.

### Docker

To build and run the Docker image, you can use the following make commands:

```bash
make docker-build
make docker-run
```

### Testing

#### Unit tests

Unit tests are implemented into [tests/](./tests/).
You can execute the unit test suite by running:

```bash
make test
```

#### Load testing

Load testing can be performed using Locust.
Locust comes with dev-requirements and it can be run using:

```bash
make load_test
```
##### Pre-run tests

Following tests were ran with Intel(R) Core(TM) i7-6700K CPU @ 4.00GHz running Linux ubuntu 5.15.0-71-generic #78~20.04.1-Ubuntu.

To execute the test, [./load_tests/locustfile.py](./load_tests/locustfile.py) and command `locust --host=http://localhost --users=1000 --headless --run-time=1m -f load_tests/locustfile.py` were used against KV-server storing 10000 KV-pairs.
So in other words, the load test was executed with 1000 concurrent users for a duration of 1 minute, targeting the endpoint `/key/{key}` with random keys from a list of test data. The result is shown below:

|Type    |50%     |66%   |75%   |80%   |90%   |95%   |98%   |99%   |99.9% |99.99%|  100%| # reqs|
|--------|--------|------|------|------|------|------|------|------|------|------|------|-------|
| Agg.   |6       |7     |7     |8     |10    |12    |14    |16    |130   |210   |210   |3167   |

Highest response time was 210 ms, and median response time reached 6 ms.

## Design decisions

The design philosophy of this application is simplicity.

The KV-server:

- Is Read Only
- Single-threaded, but asynchronous
- Reads values from file to memory at application startup
  - More than 1M KV-pairs can be stored in memory in most systems
  - Duplicate keys are ignored, latest key (i.e. lower on the list) stays in effect
- Serves values through single HTTP GET endpoint: `/keys/{key}`
- Is easy to run with multiple replicas
  - No need to share state between replicas
- Readability over minimal dependencies: FastAPI is used to achieve highly readable, simple codebase and implementing safety, such as blocking injection out of the box
- Implements no authentication

### Further considerations

Depending on changing requirements, KV-server might need to change the design philosophy entirely.

Following features and changes might be required, but not limited to:
- If writes or modifications of KV-pairs needs to implemented, some other data access should be implemented for scalability, e.g. database file with caching.
- Current implementation uses Uvicorn Asynchronous Server Gateway Interface (ASGI) to take care of workload balancing on host system. If better visibility and control over this is required for e.g. for higher traffic, custom implementation should be used or some other language entirely, such as Rust or Golang.
- For production deployments, authentication, Role-Based Access Control, Kubernetes manifests with multiple replicas, traffic based scaling policies, automated CI/CD pipelines along with proper networking and load-balancing configs should be implemented.
- If Python implementation is kept, ASGI worker configuration should be reviewed
- If feature to read the data from file is kept, more format checking should be done to it
