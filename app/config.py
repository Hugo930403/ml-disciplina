from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODELS_DIR = ARTIFACTS_DIR / "models"
DATASETS_DIR = ARTIFACTS_DIR / "datasets"

MODEL_DISCIPLINA_PRUEBA = "disciplina_prueba_v1.pkl"
MODEL_DISCIPLINA_INDEFINIDO = "disciplina_indefinido_v1.pkl"