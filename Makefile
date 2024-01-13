run-debug:
	poetry run python debug.py

format:
	poetry run black .
	poetry run ruff . --fix