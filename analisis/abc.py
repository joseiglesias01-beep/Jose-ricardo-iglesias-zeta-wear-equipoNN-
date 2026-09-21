import csv
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "datos", "ex2_sku_master.csv")
    output_dir = os.path.join(base_dir, "resultados")
    output_file = os.path.join(output_dir, "abc.csv")

    os.makedirs(output_dir, exist_ok=True)

    skus_data = []
    with open(input_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row["sku"]
            price = float(row["price"])
            cost = float(row["cost"])
            annual_demand = float(row["annual_demand"])
            margen_anual = annual_demand * (price - cost)
            skus_data.append({
                "sku": sku,
                "margen_anual": margen_anual
            })

    # Sort descending by margen_anual
    skus_data.sort(key=lambda x: x["margen_anual"], reverse=True)

    total_margen = sum(x["margen_anual"] for x in skus_data)

    cum_margen = 0.0
    for item in skus_data:
        cum_margen += item["margen_anual"]
        pct_acumulado = (cum_margen / total_margen) * 100.0

        if pct_acumulado <= 80.0:
            clase = "A"
        elif pct_acumulado <= 95.0:
            clase = "B"
        else:
            clase = "C"

        item["pct_acumulado"] = pct_acumulado
        item["clase_abc"] = clase

    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sku", "margen_anual", "pct_acumulado", "clase_abc"])
        for item in skus_data:
            writer.writerow([
                item["sku"],
                f"{item['margen_anual']:.2f}",
                f"{item['pct_acumulado']:.2f}",
                item["clase_abc"]
            ])

if __name__ == "__main__":
    main()
