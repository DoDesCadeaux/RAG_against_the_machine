import fire
import json
from pathlib import Path
from pydantic import ValidationError
from .models import RagDataset


class App:
    def hello(self, name: str = "world") -> None:
        """Tiny command to verify the CLI works"""
        print(f"hello {name}")

    def validate_dataset(self, dataset_path: str) -> None:
        """Load a dataset JSON file and validate it with Pydantic"""
        path = Path(dataset_path)

        try:
            raw_text = path.read_text(encoding="utf-8")
            raw_obj = json.loads(raw_text)
            dataset = RagDataset.model_validate(raw_obj)
        except OSError as e:
            raise RuntimeError(f"Cannot read file: {path}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON: {path}") from e
        except ValidationError as e:
            raise RuntimeError(f"Dataset schema error: {path}\n{e}") from e

        print(f"OK: {len(dataset.rag_questions)} questions loaded")


def main() -> None:
    app = App()
    fire.Fire(app)
