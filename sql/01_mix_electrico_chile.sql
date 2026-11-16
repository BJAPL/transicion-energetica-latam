-- =====================================================================
-- P1. ¿Cómo ha cambiado la matriz eléctrica de Chile desde el año 2000?
-- Técnicas: JOIN, agregación condicional (pivot con CASE), redondeo
-- =====================================================================
SELECT
    g.anio,
    ROUND(SUM(g.generacion_twh), 1)                                                   AS generacion_total_twh,
    ROUND(SUM(CASE WHEN f.categoria = 'Fósil'     THEN g.generacion_twh END), 1)      AS fosil_twh,
    ROUND(SUM(CASE WHEN f.fuente_id = 'hidro'     THEN g.generacion_twh END), 1)      AS hidro_twh,
    ROUND(SUM(CASE WHEN f.fuente_id = 'solar'     THEN g.generacion_twh END), 1)      AS solar_twh,
    ROUND(SUM(CASE WHEN f.fuente_id = 'eolica'    THEN g.generacion_twh END), 1)      AS eolica_twh,
    ROUND(SUM(CASE WHEN f.fuente_id IN ('bioenergia', 'otras_renov') THEN g.generacion_twh END), 1) AS otras_renov_twh,
    ROUND(100.0 * SUM(CASE WHEN f.categoria = 'Renovable' THEN g.generacion_twh END)
                / SUM(g.generacion_twh), 1)                                           AS renovables_pct,
    ROUND(100.0 * SUM(CASE WHEN f.fuente_id = 'carbon' THEN g.generacion_twh END)
                / SUM(g.generacion_twh), 1)                                           AS carbon_pct
FROM fact_generacion g
JOIN dim_fuente f USING (fuente_id)
WHERE g.iso3 = 'CHL'
GROUP BY g.anio
ORDER BY g.anio;
