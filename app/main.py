from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(
    title="ML Disciplina Empleados",
    version="1.0"
)

model = joblib.load("model_disciplina.pkl")
columns = joblib.load("columns.pkl")

THRESHOLD = 0.3

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: dict):
    try:
        df = pd.DataFrame([data])

        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return {
                "error": f"Faltan columnas: {missing_cols}"
            }

        df = df[columns]

        proba = model.predict_proba(df)[0][1]

        prediction = int(proba >= THRESHOLD)

        return {
            "riesgo": prediction,
            "probabilidad": float(proba)
        }
    except Exception as e:
        return {"error": str(e)}