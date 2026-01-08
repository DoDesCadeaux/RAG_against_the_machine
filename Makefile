# Règle par défaut
all: install lint

# Installation propre de l'environnement
install:
	uv sync

# Vérification de la qualité du code
lint:
	uv run flake8 src/
	uv run mypy --warn-return-any --check-untyped-defs src/

# Nettoyage
clean:
	rm -rf .venv .mypy_cache .uv
	find . -type d -name "__pycache__" -exec rm -rf {} +
