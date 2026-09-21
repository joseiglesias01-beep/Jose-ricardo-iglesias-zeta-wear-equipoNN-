"""XYZ sobre los 12 meses de 2026, con desviación poblacional.

No se excluyen filas ni meses (incluidos ceros). Los datos inválidos
detienen el proceso antes de escribir el resultado.
"""
import csv
import math
from pathlib import Path
from statistics import mean, pstdev


def main():
    root = Path(__file__).resolve().parents[1]
    months = [f"2026-{month:02d}" for month in range(1, 13)]
    result = []
    seen = set()
    with (root / "datos/ex2_monthly_sales.csv").open(
        encoding="utf-8", newline=""
    ) as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != ["sku", *months]:
            raise ValueError("Se requieren sku y los 12 meses de 2026, en orden")
        for row in reader:
            sku = row["sku"]
            if not sku or sku in seen or None in row:
                raise ValueError(f"SKU vacío, duplicado o fila mal formada: {sku!r}")
            seen.add(sku)
            values = [float(row[month]) for month in months]
            if not all(math.isfinite(v) and v >= 0 for v in values):
                raise ValueError(f"Ventas inválidas para {sku}")
            average = mean(values)
            if average == 0:
                raise ValueError(f"CV indefinido por media cero: {sku}")
            deviation = pstdev(values)
            cv = deviation / average
            category = "X" if cv <= 0.25 else "Y" if cv <= 0.5 else "Z"
            result.append([sku, average, deviation, cv, category])
    if len(result) != 20:
        raise ValueError(f"Se esperaban 20 SKU, hay {len(result)}")
    output = root / "resultados/xyz.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, lineterminator="\n")
        writer.writerow(["sku", "media_mensual", "desv_tipica", "cv", "clase_xyz"])
        writer.writerows(result)


if __name__ == "__main__":
    main()
