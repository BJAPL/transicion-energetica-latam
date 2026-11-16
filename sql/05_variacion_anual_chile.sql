-- =====================================================================
-- P5. ¿Cuánto cambia año a año la generación solar de Chile y su participación
--     renovable? ¿En qué años se aceleró la transición?
-- Técnicas: funciones de ventana LAG(), crecimiento porcentual, CASE
-- =====================================================================
WITH chile AS (
    SELECT
        pa.anio,
        pa.renovables_pct,
        g.generacion_twh AS solar_twh,
        pa.anio_cobertura_completa
    FROM fact_pais_anio pa
    JOIN fact_generacion g ON g.iso3 = pa.iso3 AND g.anio = pa.anio AND g.fuente_id = 'solar'
    WHERE pa.iso3 = 'CHL'
)
SELECT
    anio,
    ROUND(solar_twh, 2)                                                       AS solar_twh,
    ROUND(solar_twh - LAG(solar_twh) OVER (ORDER BY anio), 2)                 AS var_solar_twh,
    ROUND(100.0 * (solar_twh - LAG(solar_twh) OVER (ORDER BY anio))
          / NULLIF(LAG(solar_twh) OVER (ORDER BY anio), 0), 1)                AS var_solar_pct,
    ROUND(renovables_pct, 1)                                                  AS renovables_pct,
    ROUND(renovables_pct - LAG(renovables_pct) OVER (ORDER BY anio), 1)       AS var_renovables_pp,
    CASE WHEN anio_cobertura_completa = 0 THEN 'preliminar' ELSE '' END       AS nota
FROM chile
WHERE anio >= 2010
ORDER BY anio;
