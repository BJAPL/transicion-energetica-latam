"""
04 - Ejecuta las consultas SQL de análisis
------------------------------------------
Corre cada archivo sql/0[1-9]_*.sql contra la base SQLite, guarda el resultado
en outputs/<consulta>.csv y genera outputs/resultados_consultas.md (vista rápida en GitHub).

Uso:
    python src/04_ejecutar_consultas.py
"""
from pathlib import Path
import sqlite3

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RUTA_DB = RAIZ / "data" / "transicion_energetica.db"
DIR_SQL = RAIZ / "sql"
DIR_OUT = RAIZ / "outputs"


def a_markdown(df: pd.DataFrame) -> str:
    """Tabla markdown sin depender de 'tabulate'."""
    df = df.astype(object).where(df.notna(), "")
    filas = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    filas += ["| " + " | ".join(map(str, fila)) + " |" for fila in df.itertuples(index=False)]
    return "\n".join(filas)


def titulo_pregunta(sql: str) -> str:
    """Une la pregunta 'P#' del encabezado del .sql aunque ocupe varias líneas."""
    partes, dentro = [], False
    for linea in sql.splitlines():
        if linea.startswith("-- P"):
            dentro = True
        elif dentro and (not linea.startswith("--     ") or linea.startswith("-- ===")):
            break
        if dentro:
            partes.append(linea.removeprefix("--").strip())
    return " ".join(partes)


def main() -> None:
    DIR_OUT.mkdir(exist_ok=True)
    con = sqlite3.connect(RUTA_DB)
    md = ["# Resultados de las consultas SQL\n",
          "Generado por `src/04_ejecutar_consultas.py`. Cada sección corresponde a un archivo de `sql/`.\n"]
    for ruta in sorted(DIR_SQL.glob("0[1-9]_*.sql")):
        sql = ruta.read_text(encoding="utf-8")
        df = pd.read_sql_query(sql, con)
        df.to_csv(DIR_OUT / f"{ruta.stem}.csv", index=False, encoding="utf-8")
        print(f"[ok] {ruta.name}: {len(df)} filas")
        md += [f"## {ruta.stem}\n", f"**{titulo_pregunta(sql)}**\n", a_markdown(df), ""]
    con.close()
    (DIR_OUT / "resultados_consultas.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
