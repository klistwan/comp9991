alias fmt := format

activate:
    source .venv/bin/activate

format:
    ruff format .

lint:
    ruff main.py

run:
    . .venv/bin/activate && python main.py

test:
    pytest
