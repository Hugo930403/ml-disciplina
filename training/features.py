import pandas as pd

def build_fuatures(df, fecha_corte, empleado_id, window_day=90):
    inicio = fecha_corte - pd.Timedelta(days=window_day)

    df_emp = df[
        (df["EmpleadoId"] == empleado_id) &
        (df["Fecha"] > inicio) &
        (df["Fecha"] <= fecha_corte)
    ]

    if df_emp.empty:
        return None
    
    total_dias = len(df_emp)

    features = {
        
        "empleado_id": empleado_id,
        "fecha_corte": fecha_corte,

        "faltas_count": df_emp["Falta"].sum(),
        "retardos_count": df_emp["Retardo"].sum(),
        "salidas_temprano_count": df_emp["SalidaTemprano"].sum(),

        "horas_trabajadas_total": df_emp["HorasTrabajadas"].sum(),
        "tiempo_extra_total": df_emp["TiempoExtra"].sum(),

        "ratio_retardos": df_emp["Retardo"].sum() / total_dias if total_dias else 0,
        "faltas_ratio": df_emp["Falta"].sum() / total_dias,
        "retardos_ratio": df_emp["Retardo"].sum() / total_dias,
        "salidas_ratio": df_emp["SalidaTemprano"].sum() / total_dias
    }

    return features
    