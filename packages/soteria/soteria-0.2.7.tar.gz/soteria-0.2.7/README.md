# Soteria

A modular monitoring system with a cron-style scheduler.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Soteria.

```bash
pip install soteria
```

## Usage
Additional files will be needed for the package to work. *config.py*, *encrypted.yaml*, *database_lookup.py*.

```python
from soteria.soteria_scheduler import SoteriaScheduler

scheduler = SoteriaScheduler()
scheduler.start_scheduler()

```

## License
[MIT](https://choosealicense.com/licenses/mit/)