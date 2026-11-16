-- =====================================================================
-- P9. ¿Qué porcentaje de toda la generación solar de América Latina y el Caribe
--     produce Chile cada año, y qué lugar ocupa en la región?
-- Técnicas: funciones de ventana SUM() OVER (PARTITION BY) y RANK() OVER (PARTITION BY)
-- =====================================================================
WITH solar_latam AS (
    SELECT
        g.anio,
        g.iso3,
        g.generacion_twh                                                      AS solar_twh,
        SUM(g.generacion_twh) OVER (PARTITION BY g.anio)                      AS solar_latam_twh,
        RANK() OVER (PARTITION BY g.anio ORDER BY g.generacion_twh DESC)      AS ranking_regional
    FROM fact_generacion g
    JOIN dim_pais p USING (iso3)
    JOIN fact_pais_anio pa USING (iso3, anio)
    WHERE g.fuente_id = 'solar'
      AND p.es_latam = 1
      AND pa.anio_cobertura_completa = 1
)
SELECT
    anio,
    ROUND(solar_twh, 2)                                AS chile_solar_twh,
    ROUND(solar_latam_twh, 2)                          AS latam_solar_twh,
    ROUND(100.0 * solar_twh / NULLIF(solar_latam_twh, 0), 1) AS participacion_chile_pct,
    ranking_regional
FROM solar_latam
WHERE iso3 = 'CHL'
  AND anio >= 2012
ORDER BY anio;
