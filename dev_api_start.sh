#!/bin/bash
set -e

./.venv/bin/uvicorn app.api.main_dev:app --port 8888 --reload