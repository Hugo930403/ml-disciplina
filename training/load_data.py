import pandas as pd
from app.database import engine

def load_estadisticas(limit=None):
    query = "SELECT * FROM EstadisticaEmpleados"

    if limit:
        query += f" LIMIT {limit}"

    df = pd.read_sql(query, engine)

    df["Fecha"] = pd.to_datetime(df["Fecha"])

    df = df.sort_values(["EmpleadoId", "Fecha"])
    df = df.reset_index(drop=True)

    return df

if __name__== "__main__":
    df = load_estadisticas(limit=1000)

    print(df.head())
    print("\nShape:", df.shape)
    print("\nColumns:", df.columns)