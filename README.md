# ORGA-PINESS

## Requirements

- [Docker >= 17.05](https://docs.docker.com/engine/release-notes/17.05/)
- [Python >= 3.7](https://www.python.org/downloads/)
- [Poetry](https://github.com/python-poetry/poetry)

> **NOTE** - Run all commands from the project root

## Local development

### Poetry

Create the virtual environment and install dependencies with:

```shell
poetry install
```

See the [poetry docs](https://python-poetry.org/docs/) for information on how to add/update dependencies.

Run commands inside the virtual environment with:

```shell
poetry run <your_command>
```

Spawn a shell inside the virtual environment with:

```shell
poetry shell
```

Start a development server locally:

```shell
poetry run uvicorn app.main:app --reload --host localhost --port 8002
```

API will be available at [localhost:8002/](http://localhost:8002/)

- Swagger UI docs at [localhost:8002/docs](http://localhost:8002/docs)
- ReDoc docs at [localhost:8002/redoc](http://localhost:8002/redoc)

To run testing/linting locally you would execute lint/test in the [scripts directory](/scripts).
## Docker

Build images with:
```shell
docker build --tag orga_piness --file docker/Dockerfile .
```

The Dockerfile uses multi-stage builds to run lint and test stages before building the production stage.
If linting or testing fails the build will fail.

You can stop the build at specific stages with the `--target` option:

```shell
docker build --name orga_piness --file docker/Dockerfile . --target <stage>
```

For example we wanted to stop at the **test** stage:

```shell
docker build --tag orga_piness --file docker/Dockerfile --target test .
```

We could then get a shell inside the container with:

```shell
docker run -it orga_piness:latest bash
```

If you do not specify a target the resulting image will be the last image defined which in our case is the 'production' image.



## Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)