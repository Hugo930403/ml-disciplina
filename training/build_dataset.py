import pandas as pd
from training.load_data import load_estadisticas
from training.features import build_fuatures
from training.target import build_target

def build_dataset():
    df = load_estadisticas()

    df = df.sort_values(["EmpleadoId", "Fecha"])

    empleados = df["EmpleadoId"].unique()

    dataset = []

    for emp in empleados:
        df_emp = df[df["EmpleadoId"] == emp].copy()

        # 🔥 ORDENAR Y CREAR MESES
        df_emp = df_emp.sort_values("Fecha")
        df_emp["Mes"] = df_emp["Fecha"].dt.to_period("M")

        # 🔥 FECHAS DE CORTE (fin de cada mes)
        fechas_corte = df_emp.groupby("Mes")["Fecha"].max().values

        for fecha_corte in fechas_corte:

            features = build_fuatures(df, fecha_corte, emp, 90)
            score = build_target(df, fecha_corte, emp, 90)

            if features is None or score is None:
                continue

            features["score"] = score

            dataset.append(features)

    # 🔥 YA FUERA DEL LOOP
    dataset_df = pd.DataFrame(dataset)

    # 🔥 TARGET GLOBAL (muy importante que sea aquí)
    threshold = dataset_df["score"].quantile(0.8)
    dataset_df["target"] = (dataset_df["score"] >= threshold).astype(int)

    return dataset_df


if __name__ == "__main__":
    df = build_dataset()

    print("\nDistribución target:")
    print(df["target"].value_counts())

    print("\nProporción:")
    print(df["target"].value_counts(normalize=True))

    print("\nTipos de datos:")
    print(df.dtypes)

    print("\nScore stats:")
    print(df["score"].describe())

    print("\nScores únicos:")
    print(df["score"].nunique())