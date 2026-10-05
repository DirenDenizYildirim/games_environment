#!/usr/bin/env bash
# Reproduce every number in RESULTS.md. Resumable: re-run after an interruption.
set -euo pipefail
cd "$(dirname "$0")"
python sanity.py
python run_all.py calib4
python run_all.py calib5
python run_all.py sanity
python run_all.py main
python analyze.py calib
python analyze.py main
