c:
	uv run ruff check

g:
	uv run alembic revision --autogenerate -m "$(m)"

up:
	uv run alembic upgrade head

down:
	uv run alembic downgrade -1

s:
	uv venv

r:
	fastapi run src/main.py

i:
	uv sync