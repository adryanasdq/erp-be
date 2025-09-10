c:
	uv run ruff check

g:
	uv run alembic revision --autogenerate -m "$(m)"

up:
	uv run alembic upgrade head

s:
	uv venv

r:
	uv run src/main.py

i:
	uv sync