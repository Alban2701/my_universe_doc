"""
Session-wide fixtures for the autonomous E2E suite.

The `e2e_stack` fixture spins up an isolated docker-compose stack (frontend +
api + postgres on dedicated ports), waits for it to be reachable, yields the
base URL of the frontend, and tears the stack down at the end of the test
session.

Set ``E2E_USE_RUNNING_STACK=1`` to skip the start/stop dance and reuse a
stack that's already running (handy during local development when you're
iterating on tests).
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

import httpx
import pytest

HERE = Path(__file__).parent
COMPOSE_FILE = HERE / "docker-compose.e2e.yaml"

FRONTEND_URL = "http://localhost:8080"
API_URL = "http://localhost:8001"

READINESS_TIMEOUT_SECONDS = 180
READINESS_POLL_INTERVAL = 1.0


def _compose(*args: str) -> None:
    """Run a docker-compose command against our e2e file."""
    cmd = ["docker", "compose", "-f", str(COMPOSE_FILE), *args]
    subprocess.run(cmd, check=True)


def _wait_until_ready(url: str, deadline: float, label: str) -> None:
    """Poll an HTTP endpoint until it returns a 2xx, or fail with a clear msg."""
    last_error: str | None = None
    while time.monotonic() < deadline:
        try:
            response = httpx.get(url, timeout=2.0)
            if response.status_code < 400:
                return
            last_error = f"HTTP {response.status_code}"
        except httpx.HTTPError as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        time.sleep(READINESS_POLL_INTERVAL)
    raise RuntimeError(
        f"{label} at {url} did not become ready within "
        f"{READINESS_TIMEOUT_SECONDS}s (last error: {last_error})"
    )


@pytest.fixture(scope="session")
def e2e_stack() -> str:
    """Boot the stack, yield the frontend base URL, then tear it down."""
    use_running = os.getenv("E2E_USE_RUNNING_STACK") == "1"

    if not use_running:
        _compose("up", "-d", "--build", "--wait")

    try:
        deadline = time.monotonic() + READINESS_TIMEOUT_SECONDS
        _wait_until_ready(f"{API_URL}/", deadline, "API")
        _wait_until_ready(f"{FRONTEND_URL}/", deadline, "Frontend")
        yield FRONTEND_URL
    finally:
        if not use_running:
            # `down -v` to drop the seeded DB volume so the next run reseeds.
            _compose("down", "-v")


@pytest.fixture(scope="session")
def base_url(e2e_stack: str) -> str:
    """Public alias used by tests."""
    return e2e_stack


# Tighten the default pytest-playwright browser context: deterministic viewport
# and a sensible navigation timeout. Tests can override via their own fixtures.
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "ignore_https_errors": True,
    }
