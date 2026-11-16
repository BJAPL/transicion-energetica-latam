-- =====================================================================
-- P7. ¿Los países con más generación renovable tienen una electricidad menos
--     intensiva en carbono? ¿Cuál es la intensidad media por tramo de renovables?
-- Técnicas: segmentación con CASE, agregación por tramo, promedio ponderado
-- =====================================================================
WITH anio_ref AS (
    SELECT MAX(anio) AS anio FROM fact_pais_anio WHERE anio_cobertura_completa = 1
),
tramos AS (
    SELECT
        pa.*,
        CASE
            WHEN renovables_pct < 20 THEN '1. 0–20 %'
            WHEN renovables_pct < 40 THEN '2. 20–40 %'
            WHEN renovables_pct < 60 THEN '3. 40–60 %'
            WHEN renovables_pct < 80 THEN '4. 60–80 %'
            ELSE                          '5. 80–100 %'
        END AS tramo_renovables
    FROM fact_pais_anio pa
    JOIN anio_ref r ON pa.anio = r.anio
    WHERE pa.generacion_twh >= 1
      AND pa.intensidad_carbono_g_kwh IS NOT NULL
)
SELECT
    tramo_renovables,
    COUNT(*)                                                                    AS n_paises,
    ROUND(AVG(intensidad_carbono_g_kwh), 0)                                     AS intensidad_promedio_simple,
    ROUND(SUM(intensidad_carbono_g_kwh * generacion_twh) / SUM(generacion_twh), 0) AS intensidad_promedio_ponderada,
    ROUND(AVG(co2_per_capita_t), 2)                                             AS co2_per_capita_promedio_t,
    GROUP_CONCAT(CASE WHEN iso3 IN ('CHL', 'BRA', 'MEX', 'ARG', 'COL', 'PER', 'URY') THEN iso3 END) AS latam_destacados
FROM tramos
GROUP BY tramo_renovables
ORDER BY tramo_renovables;
