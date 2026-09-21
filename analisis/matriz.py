"""Cruza ABC y XYZ por SKU, sin descartar filas ni recalcular sus criterios."""
import csv
import math
from pathlib import Path


POLICIES = {
    "AX": "Priorizar la disponibilidad por su margen alto. Automatizar alertas y reposición con revisión por excepciones; dimensionar el colchón cuando existan datos de stock y servicio.",
    "AY": "Revisar con frecuencia la previsión y la reposición por su margen alto y variabilidad intermedia. Mantener aprobación humana de ajustes y evaluar un colchón con datos de servicio y stock.",
    "AZ": "Priorizar revisión humana de demanda y compromisos de compra por su margen alto y variabilidad elevada. Usar alertas, evitar reposición ciega y dimensionar el colchón con evidencia adicional.",
    "BX": "Aplicar revisión periódica y automatizar alertas de reposición por su demanda estable. Ajustar el colchón al servicio objetivo cuando se disponga de existencias y demanda durante el plazo de entrega.",
    "BY": "Revisar periódicamente previsión y existencias, con alertas ante cambios de demanda. Ajustar el colchón con datos disponibles y validar manualmente cambios relevantes de compra.",
    "BZ": "Usar revisión humana ante variaciones de demanda y limitar compromisos de compra sin respaldo. Evaluar colchón y riesgo de sobrantes antes de automatizar pedidos.",
    "CX": "Simplificar la gestión con revisión agrupada y alertas automáticas por su margen relativo bajo y demanda estable. Evitar dedicar un colchón desproporcionado sin evaluar el nivel de servicio.",
    "CY": "Agrupar revisiones para contener el esfuerzo de gestión y controlar excepciones. Ajustar compras y colchón de forma prudente con evidencia de servicio y existencias.",
    "CZ": "Revisar conveniencia de mantener surtido y compras ante margen relativo bajo y alta variabilidad. Evitar grandes colchones o reposición automática sin supervisión; valorar compra bajo demanda cuando sea viable.",
}


def read_unique(path, required):
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if not set(required).issubset(reader.fieldnames or []):
            raise ValueError(f"Columnas incompletas en {path.name}")
        records = {}
        for row in reader:
            sku = row.get("sku")
            if not sku or sku in records or None in row:
                raise ValueError(f"SKU vacío, duplicado o fila inválida en {path.name}: {sku!r}")
            records[sku] = row
    if len(records) != 20:
        raise ValueError(f"{path.name}: se esperaban 20 SKU, hay {len(records)}")
    return records


def main():
    output = Path(__file__).resolve().parents[1] / "resultados"
    abc = read_unique(output / "abc.csv", ["sku", "clase_abc"])
    xyz = read_unique(output / "xyz.csv", ["sku", "cv", "clase_xyz"])
    if abc.keys() != xyz.keys():
        raise ValueError("ABC y XYZ no contienen exactamente los mismos SKU")
    rows = []
    for sku, value in abc.items():
        variability = xyz[sku]
        cv = float(variability["cv"])
        expected = "X" if cv <= 0.25 else "Y" if cv <= 0.5 else "Z"
        if value["clase_abc"] not in {"A", "B", "C"}:
            raise ValueError(f"Clase ABC inválida: {sku}")
        if not math.isfinite(cv) or cv < 0 or variability["clase_xyz"] != expected:
            raise ValueError(f"CV o clase XYZ inválidos: {sku}")
        cell = value["clase_abc"] + variability["clase_xyz"]
        rows.append([sku, value["clase_abc"], variability["cv"], variability["clase_xyz"], cell])
    occupied = {r[4] for r in rows}
    policies = ["# Políticas de gestión ABC×XYZ", "",
                "Recomendaciones cualitativas basadas en margen anual y variabilidad mensual. No son niveles de stock calculados.",
                "El stock medio, los niveles de servicio y el histórico de existencias no están disponibles: no se fijan cantidades de colchón ni frecuencias numéricas sin esos datos.", ""]
    for cell in sorted(occupied):
        policies.extend([f"## {cell}", POLICIES[cell], ""])
    with (output / "clasificacion.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, lineterminator="\n")
        writer.writerow(["sku", "clase_abc", "cv", "clase_xyz", "celda"])
        writer.writerows(rows)
    (output / "politicas.md").write_text("\n".join(policies), encoding="utf-8")


if __name__ == "__main__":
    main()
