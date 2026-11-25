# My Universe Doc

MyUniverseDoc is an advanced collaborative wiki for documenting universes (fictional or creative). It lets you create entries (characters, places, objects…), manage access rights, and collaborate easily to structure, share, and enrich your worlds.

## Requirements

- [Docker and Docker Compose](https://docs.docker.com/get-docker/)
- Python 3.12 or newer (to run the tests locally; CI uses 3.12)
- git
- (optional) [pnpm](https://pnpm.io/) for frontend development
- (optional) PGAdmin to inspect the database

## Running the program

From the project root:

```bash
docker compose up -d --build
```

The application is then available at <http://localhost>.

The stack starts three containers:

| Service  | Container   | Role                              | Exposed port         |
|----------|-------------|-----------------------------------|----------------------|
| frontend | `myd_front` | React + Vite served by nginx      | 80                   |
| api      | `myd_api`   | FastAPI API (uvicorn)             | 8000 (internal)      |
| db       | `myd_db`    | PostgreSQL 18                     | 127.0.0.1:5432       |

The API is not exposed directly: nginx acts as a proxy. The database is initialized automatically with the scripts in `backend/src/data/`, and its data is persisted in the `db-data` Docker volume.

Useful commands:

```bash
docker compose logs -f      # follow the logs
docker compose down         # stop the stack
docker compose down -v      # stop and remove the database data
```

### Frontend development (outside Docker)

```bash
cd frontend
pnpm install
pnpm dev        # Vite dev server with HMR
pnpm lint       # lint with Biome
pnpm build      # production build
```

## Running the tests

The project has three levels of tests: unit and integration on the backend, and end-to-end with Playwright. All three also run in CI (workflows `.github/workflows/unit-integration-test.yml` and `.github/workflows/e2e-test.yml`).

### Backend Python environment (once)

```bash
cd backend
python -m venv .venv
pip install -r requirements-dev.txt   # after activating the venv
```

Activate the venv with `.venv\Scripts\Activate.ps1` (PowerShell), `. .venv/Scripts/activate` (Git Bash) or `source .venv/bin/activate` (Linux/macOS).

> **Windows:** if `python` opens the Microsoft Store or says it is not found, it is the Store alias in `WindowsApps`. Use the `py` launcher instead (`py -m venv .venv`), or call the venv interpreter directly: `.venv\Scripts\python.exe -m pytest ...`. You can also disable the alias in *Settings → Apps → Advanced app settings → App execution aliases*.

All the commands below are run from `backend/` with the venv activated (or prefixed with `.venv\Scripts\python.exe -m`).

### Unit tests (backend)

Located in `backend/tests/units/`, they mock the repositories and need no database:

```bash
pytest tests/units/ -v
```

### Integration tests (backend)

Located in `backend/tests/integration/`, they exercise controllers, services and repositories against a real PostgreSQL. They need:

1. A `backend/.env.test` file (gitignored, to be created once), loaded automatically by the `test_db` fixture. Its values must match `docker-compose.test.yaml`:

    ```env
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5434
    DATABASE_NAME=my_universe_doc_db_test
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=myuniversedocpwdb
    ```

2. The test database (container `myd_db_test`, PostgreSQL 18 on port 5434). Docker Desktop must be running:

    ```bash
    docker compose -f docker-compose.test.yaml up -d --wait   # --wait returns once the DB is healthy
    ```

Then run the suite, or the whole backend suite at once:

```bash
pytest tests/integration/ -v
pytest tests/ -q                       # units + integration
pytest tests/integration/test_session_token_repository.py -k expired -v   # one file / one test
```

The database can stay up between runs. Stop it when you are done:

```bash
docker compose -f docker-compose.test.yaml down -v
```

#### How the test database is reset

- **On container creation**, PostgreSQL runs `backend/src/data/*.sql` (schema `00.sql`, `01.sql`, then the demo seed `99.sql`). These scripts only run when the volume is empty, so **after changing a `.sql` file, recreate the container** with `down -v` then `up -d --wait`.
- **Before every test**, the autouse `reset_db` fixture (`tests/integration/conftest.py`) truncates the tables (`RESTART IDENTITY CASCADE`, which also empties `session_token`) and replays `99.sql`. Each test therefore starts from the same seed: users 1 to 4 (password `azer`), their universes, entities, etc. A test can freely insert or delete data.

#### Writing an integration test

- Build the objects through `src.factory.Factory()` (`factory.user_controller`, `factory.session_repository`, …) so the real dependency graph is used.
- Tests are plain `async def` functions or methods: `asyncio_mode = auto` is set in `pytest.ini`, no decorator needed.
- Rely on the ids from `99.sql` rather than hard-coding data you did not insert yourself.
- For anything time-related (token expiration…), compare with `NOW()` in SQL rather than `datetime.now()` in Python, the Python process and the Postgres container may not share the same time zone. See `tests/integration/test_session_token_repository.py` for an example.
- The app imports its modules both as `src.models.x` and `models.x`. Python treats them as two different modules, so `isinstance(obj, src.models.x.Model)` can be `False` on an object built by the app. Assert on the fields instead.

#### If an integration test fails

1. Read the failing assertion, then re-run just that test: `pytest tests/integration/ -k <name> -v`.
2. `ValueError: db_host` (or another `db_*`) during setup: `backend/.env.test` is missing or incomplete.
3. Connection refused / timeout: the container is not running (`docker ps`) or Docker Desktop is stopped. Start it with `docker compose -f docker-compose.test.yaml up -d --wait`.
4. Errors about a missing column or table: the schema in the container is older than `src/data/*.sql`. Recreate it: `docker compose -f docker-compose.test.yaml down -v && docker compose -f docker-compose.test.yaml up -d --wait`.
5. The integration tests share the same schema/seed as production (`backend/src/data/*.sql`). A failure there often means a real regression in the repository layer. Fix the code, don't adjust the test to make it green, except if you really wanted to change the program behaviour.
6. Never merge while this suite is red.

### End-to-end tests (Playwright + pytest)

The e2e suite boots its own isolated Docker stack (frontend + api + PostgreSQL on ports 8080/8001/5435) before the tests run, and tears it down at the end.

First-time setup:

```bash
cd e2e
python -m venv .venv
. .venv/Scripts/activate        # Windows (Git Bash) or: source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps chromium
```

Running:

```bash
pytest              # boots the stack, runs all tests, tears it down
pytest --headed     # to watch the browser drive the app
```

See [e2e/README.md](e2e/README.md) for details: faster iteration against an already-running stack, recording tests with `playwright codegen`, writing conventions.

## Deploying on a server

The full procedure for deploying on an Ubuntu server (installing Docker, starting the stack, configuring the firewall) is described in [deployment.md](deployment.md).

## Additional documentation

- [backend/README.md](backend/README.md): backend setup guide
- [e2e/README.md](e2e/README.md): full end-to-end testing guide
- [deployment.md](deployment.md): deployment on an Ubuntu server

## Continuous integration

CI runs on Github Actions and is defined by two workflows:

- [`.github/workflows/unit-integration-test.yml`](.github/workflows/unit-integration-test.yml) corresponding to units tests and integration/functional tests (TI/TF)
- [`.github/workflows/e2e-test.yml`](.github/workflows/e2e-test.yml) corresponding to end-to-end tests. (TE2E)

Both trigger on push and pull request to `main` and `dev`.

### Scope TU / TI / TF / TE2E

Unit tests and integration tests, plus end-to-end suite. There is no separate functional test layer. The integration tests are the functional tests, exercising the repository layer against a real PostGreSQL.

### Where to find the results

The **Action** tab on Github and the checks shown on each pull request. On an e2e failure, the Playwright trace is attached to the run as the `playwright-traces` artifact.

### Lint checkout

The unit and integration test workflows has a lint check with `ruff`.
A `frontend-lint.yml` workflow exists to check the code with the `biome` linter.

### If CI fails

Open the failed job, read the step logs and reproduce locally with the exact same command (`pytest tests/units/`, `pytest tests/integration/`, or `pytest` from `e2e/`). Fix the cause and push again. A red pipeline blocks the merge.

### Static analysis

The frontend is linted with  [Biome](https://biomejs.dev/) (`frontend/biome.json`, `pnpm lint`); the backend with [Ruff](https://docs.astral.sh/ruff/).
