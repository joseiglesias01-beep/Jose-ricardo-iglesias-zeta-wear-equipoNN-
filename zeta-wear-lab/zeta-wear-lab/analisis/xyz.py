import csv
import math
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "datos", "ex2_monthly_sales.csv")
    output_dir = os.path.join(base_dir, "resultados")
    output_file = os.path.join(output_dir, "xyz.csv")

    os.makedirs(output_dir, exist_ok=True)

    results = []
    with open(input_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row["sku"]
            monthly_sales = [float(row[f"2026-{m:02d}"]) for m in range(1, 13)]

            media_mensual = sum(monthly_sales) / 12.0

            # Population standard deviation
            variance = sum((x - media_mensual) ** 2 for x in monthly_sales) / 12.0
            desv_tipica = math.sqrt(variance)

            cv = desv_tipica / media_mensual if media_mensual > 0 else 0.0

            if cv <= 0.25:
                clase_xyz = "X"
            elif cv <= 0.50:
                clase_xyz = "Y"
            else:
                clase_xyz = "Z"

            results.append({
                "sku": sku,
                "media_mensual": media_mensual,
                "desv_tipica": desv_tipica,
                "cv": cv,
                "clase_xyz": clase_xyz
            })

    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sku", "media_mensual", "desv_tipica", "cv", "clase_xyz"])
        for r in results:
            writer.writerow([
                r["sku"],
                f"{r['media_mensual']:.2f}",
                f"{r['desv_tipica']:.2f}",
                f"{r['cv']:.4f}",
                r["clase_xyz"]
            ])

if __name__ == "__main__":
    main()
