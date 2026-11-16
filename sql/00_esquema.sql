-- =====================================================================
-- Esquema en estrella para el análisis de transición energética
-- Motor: SQLite (compatible en su mayoría con PostgreSQL)
-- =====================================================================

DROP TABLE IF EXISTS fact_generacion;
DROP TABLE IF EXISTS fact_pais_anio;
DROP TABLE IF EXISTS dim_fuente;
DROP TABLE IF EXISTS dim_pais;

CREATE TABLE dim_pais (
    iso3        TEXT PRIMARY KEY,
    pais        TEXT NOT NULL,
    pais_en     TEXT,
    region      TEXT NOT NULL,
    subregion   TEXT NOT NULL,
    es_latam    INTEGER NOT NULL CHECK (es_latam IN (0, 1))
);

CREATE TABLE dim_fuente (
    fuente_id   TEXT PRIMARY KEY,
    fuente      TEXT NOT NULL,
    categoria   TEXT NOT NULL CHECK (categoria IN ('Renovable', 'Fósil', 'Nuclear')),
    orden       INTEGER,
    grupo_grafico TEXT,
    color_hex   TEXT
);

CREATE TABLE fact_generacion (
    iso3            TEXT    NOT NULL REFERENCES dim_pais (iso3),
    anio            INTEGER NOT NULL,
    fuente_id       TEXT    NOT NULL REFERENCES dim_fuente (fuente_id),
    generacion_twh  REAL    NOT NULL CHECK (generacion_twh >= 0),
    PRIMARY KEY (iso3, anio, fuente_id)
);

CREATE TABLE fact_pais_anio (
    iso3                        TEXT    NOT NULL REFERENCES dim_pais (iso3),
    anio                        INTEGER NOT NULL,
    poblacion                   REAL,
    pib_usd_ppa                 REAL,
    generacion_twh              REAL,
    demanda_twh                 REAL,
    generacion_per_capita_kwh   REAL,
    renovables_pct              REAL,
    fosil_pct                   REAL,
    nuclear_pct                 REAL,
    intensidad_carbono_g_kwh    REAL,
    suma_fuentes_consistente    INTEGER,
    co2_mt                      REAL,
    co2_per_capita_t            REAL,
    anio_cobertura_completa     INTEGER,
    PRIMARY KEY (iso3, anio)
);

CREATE INDEX idx_gen_anio   ON fact_generacion (anio);
CREATE INDEX idx_pa_anio    ON fact_pais_anio (anio);
