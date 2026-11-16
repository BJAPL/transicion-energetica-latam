-- =====================================================================
-- P6. ¿Qué países (de cualquier región, con sistemas de al menos 10 TWh)
--     redujeron más la participación del carbón entre 2015 y el último año completo?
-- Técnicas: CTE, self-join entre años, filtro HAVING-like, ORDER BY + LIMIT
-- =====================================================================
WITH anio_ref AS (
    SELECT MAX(anio) AS anio FROM fact_pais_anio WHERE anio_cobertura_completa = 1
),
carbon AS (
    SELECT
        g.iso3,
        g.anio,
        100.0 * SUM(CASE WHEN g.fuente_id = 'carbon' THEN g.generacion_twh ELSE 0 END)
              / SUM(g.generacion_twh) AS carbon_pct,
        SUM(g.generacion_twh) AS total_twh
    FROM fact_generacion g
    WHERE g.anio IN (2015, (SELECT anio FROM anio_ref))
    GROUP BY g.iso3, g.anio
)
SELECT
    p.pais,
    p.region,
    ROUND(ini.carbon_pct, 1)                    AS carbon_pct_2015,
    ROUND(fin.carbon_pct, 1)                    AS carbon_pct_actual,
    ROUND(fin.carbon_pct - ini.carbon_pct, 1)   AS cambio_pp
FROM carbon ini
JOIN carbon fin ON fin.iso3 = ini.iso3 AND fin.anio = (SELECT anio FROM anio_ref)
JOIN dim_pais p ON p.iso3 = ini.iso3
WHERE ini.anio = 2015
  AND fin.total_twh >= 10
  AND ini.carbon_pct >= 10   -- solo países donde el carbón era relevante
ORDER BY cambio_pp ASC
LIMIT 15;
