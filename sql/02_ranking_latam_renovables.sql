-- =====================================================================
-- P2. ¿Dónde se ubica Chile entre los países de América Latina y el Caribe
--     según la participación renovable en su generación eléctrica?
-- Técnicas: CTE, subconsulta para el año de referencia, RANK(), self-join
-- Se excluyen sistemas muy pequeños (< 1 TWh/año) para que el ranking sea comparable.
-- =====================================================================
WITH anio_ref AS (
    -- Último año con cobertura completa (los años recientes son preliminares)
    SELECT MAX(anio) AS anio FROM fact_pais_anio WHERE anio_cobertura_completa = 1
),
actual AS (
    SELECT pa.iso3, pa.renovables_pct, pa.generacion_twh
    FROM fact_pais_anio pa
    JOIN anio_ref r ON pa.anio = r.anio
),
base AS (
    SELECT iso3, renovables_pct AS renovables_pct_2015
    FROM fact_pais_anio
    WHERE anio = 2015
)
SELECT
    RANK() OVER (ORDER BY a.renovables_pct DESC)          AS ranking,
    p.pais,
    p.subregion,
    ROUND(a.generacion_twh, 1)                             AS generacion_twh,
    ROUND(a.renovables_pct, 1)                             AS renovables_pct,
    ROUND(b.renovables_pct_2015, 1)                        AS renovables_pct_2015,
    ROUND(a.renovables_pct - b.renovables_pct_2015, 1)     AS cambio_pp_vs_2015,
    (SELECT anio FROM anio_ref)                            AS anio_referencia
FROM actual a
JOIN dim_pais p USING (iso3)
LEFT JOIN base b USING (iso3)
WHERE p.es_latam = 1
  AND a.generacion_twh >= 1
ORDER BY ranking;
