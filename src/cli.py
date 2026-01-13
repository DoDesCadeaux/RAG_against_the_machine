import fire
import json
from pathlib import Path
from pydantic import ValidationError
from .models import RagDataset, StudentSearchResults, MinimalSearchResults


class App:
    def hello(self, name: str = "world") -> None:
        """Tiny command to verify the CLI works"""
        print(f"hello {name}")

    def _validate_dataset(self, dataset_path: str) -> RagDataset:
        """Validate a RAG dataset JSON file.

        Args:
            dataset_path: Path to a JSON file matching RagDataset schema.

        Raises:
            RuntimeError: If the file can't be read, JSON is invalid, or schema validation fails.
        """
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
        return dataset

    def search_dataset(self, dataset_path: str, k: int = 10, save_dir: str = "data/output/search_results") -> None:
        try:
            dataset = self._validate_dataset(dataset_path)
        except RuntimeError as e:
            raise RuntimeError("Error Validation Dataset") from e

        if isinstance(save_dir, str):
            try:
                results: list[MinimalSearchResults] = []
                for q in dataset.rag_questions:
                    results.append(
                        MinimalSearchResults(
                            question_id=q.question_id,
                            question=q.question,
                            retrieved_sources=[]
                        )
                    )

                out = StudentSearchResults(search_results=results, k=k)
                output_path = Path(save_dir) / Path(dataset_path).name
                Path(save_dir).mkdir(parents=True, exist_ok=True)
                output_path.write_text(out.model_dump_json(indent=4), encoding="utf-8")
            except TypeError as e:
                raise RuntimeError("JSON Serialisation Error") from e
            except ValidationError as e:
                raise RuntimeError("StudentSearchResults model Validation failed") from e
            except (PermissionError, IsADirectoryError, OSError) as e:
                raise RuntimeError("File writing error") from e
            print(f"Output JSON : {out}")

            data = json.loads(output_path.read_text(encoding="utf-8"))
            print(data)


def main() -> None:
    fire.Fire(App)
