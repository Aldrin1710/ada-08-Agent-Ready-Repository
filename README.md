# Customer Search CLI (`ada-08-agent-ready-repository`)

Command-line application in Python 3.11+ for searching customer records in a local JSON database (`data/customers.json`), structured as an **Agent-Ready Repository**.

## Quick Navigation
- **Operational Contract**: [`AGENTS.md`](AGENTS.md)
- **Repository Map**: [`docs/REPO_MAP.md`](docs/REPO_MAP.md)
- **Sources of Truth**: [`REQUIREMENTS.md`](REQUIREMENTS.md) · [`SPEC.md`](SPEC.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`TASKS.md`](TASKS.md)
- **Controlled Task Under Test**: [`TASK_UNDER_TEST.md`](TASK_UNDER_TEST.md)

## Running the CLI
```bash
python src/cli.py "ale"
```

## Verification Contract
```bash
./scripts/verify_repo.sh
```
