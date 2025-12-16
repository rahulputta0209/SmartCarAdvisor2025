import pandas as pd
import os

# === Load cleaned dataset ===
df = pd.read_csv("data/cars_clean.csv")
print(f"✅ Loaded cleaned dataset with {len(df)} rows")

# === Ensure output directory exists ===
save_path = "cars_facts.pl"

# === Generate Prolog facts ===
with open(save_path, "w", encoding="utf-8") as f:
    f.write("% =========================================\n")
    f.write("%  Auto-generated Prolog facts from cars_clean.csv\n")
    f.write("% =========================================\n\n")

    for _, row in df.iterrows():
        try:
            brand = str(row["Brand"]).lower().replace(" ", "_")
            name = str(row["Name"]).lower().replace(" ", "_")
            fuel = str(row["Fuel"]).lower().replace(" ", "_")
            transmission = str(row["Transmission"]).lower().replace(" ", "_")
            seats = int(row["Seats"])
            price = int(float(row["Price"]))
            hp = int(row["Horsepower"]) if not pd.isna(row["Horsepower"]) else 0
            purpose = "sport" if hp > 400 else "family" if seats >= 5 else "city"

            fact = (
                f"car('{name}', brand({brand}), price({price}), fuel({fuel}), "
                f"transmission({transmission}), seats({seats}), purpose({purpose}), rating(4)).\n"
            )
            f.write(fact)
        except Exception as e:
            print(f"⚠️ Skipped one row due to error: {e}")

print(f"✅ Export complete → {save_path}")
