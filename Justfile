activate:
    source .venv/bin/activate

format:
    ruff format .

lint:
    ruff .

run:
    . .venv/bin/activate && python main.py
