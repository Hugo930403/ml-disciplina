import pandas as pd

def build_target(df, fecha_corte, empleado_id, window_day=90):
    fin = fecha_corte + pd.Timedelta(days=window_day)

    df_future = df[
        (df["EmpleadoId"] == empleado_id) &
        (df["Fecha"] > fecha_corte) &
        (df["Fecha"] <= fin)
    ]

    if df_future.empty:
        return None

    dias = len(df_future)

    # Conteos
    faltas = df_future["Falta"].sum()

    # Ratios
    ratio_dias_malos = (
        (df_future["Falta"] |
         df_future["Retardo"] |
         df_future["SalidaTemprano"]).sum()
    ) / dias

    # Intensidad
    avg_minutos_retardo = df_future["MinutosRetardo"].mean()
    max_minutos_retardo = df_future["MinutosRetardo"].max()
    std_retardos = df_future["MinutosRetardo"].std()

    # Manejo de NaN
    std_retardos = std_retardos if pd.notna(std_retardos) else 0

    # SCORE
    score = (
        (faltas / dias) * 40 +
        ratio_dias_malos * 30 +
        avg_minutos_retardo * 0.5 +
        max_minutos_retardo * 0.2 +
        std_retardos * 0.3
    )

    return score