# End-to-end tests (Playwright + pytest)

This folder contains the autonomous end-to-end suite. It boots its own
isolated docker-compose stack (frontend + api + Postgres on dedicated ports)
before the tests run, and tears it down at the end. The same setup works
locally and in GitHub Actions.

## Layout

```mermaid
e2e/
├── docker-compose.e2e.yaml   # isolated stack (ports 8080/8001/5435)
├── conftest.py               # session fixture that boots/tears down the stack
├── pytest.ini
├── requirements.txt
├── tests/
│   ├── __init__.py
│   └── test_smoke.py         # template; start here
└── README.md
```

## First-time setup

From the repo root:

```bash
cd e2e
python -m venv .venv
. .venv/Scripts/activate   # Windows (Git Bash)
# or: source .venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
playwright install --with-deps chromium
```

`playwright install --with-deps` downloads the browser binary and (on Linux)
the required system libraries. On Windows/macOS the `--with-deps` flag is
ignored — that's fine.

## Run the tests

```bash
# from e2e/
pytest                       # boots the stack, runs all tests, tears it down
pytest -m smoke              # only the smoke template
pytest --headed              # watch the browser drive the app
pytest -k text_block         # by name
```

The fixture takes approximately 1 or 2 minutes the first time (docker image build) and a few
seconds on subsequent runs.

### Faster iteration during development

While writing tests you don't want to wait for the stack to boot on every
run. Start it once manually, then point pytest at it:

```bash
# Terminal 1 : boot the stack and leave it up
docker compose -f docker-compose.e2e.yaml up -d --build --wait

# Terminal 2 :  run tests against the running stack
E2E_USE_RUNNING_STACK=1 pytest --headed -k my_new_test

# When done
docker compose -f docker-compose.e2e.yaml down -v
```

The `E2E_USE_RUNNING_STACK=1` env var tells the fixture to skip
boot/teardown and just check the URLs are reachable.

## Recording tests with `playwright codegen`

Playwright ships an interactive recorder that watches what you click and
generates the pytest code for it.

```bash
# Boot the stack first
docker compose -f docker-compose.e2e.yaml up -d --build --wait

# Launch the recorder
playwright codegen --target python-pytest http://localhost:8080
```

A browser opens alongside an inspector window. Do whatever interaction you
want to record (clicks, fills, navigation) and the inspector writes the
corresponding pytest test in real time. When you're done:

1. Copy the generated function into a new file under `e2e/tests/`
   (e.g. `tests/test_login.py`).
2. Rename it to start with `test_`.
3. Replace the hard-coded URL by the `base_url` fixture:

   ```python
   def test_my_flow(page, base_url):
       page.goto(base_url)              # was: page.goto("http://localhost:8080")
       ...
   ```

4. Replace brittle selectors (`page.locator("div >> nth=3")`) by stable ones
   prefer `get_by_role`, `get_by_label`, `get_by_test_id`. The recorder
   tries to pick stable ones but doesn't always succeed.
5. Run it: `pytest tests/test_login.py --headed -k my_flow`.

Tear the stack down when you're done recording:

```bash
docker compose -f docker-compose.e2e.yaml down -v
```

## Conventions

- One file per user flow (e.g. `test_login.py`, `test_text_block_editor.py`).
- Use the `base_url` fixture, never hard-code `http://localhost:8080`.
- Mark template / pipeline-validation tests with `@pytest.mark.smoke`.
- Prefer Playwright's role/label-based locators; they survive UI tweaks.

## When a test fails

1. Re-run the single failing test while watching the browser: `E2E_USE_RUNNING_STACK=1 pytest -k my_test --headed`
2. Open the Playwright trace recorded on failure thanks to `--tracing=retain-on-failure`: `playwright show-trace test-results/<...>/trace.zip`
3. Inspect the stack if the app itself misbehaves: `docker compose -f docker-compose.e2e.yaml logs`
4. Reset a stuck/poisoned stack so the DB reseeds cleanly: `docker compose -f docker-compose.e2e.yaml down -v`
5. In CI the trace is uploaded as the `playwright-traces` artifact and the stack logs are printed in the failed job. Download the artifact and open it locally with `playwright show-trace`.
6. Don't merge while the e2e suite is red.

## CI

The workflow `.github/workflows/e2e-test.yml` runs the same suite on push
and PR. It installs Python, the dependencies, the Chromium browser, then
calls `pytest`. The stack is booted by the fixture ; no separate
docker-compose step needed.
