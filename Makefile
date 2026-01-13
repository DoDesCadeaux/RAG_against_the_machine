# Règle par défaut
all: install lint

# Installation propre de l'environnement
install:
	uv sync

# Vérification de la qualité du code
lint:
	uv run flake8 src/
	uv run mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src/
	uv run mypy src/ --strict

# Nettoyage
clean:
	rm -rf .venv .mypy_cache .uv
	find . -type d -name "__pycache__" -exec rm -rf {} +

clean-results:
	rm -rf data/outputs

run:
	uv run python -m src hello --name=Dorian


debug:
	uv run python -m pdb -m src hello --name=Dorian