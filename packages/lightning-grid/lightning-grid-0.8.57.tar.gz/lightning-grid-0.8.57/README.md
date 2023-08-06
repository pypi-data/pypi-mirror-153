# Grid CLI

## Getting Started

The Grid CLI is written in Python as a simple client to the backend.
It makes requestst via the Backend's GraphQL API and renders responses
in a terminal UI.

If you are unfamiliar wtih GraphQL, take a look at the [GraphQL spec](https://graphql.org/).

1. Install the CLI.

```shell
# clone project
git clone https://github.com/gridai/grid
cd grid/grid-cli

make develop
```

That will install all the Python requirements packages, including
development dependencies. It will do so in a Python virtual environment
using Python's native `venv`.

Then, activate your virtual environment and export required environment
variables to your environment. Make a copy of the file `.env.example`
as `.env` (it contains all the env vars) and export them into your
environment with (or your other env magament tool):

```shell
export $(cat .env)
```

Make sure that `GRID_URL` is pointing to your local database, ie
`export GRID_URL=http://localhost:8000/graphql`

You should now be all setup to develop the CLI.

You will also need to have a local version of the backend server running.
Follow the instructions in [Getting Started](../README.md) to get going.

## Using as a CLI

You can test the CLI functionally by installing it as a local package
with:

```shell
pip install -e .
```

The Grid CLI will be available under `grid`.

```shell
grid status
```

**Note:** test dependencies have a dependency problem with the CLI
when packaged. If you do this you will need to re-install the dependencies
for continue to run tests. You can do that with:

```shell
source venv/bin/deactivate
rm -rf venv
make develop
```
