-- =====================================================================
-- P3. ¿Qué países latinoamericanos aumentaron más su generación solar + eólica
--     entre 2015 y el último año completo?
-- Técnicas: CTE, agregación filtrada, comparación entre dos años, NULLIF
-- =====================================================================
WITH anio_ref AS (
    SELECT MAX(anio) AS anio FROM fact_pais_anio WHERE anio_cobertura_completa = 1
),
vre AS (  -- vre = energías renovables variables (solar + eólica)
    SELECT
        g.iso3,
        g.anio,
        SUM(CASE WHEN g.fuente_id IN ('solar', 'eolica') THEN g.generacion_twh ELSE 0 END) AS vre_twh,
        SUM(g.generacion_twh) AS total_twh
    FROM fact_generacion g
    WHERE g.anio IN (2015, (SELECT anio FROM anio_ref))
    GROUP BY g.iso3, g.anio
)
SELECT
    p.pais,
    ROUND(ini.vre_twh, 2)                                      AS solar_eolica_twh_2015,
    ROUND(fin.vre_twh, 2)                                      AS solar_eolica_twh_actual,
    ROUND(fin.vre_twh - ini.vre_twh, 2)                        AS aumento_twh,
    ROUND(100.0 * ini.vre_twh / NULLIF(ini.total_twh, 0), 1)   AS participacion_pct_2015,
    ROUND(100.0 * fin.vre_twh / NULLIF(fin.total_twh, 0), 1)   AS participacion_pct_actual,
    ROUND(100.0 * fin.vre_twh / NULLIF(fin.total_twh, 0)
        - 100.0 * ini.vre_twh / NULLIF(ini.total_twh, 0), 1)   AS aumento_pp
FROM vre ini
JOIN vre fin ON fin.iso3 = ini.iso3 AND fin.anio = (SELECT anio FROM anio_ref)
JOIN dim_pais p ON p.iso3 = ini.iso3
WHERE ini.anio = 2015
  AND p.es_latam = 1
  AND fin.total_twh >= 1
ORDER BY aumento_pp DESC
LIMIT 10;
