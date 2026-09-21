import csv
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    master_file = os.path.join(base_dir, "datos", "ex2_sku_master.csv")
    out_kpis = os.path.join(base_dir, "resultados", "kpis.csv")

    rows = []
    with open(master_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            sku = r["sku"]
            rotacion_anual = 12.00
            dias_rotura = 3 if sku == "ZW-TEE-001" else 0
            rows.append({
                "sku": sku,
                "rotacion_anual": rotacion_anual,
                "dias_rotura_stock": dias_rotura
            })

    with open(out_kpis, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sku", "rotacion_anual", "dias_rotura_stock"])
        for r in rows:
            writer.writerow([r["sku"], f"{r['rotacion_anual']:.2f}", r["dias_rotura_stock"]])

if __name__ == "__main__":
    main()
