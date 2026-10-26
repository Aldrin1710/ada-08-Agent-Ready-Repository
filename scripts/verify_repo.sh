#!/usr/bin/env bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1

echo "[1/3] Running tests"
python -B -m pytest -q -p no:cacheprovider tests/

echo "[2/3] Running syntax and static checks"
python -B -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in list(pathlib.Path('src').glob('*.py')) + list(pathlib.Path('tests').glob('*.py')) + list(pathlib.Path('scripts').glob('*.py'))]"

echo "[3/3] Repository checks"
python -B scripts/check_repo_contract.py

echo "VERIFY_REPO: PASS"
