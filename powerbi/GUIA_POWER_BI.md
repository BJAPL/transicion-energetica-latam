# Guía para construir el dashboard en Power BI

Esta guía arma el dashboard paso a paso a partir de los CSV de `data/processed/`.
Toma unos 60–90 minutos. Al terminar, guarda el archivo como
`powerbi/transicion_energetica.pbix` y sube capturas a `docs/img/`.

> Requisito: **Power BI Desktop** (gratis, Windows). No necesitas ejecutar Python:
> los CSV procesados ya vienen en el repositorio.

---

## 1. Configuración regional (¡importante!)

Los CSV usan **punto como separador decimal** (`70.04`). Si tu Windows está en
español de Chile, Power BI podría leer `70.04` como `7004`.

**Archivo → Opciones y configuración → Opciones → Archivo actual → Configuración regional**
→ *Configuración regional para la importación* = **Inglés (Estados Unidos)**.

Hazlo **antes** de importar los datos.

## 2. Importar los datos

1. **Inicio → Obtener datos → Texto/CSV** y carga, uno por uno:
   `dim_pais.csv`, `dim_fuente.csv`, `fact_generacion.csv`, `fact_pais_anio.csv`.
2. En cada uno, haz clic en **Transformar datos** (Power Query) y revisa los tipos:

| Tabla | Columna | Tipo |
|---|---|---|
| todas | `anio` | Número entero |
| `fact_*` | columnas numéricas (`generacion_twh`, `renovables_pct`, `co2_mt`…) | Número decimal |
| `dim_pais` | `es_latam` | Verdadero/Falso |
| `fact_pais_anio` | `anio_cobertura_completa`, `suma_fuentes_consistente` | Verdadero/Falso |
| `dim_fuente` | `orden` | Número entero |

3. **Cerrar y aplicar**.

> Comprueba la configuración regional: en la vista de tabla, Chile 2024 debe tener
> `renovables_pct = 70.04`, no `7004`.

## 3. Modelo de datos (esquema en estrella)

1. **Modelado → Nueva tabla** y pega la tabla `dim_anio` de `medidas.dax`.
2. En la **vista de modelo**, crea estas relaciones (todas *de uno a varios*, filtro en una dirección):

```
dim_pais[iso3]       1 ──► *  fact_generacion[iso3]
dim_pais[iso3]       1 ──► *  fact_pais_anio[iso3]
dim_fuente[fuente_id] 1 ──► * fact_generacion[fuente_id]
dim_anio[anio]       1 ──► *  fact_generacion[anio]
dim_anio[anio]       1 ──► *  fact_pais_anio[anio]
```

No relaciones directamente las dos tablas de hechos: se filtran a través de las dimensiones.

3. Ordena las columnas de texto para que los gráficos respeten el orden lógico:
   `dim_fuente[fuente]` → **Ordenar por columna** → `orden`.
4. Oculta en la vista de informe las columnas de llaves de las tablas de hechos (`iso3`, `anio`, `fuente_id`).
   Así los usuarios filtran siempre desde las dimensiones.

## 4. Medidas

1. **Inicio → Escribir datos** → nombre `_Medidas` → Cargar (tabla vacía para agrupar medidas).
2. Con `_Medidas` seleccionada, **Nueva medida** y pega cada medida de `medidas.dax`.
3. Formato:
   - Medidas `% …` → **Porcentaje**, 1 decimal.
   - Medidas `(pp)` → **Número decimal**, 1 decimal (son puntos porcentuales).
   - `Generación … TWh` → **Número decimal**, 1 decimal.

> Si al pegar aparece un error de sintaxis en las comas, tu configuración usa `;`
> como separador: reemplaza `,` por `;` entre argumentos.

## 5. Tema

**Vista → Temas → Examinar temas** → `powerbi/tema_transicion.json`.

Para que cada fuente tenga siempre el mismo color, en los gráficos por fuente usa
`dim_fuente[grupo_grafico]` como leyenda y asigna a mano en **Formato → Colores** el
código de `dim_fuente[color_hex]` de cada grupo (son 7):

| Grupo | Color |
|---|---|
| Carbón | `#6250D6` |
| Gas y petróleo | `#E87BA4` |
| Nuclear | `#E34948` |
| Hidroeléctrica | `#2A78D6` |
| Solar | `#EDA100` |
| Eólica | `#1BAF7A` |
| Otras renovables | `#008300` |

Esta paleta está validada para que los grupos vecinos se distingan también con daltonismo.
Aun así, activa las **etiquetas de datos** en los gráficos apilados: el color no debe ser la única pista.

---

## 6. Páginas del informe

Tamaño de página: 16:9. Deja un margen de ~20 px y alinea los objetos a una grilla.

### Página 1 — Chile: resumen

| Zona | Visual | Configuración |
|---|---|---|
| Encabezado | Tarjeta (texto) | Medida `Título página`; debajo una tarjeta con `Nota año preliminar` |
| Filtros (fila superior) | 2 segmentaciones | `dim_anio[anio]` (lista desplegable, selección única, **predeterminado 2024**) y `dim_pais[pais]` (**predeterminado Chile**) |
| KPI (fila de 4) | Tarjetas | `% Renovable` · `Cambio vs 2015 (pp)` · `% Carbón` · `Brecha vs LatAm (pp)` |
| Centro izquierda | **Gráfico de áreas apiladas** | Eje X `dim_anio[anio]` · Valores `Generación TWh` · Leyenda `dim_fuente[grupo_grafico]` |
| Centro derecha | **Gráfico de líneas** | Eje X `dim_anio[anio]` · Valores `% Renovable`, `% Renovable LatAm`, `% Renovable Mundo` |
| Abajo | Gráfico de columnas | Eje X `dim_anio[anio]` · Valores `Variación % renovable (pp)` (colores condicionales: verde > 0, rojo < 0) |

> Los gráficos de evolución (áreas y líneas) no deben filtrarse por el año: selecciona la
> segmentación de año → **Formato → Editar interacciones** → marca "Ninguno" sobre esos dos gráficos.

### Página 2 — Comparación latinoamericana

| Zona | Visual | Configuración |
|---|---|---|
| Filtros | Segmentación | `dim_anio[anio]` (predeterminado 2024); filtro de página `dim_pais[es_latam] = Verdadero` |
| Izquierda | **Barras horizontales** | Eje `dim_pais[pais]` · Valor `% Renovable` · ordenar descendente · filtro del visual `Generación TWh ≥ 5` · resalta Chile con formato condicional |
| Derecha arriba | **Gráfico de dispersión** | X `% Renovable` · Y `Intensidad de carbono (gCO2/kWh)` · Tamaño `Generación TWh` · Valores `dim_pais[pais]` · quitar el filtro de página para ver todos los países y usar `dim_pais[es_latam]` como leyenda |
| Derecha abajo | **Tabla** | `pais`, `% Renovable`, `% Solar + eólica`, `Cambio vs 2015 (pp)`, `Ranking % renovable LatAm`, `CO2 per cápita (t)` con barras de datos en `% Renovable` |

### Página 3 — El boom solar de Chile (opcional)

- Columnas agrupadas: `dim_anio[anio]` × `Generación TWh` filtrado a fuente Solar, para Chile, Brasil y México.
- Línea: `Participación en solar LatAm` para Chile (2012–2024).
- Cuadro de texto con 2–3 hallazgos (ver README).

### Página 4 — Notas y metodología

Cuadro de texto con: fuente (Our World in Data, CC BY 4.0), fecha de descarga,
definición de "renovable" (hidro + solar + eólica + bioenergía + geotermia/otras),
que los promedios regionales están ponderados por TWh y que 2025 es preliminar.

---

## 7. Checklist antes de publicar

- [ ] Chile 2024: `% Renovable` = 70,0 % y `% Carbón` ≈ 15,3 % (compara con `outputs/01_mix_electrico_chile.csv`).
- [ ] `% Renovable LatAm` 2024 ≈ 62,7 % y `% Renovable Mundo` ≈ 32,0 % (compara con `outputs/04_chile_vs_latam_vs_mundo.csv`).
- [ ] Ningún gráfico usa doble eje.
- [ ] Todos los visuales tienen título que dice qué muestran.
- [ ] Guardaste `powerbi/transicion_energetica.pbix` y capturas en `docs/img/dashboard_p1.png`, `dashboard_p2.png`.
- [ ] (Opcional) **Publicar en la web** desde Power BI Service y pegar el enlace en el README.
