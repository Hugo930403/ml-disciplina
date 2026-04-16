import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

from training.build_dataset import build_dataset

def prepare_data(df):
    # 🔥 Convertir timedelta a minutos
    df["horas_trabajadas_total"] = df["horas_trabajadas_total"].dt.total_seconds() / 60
    df["tiempo_extra_total"] = df["tiempo_extra_total"].dt.total_seconds() / 60

    # 🔥 Features (QUITAMOS columnas que no sirven)
    X = df.drop(columns=[
        "target",
        "fecha_corte",
        "score",
        "empleado_id",
        "horas_trabajadas_total",
        "tiempo_extra_total",
        "faltas_count",
        "retardos_count",
        "salidas_temprano_count"
    ])
    y = df["target"]

    return X, y


def train():
    df = build_dataset()

    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"  # 👈 clave
    )

    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:, 1]

    threshold = 0.2  # ajustar umbral para pruebas

    y_pred = (y_proba >= threshold).astype(int)

    y_pred = (y_proba >= threshold).astype(int)
    print(f"\nThreshold:")
    print(classification_report(y_test, y_pred))

    importances = model.feature_importances_
    cols = X_train.columns

    df_imp = pd.DataFrame({
        "feature": cols,
        "importance": importances
    }).sort_values("importance", ascending=False)

    print("\nImportancia de variables:")
    print(df_imp)

    joblib.dump(model, "model_disciplina.pkl")
    joblib.dump(X_train.columns.tolist(), "columns.pkl")


if __name__ == "__main__":
    train()