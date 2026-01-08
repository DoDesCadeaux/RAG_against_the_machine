from pydantic import BaseModel, ValidationError


class SimpleSource:
    def __init__(self, file_path: str, index: int):
        self.file_path = file_path
        self.index = index


# Erreur silencieuse
source = SimpleSource("file.py", "cent")
print(source.index)  # Affiche 100  Ça cassera les calculs plus tard


class MinimalSource(BaseModel):  # Héritage obligatoire
    file_path: str
    first_character_index: int
    last_character_index: int


try:
    # Tentative avec une erreur (str au lieu d'int)
    s = MinimalSource(
        file_path="vllm/core.py",
        first_character_index="abc",
        last_character_index=500
    )
except ValidationError as e:
    print("Donnée invalude détectée !")
    print(e)
