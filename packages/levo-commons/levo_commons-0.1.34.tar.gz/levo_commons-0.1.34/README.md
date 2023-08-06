# levo-commons
Common code between Levo's CLI and test plans

# Running the checks and tests locally

```bash
# Pre-commit checks
pip install pre-commit
SKIP=pylint,mypy pre-commit run --all-files
pre-commit run mypy --all-files

# Unit tests
pip install tox
tox -e py
```
