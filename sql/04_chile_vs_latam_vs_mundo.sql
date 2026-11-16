-- =====================================================================
-- P4. ¿Cómo evoluciona la participación renovable de Chile frente al promedio
--     de América Latina y el Caribe y al promedio mundial?
-- Nota: los promedios regionales son PONDERADOS por generación
--       (suma de TWh renovables / suma de TWh totales), no un promedio simple
--       de porcentajes, que daría el mismo peso a Barbados que a Brasil.
-- Técnicas: CTE, agregación condicional, UNION ALL, pivot final
-- =====================================================================
WITH por_pais AS (
    SELECT
        g.iso3,
        g.anio,
        SUM(CASE WHEN f.categoria = 'Renovable' THEN g.generacion_twh ELSE 0 END) AS renov_twh,
        SUM(g.generacion_twh) AS total_twh
    FROM fact_generacion g
    JOIN dim_fuente f USING (fuente_id)
    JOIN fact_pais_anio pa USING (iso3, anio)
    WHERE pa.anio_cobertura_completa = 1
    GROUP BY g.iso3, g.anio
),
series AS (
    SELECT 'Chile' AS grupo, anio, SUM(renov_twh) AS renov, SUM(total_twh) AS total
    FROM por_pais WHERE iso3 = 'CHL' GROUP BY anio
    UNION ALL
    SELECT 'América Latina y el Caribe', pp.anio, SUM(renov_twh), SUM(total_twh)
    FROM por_pais pp JOIN dim_pais p USING (iso3) WHERE p.es_latam = 1 GROUP BY pp.anio
    UNION ALL
    SELECT 'Mundo', anio, SUM(renov_twh), SUM(total_twh)
    FROM por_pais GROUP BY anio
)
SELECT
    anio,
    ROUND(100.0 * MAX(CASE WHEN grupo = 'Chile' THEN renov / total END), 1)                       AS chile_pct,
    ROUND(100.0 * MAX(CASE WHEN grupo = 'América Latina y el Caribe' THEN renov / total END), 1)  AS latam_pct,
    ROUND(100.0 * MAX(CASE WHEN grupo = 'Mundo' THEN renov / total END), 1)                       AS mundo_pct
FROM series
GROUP BY anio
ORDER BY anio;
