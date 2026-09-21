import csv
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abc_file = os.path.join(base_dir, "resultados", "abc.csv")
    xyz_file = os.path.join(base_dir, "resultados", "xyz.csv")

    out_clasificacion = os.path.join(base_dir, "resultados", "clasificacion.csv")
    out_politicas = os.path.join(base_dir, "resultados", "politicas.md")

    abc_data = {}
    with open(abc_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            abc_data[r["sku"]] = r

    xyz_data = {}
    with open(xyz_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            xyz_data[r["sku"]] = r

    rows = []
    for sku, abc_row in abc_data.items():
        xyz_row = xyz_data[sku]
        clase_abc = abc_row["clase_abc"]
        cv = xyz_row["cv"]
        clase_xyz = xyz_row["clase_xyz"]
        celda = f"{clase_abc}{clase_xyz}"
        rows.append({
            "sku": sku,
            "clase_abc": clase_abc,
            "cv": cv,
            "clase_xyz": clase_xyz,
            "celda": celda
        })

    with open(out_clasificacion, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sku", "clase_abc", "cv", "clase_xyz", "celda"])
        for r in rows:
            writer.writerow([r["sku"], r["clase_abc"], r["cv"], r["clase_xyz"], r["celda"]])

    politicas = """# Políticas de gestión por celda de la matriz ABC × XYZ

- **AX (Revisión continua / Stock mínimo)**: Referencias clave de máximo margen y demanda muy estable. Programación automatizada de pedidos periódicos con proveedores y stock de seguridad mínimo.
- **AY (Revisión periódica semanal / Buffer medio)**: Alto margen pero con variabilidad moderada. Requiere supervisión semanal de previsiones y colchón de seguridad ajustado a la estacionalidad.
- **BX (Revisión periódica / Lote económico)**: Margen intermedio y demanda predecible. Gestión mediante punto de reequilibrio de pedido (ROP) estandarizado y revisiones quincenales.
- **BY (Revisión quincenal / Colchón flexible)**: Margen medio con variabilidad moderada. Monitoreo quincenal de ventas para ajustar la producción/compra antes de picos de demanda.
- **BZ (Revisión por pedido / Colchón dinámico)**: Margen intermedio y demanda muy errática. Evitar sobrestock; compras bajo demanda proyectada o lotes pequeños con buffer flexible.
- **CX (Gestión automatizada / Lotes grandes)**: Bajo margen pero demanda constante. Automatización total de reposición en lotes óptimos con bajo coste de gestión.
- **CY (Gestión simplificada / Revisión mensual)**: Bajo margen y variabilidad media. Reposición mensual simplificada asegurando disponibilidad sin dedicar excesivo tiempo analítico.
- **CZ (Bajo pedido / Sin stock permanente)**: Bajo margen y alta incertidumbre. Gestión bajo pedido o stock mínimo bajo demanda explícita para evitar obsolescencia y costes financieros.
"""

    with open(out_politicas, mode="w", encoding="utf-8") as f:
        f.write(politicas)

if __name__ == "__main__":
    main()
