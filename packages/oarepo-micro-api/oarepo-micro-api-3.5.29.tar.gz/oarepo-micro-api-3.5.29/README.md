# OARepo Micro API

[![image](https://img.shields.io/travis/oarepo/oarepo-micro-api.svg)](https://travis-ci.org/oarepo/oarepo-micro-api)
[![image](https://img.shields.io/coveralls/oarepo/oarepo-micro-api.svg)](https://coveralls.io/r/oarepo/oarepo-micro-api)
[![image](https://img.shields.io/github/license/oarepo/oarepo-micro-api.svg)](https://github.com/oarepo/oarepo-micro-api/blob/master/LICENSE)

OARepo REST API microservice module

## Getting Started

This package will provide a simple UWSGI microservice that will serve
all of the registered OArepo API apps in your repository instance under the `/api` endpoint. It also
provides some `/.well-known` endpoints that are usable for running in k8s environments.

### Prerequisites

- Python >=3.6
- Docker

### How to use

Specify this package as a dependency in your OArepo repository project's `setup.py`.
If you're using `oarepo` as a base package for your repository, you should use the following extras:
```python
# setup.py
#...
install_requires = [
    'oarepo[micro-api,...another-oarepo-extras]'
]
#...
```
otherwise:
```python
# setup.py
#...
install_requires = [
    'oarepo-micro-api'
]
#...
```

After that, reinstall your project by:
```
pip install -e .
```

Start your repository instance and verify, that everything worked out, by running:
```
curl -k https://localhost:5000/.well-known/heartbeat/readiness
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
