# csp zeromq adapter

A [csp](https://github.com/point72/csp) adapter for [zeromq](https://zeromq.org).

## Features

Exposes the following patterns:
- Pub / Sub 
- Push / Pull

In progress:
- Req / Rep

## Development

We utilize conda for managing environment dependencies. In order to create your development environment:

```bash
git clone https://github.com/wrieg123/csp-zeromq-adapter.git
cd csp-zeromq-adapter
micromamba create -n csp-zmq -f conda/dev-env-unix.yml
micromamba activate csp-zmq
make requirements
```

Building C++:
```bash
make build
```

Installing Python:
```bash
make develop
```

Tests:
```bash
make test
```


