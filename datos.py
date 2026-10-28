import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def preparar_datos() -> pd.DataFrame:
    ruta_entrada = Path("datos/entrada")
    
    # 1. Leer
    df_alumnos = pd.read_csv(ruta_entrada / "alumnos.csv", sep=";", dtype={"id_alumno": str})
    df_notas = pd.read_csv(ruta_entrada / "notas.csv", sep=";", dtype={"id_alumno": str})
    
    # 2. Limpiar
    df_alumnos = df_alumnos.drop_duplicates(subset=["id_alumno"])
    for col in ["nota1", "nota2", "nota3"]:
        df_notas[col] = pd.to_numeric(df_notas[col], errors="coerce")
        
    # 3. Cruzar (Conservando todos los alumnos con 'left')
    alumnos_sin_notas = df_alumnos[~df_alumnos["id_alumno"].isin(df_notas["id_alumno"])]
    notas_sin_alumno = df_notas[~df_notas["id_alumno"].isin(df_alumnos["id_alumno"])]
    
    if not alumnos_sin_notas.empty:
        print(f"Alumnos sin notas: {', '.join(alumnos_sin_notas['id_alumno'])}")
    if not notas_sin_alumno.empty:
        print(f"Notas sin alumno: {', '.join(notas_sin_alumno['id_alumno'])}")
        
    df_informe = pd.merge(df_alumnos, df_notas, on="id_alumno", how="left")
    
    # 4. Calcular (min_count=3 exige que existan las 3 notas para sumar)
    df_informe["total"] = df_informe[["nota1", "nota2", "nota3"]].sum(axis=1, min_count=3)
    df_informe["media"] = (df_informe["total"] / 3).round(2)
    df_informe = df_informe.sort_values("id_alumno")
    
    return df_informe

def guardar_informes(informe: pd.DataFrame) -> None:
    ruta_salida = Path("datos/salida")
    ruta_salida.mkdir(parents=True, exist_ok=True)
    
    # 5. Guardar
    ruta_csv = ruta_salida / "informe_notas.csv"
    ruta_json = ruta_salida / "informe_notas.json"
    
    informe.to_csv(ruta_csv, index=False, sep=";")
    informe.to_json(ruta_json, orient="records", force_ascii=False)
    
    # 5. Comprobar
    check_csv = pd.read_csv(ruta_csv, sep=";", dtype={"id_alumno": str})
    check_json = pd.read_json(ruta_json, orient="records", dtype={"id_alumno": str})
    
    if len(check_csv) == len(informe) and len(check_json) == len(informe):
        print("CSV y JSON guardados y comprobados en datos/salida.")

def mostrar_grafico(informe: pd.DataFrame) -> None:
    ruta_salida = Path("datos/salida")
    ruta_salida.mkdir(parents=True, exist_ok=True)
    
    # 6. Representar
    # Filtrar solo alumnos que tienen las tres notas válidas (no nulas)
    df_validos = informe[informe[["nota1", "nota2", "nota3"]].notna().all(axis=1)]
    
    if df_validos.empty:
        print("No hay alumnos con las tres notas válidas para crear el gráfico.")
        return
        
    num_alumnos = len(df_validos)
    medias = df_validos[["nota1", "nota2", "nota3"]].mean()
    
    plt.figure(figsize=(8, 5))
    ax = medias.plot.bar(color="#32749A")
    plt.ylim(0, 10)
    plt.title(f"Media por actividad ({num_alumnos} alumnos)")
    plt.ylabel("Nota media")
    ax.set_xticklabels(["Actividad 1", "Actividad 2", "Actividad 3"], rotation=0)
    
    plt.savefig(ruta_salida / "medias_actividades.png")
    plt.show()