import csv
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resultados_dir = os.path.join(base_dir, "resultados")
    abc_file = os.path.join(resultados_dir, "abc.csv")
    xyz_file = os.path.join(resultados_dir, "xyz.csv")
    clasificacion_file = os.path.join(resultados_dir, "clasificacion.csv")
    politicas_file = os.path.join(resultados_dir, "politicas.md")

    # Read abc.csv
    abc_data = {}
    with open(abc_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            abc_data[row["sku"]] = row["clase_abc"]

    # Read xyz.csv
    xyz_data = {}
    with open(xyz_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            xyz_data[row["sku"]] = {
                "cv": row["cv"],
                "clase_xyz": row["clase_xyz"]
            }

    # Merge and build classification rows
    clasificacion_rows = []
    occupied_cells = set()

    for sku in abc_data:
        clase_abc = abc_data[sku]
        info_xyz = xyz_data.get(sku, {"cv": "0.0000", "clase_xyz": "X"})
        clase_xyz = info_xyz["clase_xyz"]
        cv = info_xyz["cv"]
        celda = f"{clase_abc}{clase_xyz}"
        occupied_cells.add(celda)

        clasificacion_rows.append({
            "sku": sku,
            "clase_abc": clase_abc,
            "cv": cv,
            "clase_xyz": clase_xyz,
            "celda": celda
        })

    # Write clasificacion.csv
    with open(clasificacion_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sku", "clase_abc", "cv", "clase_xyz", "celda"])
        for row in clasificacion_rows:
            writer.writerow([
                row["sku"],
                row["clase_abc"],
                row["cv"],
                row["clase_xyz"],
                row["celda"]
            ])

    # Policy descriptions for each matrix cell
    politicas_dict = {
        "AX": "Alto margen y demanda estable. Revisión continua, automatización de reposición y stock de seguridad mínimo para garantizar máxima disponibilidad.",
        "AY": "Alto margen y demanda moderadamente variable. Revisión continua con pronóstico ajustado y stock de seguridad medio para absorber fluctuaciones.",
        "AZ": "Alto margen y demanda muy errática. Control estrecho personalizado, pedidos sobre demanda o acuerdos prioritarios con proveedores.",
        "BX": "Margen medio y demanda estable. Revisión periódica automatizada, lote óptimo de compra y stock de seguridad bajo.",
        "BY": "Margen medio y demanda moderadamente variable. Revisión periódica con stock de seguridad moderado para balancear coste de almacenamiento y servicio.",
        "BZ": "Margen medio y demanda muy errática. Reposición bajo pedido o con lotes mínimos de seguridad estrictamente controlados.",
        "CX": "Bajo margen y demanda estable. Compras agrupadas en grandes lotes, gestión automatizada y mínimo esfuerzo administrativo.",
        "CY": "Bajo margen y demanda moderadamente variable. Revisión periódica simplificada, manteniendo stock mínimo para evitar sobrecostes.",
        "CZ": "Bajo margen y demanda muy errática. Gestión bajo pedido (MTO) o eliminación paulatina del catálogo para evitar obsolescencia."
    }

    # Write politicas.md
    with open(politicas_file, mode="w", encoding="utf-8") as f:
        f.write("# Políticas de Gestión para Matriz ABC × XYZ\n\n")
        f.write("A continuación se detallan las políticas de inventario aplicables a cada celda ocupada de la matriz:\n\n")
        all_cells = ["AX", "AY", "AZ", "BX", "BY", "BZ", "CX", "CY", "CZ"]
        for cell in all_cells:
            if cell in occupied_cells:
                f.write(f"### Celda {cell}\n")
                f.write(f"{politicas_dict[cell]}\n\n")

if __name__ == "__main__":
    main()
