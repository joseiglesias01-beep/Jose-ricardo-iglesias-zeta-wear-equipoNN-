# Encargo 4: indicadores no calculables con los datos entregados

**Resultado de la revisión de Codex: faltan datos.** Los valores vacíos de
`kpis.csv` significan NO DISPONIBLE, nunca cero. No se han estimado indicadores
ni usado fuentes externas. Esta documentación no acredita una revisión humana.

## Rotación anual por SKU

La fórmula solicitada es `annual_demand / stock_medio`. El catálogo contiene
demanda anual, precio, coste y plazo de entrega, pero no stock medio ni una
serie de existencias que permita calcularlo. Ventas mensuales y lead time no
son stock medio. Se necesita stock medio anual por SKU, con unidades, periodo
y método de cálculo documentados, o existencias fechadas para obtenerlo.

## Días con rotura por SKU en 2026

`ex1_demand_daily.csv` contiene 120 fechas, del 2026-09-01 al 2026-12-29,
y no tiene columna SKU. Hay tres registros con `stockout_flag=1`: 1 y 2 de
octubre y 24 de noviembre. Ese recuento solo describe la serie disponible:
no puede asignarse a ninguno de los 20 SKU ni presentarse como dato anual.
Faltan 245 días del calendario 2026, además de la identificación por SKU.

Se necesita una serie completa de los 365 días de 2026 por referencia, con
SKU, fecha y estado de rotura explícito. Los días ausentes no equivalen a
ausencia de rotura. Antes de contar, comprobar duplicados, cobertura y el
criterio de qué constituye un día con rotura.

## Decisión propuesta para el comité

No publicar cifras de rotación o roturas anuales hasta disponer de las
fuentes. Rechazar cualquier propuesta que rellene los huecos con cero,
stock supuesto, benchmarks o los mismos tres días para todos los SKU.
El PR documenta la insuficiencia; el objetivo numérico queda bloqueado.

`kpis.csv` conserva las 20 referencias del catálogo, deja ambos indicadores
vacíos y añade un estado y un motivo explícitos. El equipo debe verificar
estas ausencias y registrar su decisión en el PR.
