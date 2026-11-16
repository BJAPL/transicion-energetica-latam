# Reporte de calidad de datos

Generado automáticamente por `src/02_limpieza.py`. Cada fila es una decisión de limpieza y su impacto.

| Paso | Detalle |
|---|---|
| Carga | energía: 23,377 filas × 130 columnas; CO2: 56,269 filas × 79 columnas |
| Filtrar agregados (energía) | se excluyen 94 entidades que no son países (regiones, grupos, 'World'); quedan 220 países |
| Periodo | se conserva 2000–2025 (5,549 filas país-año) |
| Duplicados | 0 filas duplicadas por (país, año) |
| Sin generación total | se eliminan 162 filas país-año sin dato de generación eléctrica |
| Nulos por fuente | 1,460 valores nulos; se imputan a 0 1,460 donde la suma de fuentes ya cuadra con el total (±0.5%); quedan 0 nulos |
| Consistencia suma fuentes = total | 0 filas con diferencia > 0.5% (se marcan, no se eliminan) |
| Valores negativos | 0 valores de generación negativos |
| Dimensión país | 214 países; 44 de América Latina y el Caribe |
| Formato largo | fact_generacion: 48,483 filas (país × año × fuente) |
| Validación % renovable | diferencia máx. entre % recalculado y % publicado por OWID: 0.00 pp (mediana 0.000 pp) |
| Filtrar agregados (CO2) | se excluyen 36 entidades que no son países (regiones, grupos, 'World'); quedan 223 países |
| Unión con CO2 | 96.6% de las filas país-año tienen dato de CO2 tras el left join |
| Cobertura por año | años con < 90% de los países informados (preliminares): [2025] (90 países) |
| Rango de porcentajes | 0 filas con % renovable fuera de [0, 100] |
