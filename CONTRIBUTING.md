# Contributing

## Getting started

```bash
git clone git@github.com:oysters76/dice-viz.git
cd dice-viz
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Project structure

```
src/dice/
  __init__.py      # public API re-exports
  cli.py           # argparse CLI (simulate + plot subcommands)
  config.py        # ExperimentConfig dataclass
  simulation.py    # roll(), experiment(), theoretical_stats()
  plotting.py      # run_experiments(), overlay_gaussian()
tests/
  conftest.py      # shared fixtures
```

## Code style

- Format and lint with **ruff** (`ruff check src/ tests/` and `ruff format src/ tests/`)
- Keep dependencies minimal
- Use stdout for output, stderr for progress
- JSON output should be supported where practical

## Running tests

```bash
pytest -v
```

## Submitting changes

1. Fork the repository
2. Create a feature branch (`git checkout -b my-feature`)
3. Write tests for new functionality
4. Ensure `ruff check` and `pytest` pass
5. Open a pull request against `main`
