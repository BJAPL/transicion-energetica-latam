# Resultados de las consultas SQL

Generado por `src/04_ejecutar_consultas.py`. Cada sección corresponde a un archivo de `sql/`.

## 01_mix_electrico_chile

**P1. ¿Cómo ha cambiado la matriz eléctrica de Chile desde el año 2000?**

| anio | generacion_total_twh | fosil_twh | hidro_twh | solar_twh | eolica_twh | otras_renov_twh | renovables_pct | carbon_pct |
|---|---|---|---|---|---|---|---|---|
| 2000 | 41.1 | 20.6 | 19.6 | 0.0 | 0.0 | 0.9 | 49.8 | 20.6 |
| 2001 | 42.3 | 19.4 | 20.8 | 0.0 | 0.0 | 2.1 | 54.0 | 11.4 |
| 2002 | 43.4 | 19.4 | 22.0 | 0.0 | 0.0 | 1.9 | 55.2 | 11.6 |
| 2003 | 46.6 | 23.3 | 21.5 | 0.0 | 0.0 | 1.8 | 49.9 | 10.5 |
| 2004 | 51.0 | 27.2 | 21.8 | 0.0 | 0.0 | 2.0 | 46.7 | 15.1 |
| 2005 | 52.2 | 24.2 | 26.2 | 0.0 | 0.0 | 1.8 | 53.7 | 13.8 |
| 2006 | 55.0 | 24.8 | 28.8 | 0.0 | 0.0 | 1.4 | 55.0 | 19.3 |
| 2007 | 58.3 | 32.7 | 22.9 | 0.0 | 0.0 | 2.7 | 43.9 | 22.8 |
| 2008 | 59.5 | 32.4 | 23.9 | 0.0 | 0.0 | 3.1 | 45.5 | 23.7 |
| 2009 | 60.4 | 31.0 | 25.0 | 0.0 | 0.1 | 4.3 | 48.7 | 24.7 |
| 2010 | 60.3 | 36.0 | 21.6 | 0.0 | 0.3 | 2.3 | 40.2 | 28.0 |
| 2011 | 65.7 | 39.7 | 20.9 | 0.0 | 0.3 | 4.7 | 39.5 | 29.9 |
| 2012 | 69.6 | 44.3 | 20.0 | 0.0 | 0.4 | 4.8 | 36.3 | 36.4 |
| 2013 | 72.8 | 46.8 | 19.7 | 0.0 | 0.6 | 5.8 | 35.7 | 41.5 |
| 2014 | 70.2 | 40.1 | 22.8 | 0.5 | 1.4 | 5.3 | 42.8 | 37.1 |
| 2015 | 74.9 | 42.5 | 23.4 | 1.2 | 2.1 | 5.6 | 43.2 | 37.4 |
| 2016 | 78.8 | 45.0 | 22.8 | 2.6 | 2.5 | 6.0 | 42.9 | 38.4 |
| 2017 | 78.9 | 44.6 | 20.9 | 3.8 | 3.5 | 6.1 | 43.5 | 37.1 |
| 2018 | 81.8 | 44.3 | 22.9 | 5.1 | 3.6 | 5.9 | 45.9 | 36.6 |
| 2019 | 84.0 | 45.2 | 22.0 | 6.3 | 4.9 | 5.6 | 46.2 | 33.5 |
| 2020 | 83.6 | 43.1 | 21.9 | 7.5 | 5.5 | 5.5 | 48.4 | 31.2 |
| 2021 | 88.1 | 45.0 | 19.0 | 10.6 | 7.6 | 5.9 | 48.9 | 29.6 |
| 2022 | 91.0 | 40.7 | 20.7 | 15.7 | 8.9 | 5.1 | 55.3 | 23.6 |
| 2023 | 89.2 | 32.9 | 23.3 | 17.9 | 9.5 | 5.6 | 63.1 | 16.3 |
| 2024 | 88.6 | 26.6 | 26.0 | 20.2 | 10.4 | 5.5 | 70.0 | 15.3 |
| 2025 | 88.5 | 29.8 | 19.7 | 22.2 | 11.6 | 5.3 | 66.4 | 17.8 |

## 02_ranking_latam_renovables

**P2. ¿Dónde se ubica Chile entre los países de América Latina y el Caribe según la participación renovable en su generación eléctrica?**

| ranking | pais | subregion | generacion_twh | renovables_pct | renovables_pct_2015 | cambio_pp_vs_2015 | anio_referencia |
|---|---|---|---|---|---|---|---|
| 1 | Paraguay | Sudamérica | 42.4 | 100.0 | 100.0 | 0.0 | 2024 |
| 2 | Costa Rica | Centroamérica y México | 11.0 | 99.9 | 99.0 | 0.9 | 2024 |
| 3 | Uruguay | Sudamérica | 13.4 | 98.9 | 93.2 | 5.7 | 2024 |
| 4 | Venezuela | Sudamérica | 80.1 | 91.1 | 58.8 | 32.3 | 2024 |
| 5 | El Salvador | Centroamérica y México | 6.5 | 90.8 | 58.3 | 32.5 | 2024 |
| 6 | Brasil | Sudamérica | 745.7 | 87.3 | 74.2 | 13.1 | 2024 |
| 7 | Ecuador | Sudamérica | 32.7 | 72.4 | 51.1 | 21.3 | 2024 |
| 8 | Chile | Sudamérica | 88.6 | 70.0 | 43.2 | 26.8 | 2024 |
| 9 | Guatemala | Centroamérica y México | 15.8 | 68.3 | 61.1 | 7.2 | 2024 |
| 10 | Panamá | Centroamérica y México | 13.4 | 68.0 | 65.3 | 2.6 | 2024 |
| 11 | Nicaragua | Centroamérica y México | 4.5 | 62.4 | 50.1 | 12.3 | 2024 |
| 12 | Colombia | Sudamérica | 89.1 | 61.3 | 63.3 | -2.0 | 2024 |
| 13 | Perú | Sudamérica | 59.3 | 60.1 | 52.7 | 7.4 | 2024 |
| 14 | Honduras | Centroamérica y México | 12.5 | 55.4 | 44.1 | 11.4 | 2024 |
| 15 | Surinam | Sudamérica | 1.7 | 52.9 | 26.3 | 26.5 | 2024 |
| 16 | Argentina | Sudamérica | 152.5 | 34.4 | 23.7 | 10.7 | 2024 |
| 17 | Bolivia | Sudamérica | 13.5 | 34.0 | 29.4 | 4.6 | 2024 |
| 18 | México | Centroamérica y México | 355.2 | 21.1 | 15.5 | 5.6 | 2024 |
| 19 | República Dominicana | Caribe | 24.0 | 18.9 | 7.9 | 11.0 | 2024 |
| 20 | Aruba | Caribe | 1.0 | 17.0 | 18.6 | -1.6 | 2024 |
| 21 | Jamaica | Caribe | 4.9 | 12.6 | 10.3 | 2.3 | 2024 |
| 22 | Barbados | Caribe | 1.1 | 9.0 | 1.0 | 8.0 | 2024 |
| 23 | Puerto Rico | Caribe | 20.0 | 6.0 | 1.8 | 4.2 | 2024 |
| 24 | Cuba | Caribe | 19.4 | 4.0 | 4.4 | -0.4 | 2024 |
| 25 | Guyana | Sudamérica | 1.4 | 2.9 | 4.0 | -1.1 | 2024 |
| 26 | Bahamas | Caribe | 2.3 | 0.9 | 0.0 | 0.9 | 2024 |
| 27 | Trinidad y Tobago | Caribe | 9.6 | 0.1 | 0.1 | 0.0 | 2024 |

## 03_crecimiento_solar_eolica

**P3. ¿Qué países latinoamericanos aumentaron más su generación solar + eólica entre 2015 y el último año completo?**

| pais | solar_eolica_twh_2015 | solar_eolica_twh_actual | aumento_twh | participacion_pct_2015 | participacion_pct_actual | aumento_pp |
|---|---|---|---|---|---|---|
| Chile | 3.35 | 30.62 | 27.27 | 4.5 | 34.6 | 30.1 |
| Uruguay | 2.12 | 5.72 | 3.6 | 15.4 | 42.8 | 27.4 |
| El Salvador | 0.01 | 1.39 | 1.38 | 0.2 | 21.3 | 21.1 |
| Brasil | 21.69 | 179.81 | 158.12 | 3.7 | 24.1 | 20.4 |
| Argentina | 0.6 | 20.14 | 19.54 | 0.4 | 13.2 | 12.8 |
| Panamá | 0.44 | 1.95 | 1.51 | 4.3 | 14.5 | 10.2 |
| República Dominicana | 0.32 | 2.85 | 2.53 | 1.8 | 11.9 | 10.1 |
| México | 8.95 | 45.47 | 36.52 | 2.9 | 12.8 | 9.9 |
| Barbados | 0.01 | 0.1 | 0.09 | 1.0 | 9.0 | 8.0 |
| Bolivia | 0.01 | 0.88 | 0.87 | 0.1 | 6.5 | 6.4 |

## 04_chile_vs_latam_vs_mundo

**P4. ¿Cómo evoluciona la participación renovable de Chile frente al promedio de América Latina y el Caribe y al promedio mundial?**

| anio | chile_pct | latam_pct | mundo_pct |
|---|---|---|---|
| 2000 | 49.8 | 60.1 | 18.7 |
| 2001 | 54.0 | 56.7 | 18.0 |
| 2002 | 55.2 | 57.2 | 17.9 |
| 2003 | 49.9 | 56.6 | 17.4 |
| 2004 | 46.7 | 56.5 | 18.0 |
| 2005 | 53.7 | 57.4 | 18.1 |
| 2006 | 55.0 | 57.5 | 18.2 |
| 2007 | 43.9 | 57.0 | 18.0 |
| 2008 | 45.5 | 56.6 | 18.9 |
| 2009 | 48.7 | 57.2 | 19.5 |
| 2010 | 40.2 | 56.2 | 19.7 |
| 2011 | 39.5 | 57.2 | 20.0 |
| 2012 | 36.3 | 54.4 | 21.0 |
| 2013 | 35.7 | 52.1 | 21.7 |
| 2014 | 42.8 | 51.3 | 22.3 |
| 2015 | 43.2 | 50.9 | 23.0 |
| 2016 | 42.9 | 52.6 | 23.7 |
| 2017 | 43.5 | 54.2 | 24.5 |
| 2018 | 45.9 | 55.2 | 25.1 |
| 2019 | 46.2 | 55.1 | 26.1 |
| 2020 | 48.4 | 58.3 | 28.0 |
| 2021 | 48.9 | 57.5 | 28.1 |
| 2022 | 55.3 | 62.1 | 29.5 |
| 2023 | 63.1 | 62.4 | 30.4 |
| 2024 | 70.0 | 62.7 | 32.0 |

## 05_variacion_anual_chile

**P5. ¿Cuánto cambia año a año la generación solar de Chile y su participación renovable? ¿En qué años se aceleró la transición?**

| anio | solar_twh | var_solar_twh | var_solar_pct | renovables_pct | var_renovables_pp | nota |
|---|---|---|---|---|---|---|
| 2010 | 0.0 |  |  | 40.2 |  |  |
| 2011 | 0.0 | 0.0 |  | 39.5 | -0.7 |  |
| 2012 | 0.0 | 0.0 |  | 36.3 | -3.2 |  |
| 2013 | 0.01 | 0.01 |  | 35.7 | -0.6 |  |
| 2014 | 0.48 | 0.47 | 4700.0 | 42.8 | 7.1 |  |
| 2015 | 1.24 | 0.76 | 158.3 | 43.2 | 0.4 |  |
| 2016 | 2.59 | 1.35 | 108.9 | 42.9 | -0.3 |  |
| 2017 | 3.84 | 1.25 | 48.3 | 43.5 | 0.7 |  |
| 2018 | 5.12 | 1.28 | 33.3 | 45.9 | 2.3 |  |
| 2019 | 6.3 | 1.18 | 23.0 | 46.2 | 0.3 |  |
| 2020 | 7.53 | 1.23 | 19.5 | 48.4 | 2.2 |  |
| 2021 | 10.56 | 3.03 | 40.2 | 48.9 | 0.4 |  |
| 2022 | 15.71 | 5.15 | 48.8 | 55.3 | 6.4 |  |
| 2023 | 17.94 | 2.23 | 14.2 | 63.1 | 7.8 |  |
| 2024 | 20.19 | 2.25 | 12.5 | 70.0 | 6.9 |  |
| 2025 | 22.18 | 1.99 | 9.9 | 66.4 | -3.7 | preliminar |

## 06_salida_del_carbon

**P6. ¿Qué países (de cualquier región, con sistemas de al menos 10 TWh) redujeron más la participación del carbón entre 2015 y el último año completo?**

| pais | region | carbon_pct_2015 | carbon_pct_actual | cambio_pp |
|---|---|---|---|---|
| Grecia | Europa | 43.3 | 5.7 | -37.6 |
| Hong Kong | Asia | 65.7 | 33.7 | -32.1 |
| Israel | Asia | 45.4 | 14.3 | -31.1 |
| Países Bajos | Europa | 36.1 | 6.1 | -30.0 |
| Portugal | Europa | 28.8 | 0.0 | -28.8 |
| Polonia | Europa | 79.4 | 54.3 | -25.1 |
| Bulgaria | Europa | 46.3 | 22.9 | -23.4 |
| Chile | América Latina y el Caribe | 37.4 | 15.3 | -22.1 |
| Reino Unido | Europa | 22.4 | 0.7 | -21.7 |
| Alemania | Europa | 42.6 | 21.4 | -21.1 |
| Dinamarca | Europa | 24.7 | 5.0 | -19.7 |
| Australia | Oceanía | 63.9 | 45.2 | -18.7 |
| Estados Unidos | Norteamérica | 33.1 | 14.9 | -18.3 |
| España | Europa | 18.5 | 0.9 | -17.6 |
| Kazajistán | Asia | 70.6 | 54.0 | -16.6 |

## 07_renovables_vs_intensidad_carbono

**P7. ¿Los países con más generación renovable tienen una electricidad menos intensiva en carbono? ¿Cuál es la intensidad media por tramo de renovables?**

| tramo_renovables | n_paises | intensidad_promedio_simple | intensidad_promedio_ponderada | co2_per_capita_promedio_t | latam_destacados |
|---|---|---|---|---|---|
| 1. 0–20 % | 51 | 644.0 | 614.0 | 7.94 |  |
| 2. 20–40 % | 33 | 455.0 | 485.0 | 4.27 | ARG,MEX |
| 3. 40–60 % | 23 | 338.0 | 318.0 | 3.89 |  |
| 4. 60–80 % | 20 | 207.0 | 180.0 | 2.8 | CHL,COL,PER |
| 5. 80–100 % | 27 | 74.0 | 89.0 | 2.7 | BRA,URY |

## 08_anio_supera_50_renovable

**P8. ¿Desde qué año cada país de América Latina se mantiene sobre el 50 % de generación renovable sin interrupciones?**

| pais | renovables_pct_actual | sobre_50_sin_interrupcion_desde | anios_sobre_50 |
|---|---|---|---|
| Paraguay | 100.0 | 2000 o antes | 25 de 25 |
| Costa Rica | 99.9 | 2000 o antes | 25 de 25 |
| Uruguay | 98.9 | 2000 o antes | 25 de 25 |
| Venezuela | 91.1 | 2000 o antes | 25 de 25 |
| El Salvador | 90.8 | 2000 o antes | 25 de 25 |
| Brasil | 87.3 | 2000 o antes | 25 de 25 |
| Colombia | 61.3 | 2000 o antes | 25 de 25 |
| Perú | 60.1 | 2000 o antes | 25 de 25 |
| Panamá | 68.0 | 2002 | 24 de 25 |
| Guatemala | 68.3 | 2010 | 21 de 25 |
| Ecuador | 72.4 | 2015 | 22 de 25 |
| Honduras | 55.4 | 2017 | 9 de 25 |
| Chile | 70.0 | 2022 | 7 de 25 |
| Argentina | 34.4 | Bajo 50 % hoy | 0 de 25 |
| Bolivia | 34.0 | Bajo 50 % hoy | 3 de 25 |
| México | 21.1 | Bajo 50 % hoy | 0 de 25 |
| República Dominicana | 18.9 | Bajo 50 % hoy | 0 de 25 |
| Puerto Rico | 6.0 | Bajo 50 % hoy | 0 de 25 |
| Cuba | 4.0 | Bajo 50 % hoy | 0 de 25 |
| Trinidad y Tobago | 0.1 | Bajo 50 % hoy | 0 de 25 |

## 09_participacion_chile_solar_latam

**P9. ¿Qué porcentaje de toda la generación solar de América Latina y el Caribe produce Chile cada año, y qué lugar ocupa en la región?**

| anio | chile_solar_twh | latam_solar_twh | participacion_chile_pct | ranking_regional |
|---|---|---|---|---|
| 2012 | 0.0 | 0.41 | 0.0 | 11 |
| 2013 | 0.01 | 0.75 | 1.3 | 10 |
| 2014 | 0.48 | 1.46 | 32.9 | 1 |
| 2015 | 1.24 | 3.06 | 40.5 | 1 |
| 2016 | 2.59 | 5.23 | 49.5 | 1 |
| 2017 | 3.84 | 8.75 | 43.9 | 1 |
| 2018 | 5.12 | 16.14 | 31.7 | 1 |
| 2019 | 6.3 | 29.18 | 21.6 | 3 |
| 2020 | 7.53 | 41.98 | 17.9 | 3 |
| 2021 | 10.56 | 57.84 | 18.3 | 3 |
| 2022 | 15.71 | 77.73 | 20.2 | 3 |
| 2023 | 17.94 | 104.83 | 17.1 | 3 |
| 2024 | 20.19 | 133.6 | 15.1 | 3 |
