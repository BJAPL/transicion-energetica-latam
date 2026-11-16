"""
02 - Limpieza y modelado de datos con pandas
--------------------------------------------
Toma los CSV crudos de OWID y genera un modelo en estrella listo para SQL y Power BI:

    data/processed/dim_pais.csv          -> una fila por país (región, subregión, flag LatAm)
    data/processed/dim_fuente.csv        -> una fila por fuente de generación (renovable/fósil/nuclear)
    data/processed/fact_generacion.csv   -> generación eléctrica (TWh) por país, año y fuente (formato largo)
    data/processed/fact_pais_anio.csv    -> indicadores anuales por país (participaciones, CO2, población...)

Además escribe outputs/reporte_calidad.md con cada decisión de limpieza y su impacto.

Uso:
    python src/02_limpieza.py
"""
from pathlib import Path
import logging

import numpy as np
import pandas as pd
import country_converter as coco
from babel import Locale

logging.getLogger("country_converter").setLevel(logging.CRITICAL)

RAIZ = Path(__file__).resolve().parents[1]
DIR_RAW = RAIZ / "data" / "raw"
DIR_PROC = RAIZ / "data" / "processed"
DIR_OUT = RAIZ / "outputs"

ANIO_INICIO = 2000
TOLERANCIA_SUMA = 0.005  # 0,5 % de diferencia permitida entre la suma de fuentes y el total

# Fuentes de generación eléctrica en OWID -> (id, nombre, categoría, orden, grupo para gráficos)
FUENTES = {
    "coal": ("carbon", "Carbón", "Fósil", 1, "Carbón"),
    "gas": ("gas", "Gas natural", "Fósil", 2, "Gas y petróleo"),
    "oil": ("petroleo", "Petróleo", "Fósil", 3, "Gas y petróleo"),
    "nuclear": ("nuclear", "Nuclear", "Nuclear", 4, "Nuclear"),
    "hydro": ("hidro", "Hidroeléctrica", "Renovable", 5, "Hidroeléctrica"),
    "solar": ("solar", "Solar", "Renovable", 6, "Solar"),
    "wind": ("eolica", "Eólica", "Renovable", 7, "Eólica"),
    "biofuel": ("bioenergia", "Bioenergía", "Renovable", 8, "Otras renovables"),
    "other_renewable_exc_biofuel": ("otras_renov", "Geotermia y otras", "Renovable", 9, "Otras renovables"),
}
# Paleta categórica validada (separación para daltonismo) para los 7 grupos de gráfico
COLOR_GRUPO = {
    "Carbón": "#6250D6", "Gas y petróleo": "#E87BA4", "Nuclear": "#E34948", "Hidroeléctrica": "#2A78D6",
    "Solar": "#EDA100", "Eólica": "#1BAF7A", "Otras renovables": "#008300",
}

REGION_ES = {
    "South America": ("América Latina y el Caribe", "Sudamérica"),
    "Central America": ("América Latina y el Caribe", "Centroamérica y México"),
    "Caribbean": ("América Latina y el Caribe", "Caribe"),
    "Northern America": ("Norteamérica", "Norteamérica"),
    "Northern Europe": ("Europa", "Europa del Norte"),
    "Western Europe": ("Europa", "Europa Occidental"),
    "Southern Europe": ("Europa", "Europa del Sur"),
    "Eastern Europe": ("Europa", "Europa del Este"),
    "Eastern Asia": ("Asia", "Asia Oriental"),
    "South-eastern Asia": ("Asia", "Sudeste Asiático"),
    "Southern Asia": ("Asia", "Asia del Sur"),
    "Central Asia": ("Asia", "Asia Central"),
    "Western Asia": ("Asia", "Asia Occidental y Medio Oriente"),
    "Northern Africa": ("África", "Norte de África"),
    "Western Africa": ("África", "África Occidental"),
    "Eastern Africa": ("África", "África Oriental"),
    "Middle Africa": ("África", "África Central"),
    "Southern Africa": ("África", "África Austral"),
    "Australia and New Zealand": ("Oceanía", "Australia y Nueva Zelanda"),
    "Melanesia": ("Oceanía", "Islas del Pacífico"),
    "Micronesia": ("Oceanía", "Islas del Pacífico"),
    "Polynesia": ("Oceanía", "Islas del Pacífico"),
    "Antarctica": ("Antártica", "Antártica"),
}

# Nombres en español desde los datos CLDR de Babel; aquí solo se corrigen los que no quedan bien
NOMBRE_ES_MANUAL = {
    "HKG": "Hong Kong", "MAC": "Macao", "PSE": "Palestina", "ANT": "Antillas Neerlandesas",
    "FLK": "Islas Malvinas", "USA": "Estados Unidos",
}

log_calidad: list[str] = []


def registrar(paso: str, detalle: str) -> None:
    """Guarda cada decisión de limpieza para el reporte de calidad."""
    print(f"- {paso}: {detalle}")
    log_calidad.append(f"| {paso} | {detalle} |")


def cargar_crudos() -> tuple[pd.DataFrame, pd.DataFrame]:
    energia = pd.read_csv(DIR_RAW / "owid-energy-data.csv")
    co2 = pd.read_csv(DIR_RAW / "owid-co2-data.csv")
    registrar("Carga", f"energía: {energia.shape[0]:,} filas × {energia.shape[1]} columnas; "
                       f"CO2: {co2.shape[0]:,} filas × {co2.shape[1]} columnas")
    return energia, co2


def filtrar_paises(df: pd.DataFrame, nombre: str) -> pd.DataFrame:
    """OWID mezcla países con agregados (continentes, grupos de ingreso, 'World').
    Los agregados no tienen ISO3 o empiezan con 'OWID_'. Se excluyen para no contar dos veces."""
    es_pais = df["iso_code"].notna() & ~df["iso_code"].str.startswith("OWID_", na=False)
    excluidas = df.loc[~es_pais, "country"].nunique()
    registrar(f"Filtrar agregados ({nombre})",
              f"se excluyen {excluidas} entidades que no son países (regiones, grupos, 'World'); "
              f"quedan {df.loc[es_pais, 'iso_code'].nunique()} países")
    return df.loc[es_pais].copy()


def construir_dim_pais(isos: list[str]) -> pd.DataFrame:
    cc = coco.CountryConverter()
    unr = cc.convert(isos, src="ISO3", to="UNregion", not_found=None)
    nombre_en = cc.convert(isos, src="ISO3", to="name_short", not_found=None)
    dim = pd.DataFrame({"iso3": isos, "subregion_un": unr, "pais_en": nombre_en})
    # Antillas Neerlandesas (ANT) ya no existe como país y coco no la reconoce
    dim.loc[dim.iso3 == "ANT", ["subregion_un", "pais_en"]] = ["Caribbean", "Netherlands Antilles"]
    sin_region = dim["subregion_un"].isna().sum()
    if sin_region:
        registrar("Regiones", f"{sin_region} países sin región asignada: {dim.loc[dim.subregion_un.isna(), 'iso3'].tolist()}")
    dim["region"] = dim["subregion_un"].map(lambda r: REGION_ES.get(r, ("Otra", "Otra"))[0])
    dim["subregion"] = dim["subregion_un"].map(lambda r: REGION_ES.get(r, ("Otra", "Otra"))[1])
    iso2 = cc.convert(isos, src="ISO3", to="ISO2", not_found=None)
    territorios_es = Locale("es").territories
    dim["pais"] = [NOMBRE_ES_MANUAL.get(i3) or territorios_es.get(i2 or "", None) or en
                   for i3, i2, en in zip(dim["iso3"], iso2, dim["pais_en"])]
    dim["es_latam"] = dim["region"].eq("América Latina y el Caribe")
    registrar("Dimensión país", f"{len(dim)} países; {dim.es_latam.sum()} de América Latina y el Caribe")
    return dim[["iso3", "pais", "pais_en", "region", "subregion", "es_latam"]].sort_values("iso3")


def limpiar_energia(energia: pd.DataFrame) -> pd.DataFrame:
    df = energia[energia["year"] >= ANIO_INICIO].copy()
    registrar("Periodo", f"se conserva {ANIO_INICIO}–{int(df.year.max())} ({len(df):,} filas país-año)")

    dup = df.duplicated(["iso_code", "year"]).sum()
    registrar("Duplicados", f"{dup} filas duplicadas por (país, año)")
    df = df.drop_duplicates(["iso_code", "year"])

    sin_total = df["electricity_generation"].isna()
    registrar("Sin generación total",
              f"se eliminan {sin_total.sum():,} filas país-año sin dato de generación eléctrica")
    df = df.loc[~sin_total]

    cols_fuente = [f"{k}_electricity" for k in FUENTES]
    nulos_antes = int(df[cols_fuente].isna().sum().sum())
    suma = df[cols_fuente].sum(axis=1, min_count=1)
    dif_rel = (suma - df["electricity_generation"]).abs() / df["electricity_generation"].replace(0, np.nan)
    consistente = dif_rel.fillna(0) <= TOLERANCIA_SUMA
    # Si las fuentes informadas ya suman el total, una fuente sin dato significa "no generó": se imputa 0
    df.loc[consistente, cols_fuente] = df.loc[consistente, cols_fuente].fillna(0)
    nulos_despues = int(df[cols_fuente].isna().sum().sum())
    registrar("Nulos por fuente",
              f"{nulos_antes:,} valores nulos; se imputan a 0 {nulos_antes - nulos_despues:,} donde la suma "
              f"de fuentes ya cuadra con el total (±{TOLERANCIA_SUMA:.1%}); quedan {nulos_despues:,} nulos")
    registrar("Consistencia suma fuentes = total",
              f"{(~consistente).sum()} filas con diferencia > {TOLERANCIA_SUMA:.1%} (se marcan, no se eliminan)")
    df["suma_fuentes_consistente"] = consistente

    negativos = (df[cols_fuente] < 0).sum().sum()
    registrar("Valores negativos", f"{negativos} valores de generación negativos")
    return df


def construir_fact_generacion(df: pd.DataFrame) -> pd.DataFrame:
    largo = df.melt(id_vars=["iso_code", "year"], value_vars=[f"{k}_electricity" for k in FUENTES],
                    var_name="col", value_name="generacion_twh")
    largo["fuente_id"] = largo["col"].str.replace("_electricity", "", regex=False).map(lambda k: FUENTES[k][0])
    largo = largo.rename(columns={"iso_code": "iso3", "year": "anio"}).dropna(subset=["generacion_twh"])
    largo["generacion_twh"] = largo["generacion_twh"].round(4)
    registrar("Formato largo", f"fact_generacion: {len(largo):,} filas (país × año × fuente)")
    return largo[["iso3", "anio", "fuente_id", "generacion_twh"]].sort_values(["iso3", "anio", "fuente_id"])


def construir_fact_pais_anio(df: pd.DataFrame, co2: pd.DataFrame) -> pd.DataFrame:
    gen = df["electricity_generation"]
    renov = df[[f"{k}_electricity" for k, v in FUENTES.items() if v[2] == "Renovable"]].sum(axis=1, min_count=1)
    fosil = df[[f"{k}_electricity" for k, v in FUENTES.items() if v[2] == "Fósil"]].sum(axis=1, min_count=1)
    out = pd.DataFrame({
        "iso3": df["iso_code"],
        "anio": df["year"].astype(int),
        "poblacion": df["population"],
        "pib_usd_ppa": df["gdp"],
        "generacion_twh": gen,
        "demanda_twh": df["electricity_demand"],
        "generacion_per_capita_kwh": df["per_capita_electricity"],
        # Se recalculan las participaciones desde los TWh para que sean coherentes con fact_generacion
        "renovables_pct": (renov / gen * 100).where(gen > 0),
        "fosil_pct": (fosil / gen * 100).where(gen > 0),
        "nuclear_pct": (df["nuclear_electricity"] / gen * 100).where(gen > 0),
        "intensidad_carbono_g_kwh": df["carbon_intensity_elec"],
        "suma_fuentes_consistente": df["suma_fuentes_consistente"],
    })
    dif = (out["renovables_pct"] - df["renewables_share_elec"]).abs()
    registrar("Validación % renovable",
              f"diferencia máx. entre % recalculado y % publicado por OWID: {dif.max():.2f} pp "
              f"(mediana {dif.median():.3f} pp)")

    co2 = filtrar_paises(co2, "CO2")
    co2 = co2[co2.year >= ANIO_INICIO][["iso_code", "year", "co2", "co2_per_capita"]]
    co2 = co2.rename(columns={"iso_code": "iso3", "year": "anio", "co2": "co2_mt", "co2_per_capita": "co2_per_capita_t"})
    out = out.merge(co2, on=["iso3", "anio"], how="left", validate="one_to_one")
    registrar("Unión con CO2",
              f"{out.co2_mt.notna().mean():.1%} de las filas país-año tienen dato de CO2 tras el left join")

    # Años recientes con cobertura parcial: se marca para no comparar países con muestras distintas
    cobertura = out.groupby("anio")["iso3"].nunique()
    umbral = 0.9 * cobertura.max()
    anios_completos = cobertura[cobertura >= umbral].index
    out["anio_cobertura_completa"] = out["anio"].isin(anios_completos)
    incompletos = sorted(set(cobertura.index) - set(anios_completos))
    registrar("Cobertura por año",
              f"años con < 90% de los países informados (preliminares): {incompletos} "
              f"({', '.join(str(int(cobertura[a])) + ' países' for a in incompletos)})")

    num = out.select_dtypes("float").columns
    out[num] = out[num].round(4)
    fuera_rango = ((out["renovables_pct"] < 0) | (out["renovables_pct"] > 100.0001)).sum()
    registrar("Rango de porcentajes", f"{fuera_rango} filas con % renovable fuera de [0, 100]")
    return out.sort_values(["iso3", "anio"])


def construir_dim_fuente() -> pd.DataFrame:
    return pd.DataFrame(
        [{"fuente_id": v[0], "fuente": v[1], "categoria": v[2], "orden": v[3],
          "grupo_grafico": v[4], "color_hex": COLOR_GRUPO[v[4]]} for v in FUENTES.values()]
    )


def escribir_reporte() -> None:
    DIR_OUT.mkdir(exist_ok=True)
    texto = (
        "# Reporte de calidad de datos\n\n"
        "Generado automáticamente por `src/02_limpieza.py`. Cada fila es una decisión de limpieza y su impacto.\n\n"
        "| Paso | Detalle |\n|---|---|\n" + "\n".join(log_calidad) + "\n"
    )
    (DIR_OUT / "reporte_calidad.md").write_text(texto, encoding="utf-8")


def main() -> None:
    DIR_PROC.mkdir(parents=True, exist_ok=True)
    energia, co2 = cargar_crudos()
    energia = filtrar_paises(energia, "energía")
    energia = limpiar_energia(energia)

    dim_pais = construir_dim_pais(sorted(energia["iso_code"].unique()))
    dim_fuente = construir_dim_fuente()
    fact_gen = construir_fact_generacion(energia)
    fact_pa = construir_fact_pais_anio(energia, co2)

    for nombre, tabla in {"dim_pais": dim_pais, "dim_fuente": dim_fuente,
                          "fact_generacion": fact_gen, "fact_pais_anio": fact_pa}.items():
        ruta = DIR_PROC / f"{nombre}.csv"
        tabla.to_csv(ruta, index=False, encoding="utf-8")
        print(f"[ok] {ruta.relative_to(RAIZ)}: {len(tabla):,} filas")
    escribir_reporte()


if __name__ == "__main__":
    main()
