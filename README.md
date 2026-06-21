# My Universe Doc

MyUniverseDoc is an advanced collaborative wiki for documenting universes (fictional or creative). It lets you create entries (characters, places, objects…), manage access rights, and collaborate easily to structure, share, and enrich your worlds.

## Requirements

- [Docker and Docker Compose](https://docs.docker.com/get-docker/)
- Python 3.13 minimum (to run the tests locally)
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

### Unit tests (backend)

No external dependency, just the Python environment:

```bash
cd backend
pip install -r requirements-dev.txt
pytest tests/units/ -v
```

### Integration tests (backend)

They require a dedicated test database, started via `backend/docker-compose.test.yaml` (PostgreSQL on port 5434), and a `backend/.env.test` file (gitignored, to be created once) that is loaded automatically by the tests:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5434
DATABASE_NAME=my_universe_doc_db_test
POSTGRES_USER=postgres
POSTGRES_PASSWORD=myuniversedocpwdb
```

Then:

```bash
cd backend
docker compose -f docker-compose.test.yaml up -d
pytest tests/integration/ -v
```

Finally, stop the test database:

```bash
docker compose -f docker-compose.test.yaml down -v
```

#### If an integration test fails

1. Read the failing assertion, then re-run just that test: `pytest tests/integration/ -k <name> -v`.
2. Most failures come from a stale DB. Reseed it from scratch:
    `docker compose -f docker-compose.test.yaml down -v && docker compose -f docker-compose.test.yaml up -d`.
3. Check the DB is reachable on port 5434 and that `backend/.env.test` matches the compose file.
4. The integration tests share the same schema/seed as production (`backend/src/data/*.sql). A failure there often means a real refression in the repository layer. Fix the code, don't adjust the test to make it green, except if you really wanted to change the program comportment.
5. Never merge while this suite is red.

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

The full procedure for deploying on an Ubuntu server (installing Docker, starting the stack, configuring the firewall) is described in [deploiement.md](deploiement.md).

## Additional documentation

- [backend/README.md](backend/README.md): backend setup guide
- [e2e/README.md](e2e/README.md): full end-to-end testing guide
- [deploiement.md](deploiement.md): deployment on an Ubuntu server
