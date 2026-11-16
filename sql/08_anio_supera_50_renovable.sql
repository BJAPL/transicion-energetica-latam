-- =====================================================================
-- P8. ¿Desde qué año cada país de América Latina se mantiene sobre el 50 %
--     de generación renovable sin interrupciones?
-- Técnicas: subconsulta correlacionada (último año bajo el umbral), COALESCE,
--           conteo condicional; es una versión simple del problema "gaps and islands"
-- =====================================================================
WITH anio_ref AS (
    SELECT MAX(anio) AS anio FROM fact_pais_anio WHERE anio_cobertura_completa = 1
),
resumen AS (
    SELECT
        pa.iso3,
        MAX(CASE WHEN pa.renovables_pct < 50 THEN pa.anio END) AS ultimo_anio_bajo_50,
        SUM(CASE WHEN pa.renovables_pct >= 50 THEN 1 ELSE 0 END) AS anios_sobre_50,
        COUNT(*) AS anios_con_datos
    FROM fact_pais_anio pa
    WHERE pa.anio <= (SELECT anio FROM anio_ref)
    GROUP BY pa.iso3
)
SELECT
    p.pais,
    ROUND(pa.renovables_pct, 1) AS renovables_pct_actual,
    CASE
        WHEN pa.renovables_pct < 50          THEN 'Bajo 50 % hoy'
        WHEN r.ultimo_anio_bajo_50 IS NULL   THEN '2000 o antes'
        ELSE CAST(r.ultimo_anio_bajo_50 + 1 AS TEXT)
    END AS sobre_50_sin_interrupcion_desde,
    r.anios_sobre_50 || ' de ' || r.anios_con_datos AS anios_sobre_50
FROM dim_pais p
JOIN fact_pais_anio pa ON pa.iso3 = p.iso3 AND pa.anio = (SELECT anio FROM anio_ref)
JOIN resumen r ON r.iso3 = p.iso3
WHERE p.es_latam = 1
  AND pa.generacion_twh >= 5
ORDER BY pa.renovables_pct < 50, COALESCE(r.ultimo_anio_bajo_50, 1999), pa.renovables_pct DESC;
