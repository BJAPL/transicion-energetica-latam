"""
03 - Carga del modelo a una base de datos SQLite
------------------------------------------------
Crea data/transicion_energetica.db con el esquema de sql/00_esquema.sql
y carga los CSV procesados. Al final ejecuta controles de integridad referencial.

Uso:
    python src/03_cargar_sql.py
"""
from pathlib import Path
import sqlite3

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DIR_PROC = RAIZ / "data" / "processed"
RUTA_DB = RAIZ / "data" / "transicion_energetica.db"

# Orden de carga: primero dimensiones, luego hechos (por las llaves foráneas)
TABLAS = ["dim_pais", "dim_fuente", "fact_pais_anio", "fact_generacion"]

CONTROLES = {
    "Filas de fact_generacion sin país en dim_pais":
        "SELECT COUNT(*) FROM fact_generacion g LEFT JOIN dim_pais p USING (iso3) WHERE p.iso3 IS NULL",
    "Filas de fact_generacion sin fuente en dim_fuente":
        "SELECT COUNT(*) FROM fact_generacion g LEFT JOIN dim_fuente f USING (fuente_id) WHERE f.fuente_id IS NULL",
    "País-año donde la suma por fuente no cuadra con el total (>0,5%)":
        """SELECT COUNT(*) FROM (
               SELECT g.iso3, g.anio, SUM(g.generacion_twh) AS suma, MAX(pa.generacion_twh) AS total
               FROM fact_generacion g JOIN fact_pais_anio pa USING (iso3, anio)
               GROUP BY g.iso3, g.anio
               HAVING ABS(suma - total) > 0.005 * total)""",
}


def main() -> None:
    if RUTA_DB.exists():
        RUTA_DB.unlink()
    con = sqlite3.connect(RUTA_DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript((RAIZ / "sql" / "00_esquema.sql").read_text(encoding="utf-8"))

    for tabla in TABLAS:
        df = pd.read_csv(DIR_PROC / f"{tabla}.csv")
        for col in df.select_dtypes("bool").columns:  # SQLite no tiene BOOLEAN
            df[col] = df[col].astype(int)
        df.to_sql(tabla, con, if_exists="append", index=False)
        print(f"[ok] {tabla}: {len(df):,} filas")

    print("\nControles de integridad:")
    errores = 0
    for nombre, consulta in CONTROLES.items():
        n = con.execute(consulta).fetchone()[0]
        errores += n
        print(f"  {'OK ' if n == 0 else 'ERR'} {nombre}: {n}")
    con.commit()
    con.close()
    if errores:
        raise SystemExit("Hay errores de integridad, revisar la limpieza.")
    print(f"\nBase creada en {RUTA_DB.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
