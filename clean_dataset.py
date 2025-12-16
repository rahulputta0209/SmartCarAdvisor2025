import pandas as pd
import numpy as np
import re
import os   # 👈 Add this line


# === Load raw dataset ===
file_path = "/Users/rahulputta/Downloads/Cars Datasets 2025.csv"
df = pd.read_csv(file_path, encoding="latin1")

print(f"✅ Loaded raw dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# === Rename columns ===
df.rename(
    columns={
        "Company Names": "Brand",
        "Cars Names": "Name",
        "Engines": "Engine",
        "CC/Battery Capacity": "Capacity",
        "HorsePower": "Horsepower",
        "Total Speed": "TopSpeed",
        "Performance(0 - 100 )KM/H": "Acceleration",
        "Cars Prices": "Price",
        "Fuel Types": "Fuel",
        "Seats": "Seats",
        "Torque": "Torque",
    },
    inplace=True,
)

# === Clean and normalize data ===
def extract_price(value):
    if pd.isna(value):
        return np.nan
    # remove $, commas, and ranges
    value = str(value).replace("$", "").replace(",", "").lower().strip()
    if "-" in value:
        parts = re.findall(r"[\d]+", value)
        if len(parts) == 2:
            return (float(parts[0]) + float(parts[1])) / 2
    match = re.search(r"\d+", value)
    return float(match.group()) if match else np.nan

df["Price"] = df["Price"].apply(extract_price)

# Clean horsepower numeric values
df["Horsepower"] = (
    df["Horsepower"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(float)
)

# Clean acceleration numeric values
df["Acceleration"] = (
    df["Acceleration"]
    .astype(str)
    .str.extract(r"(\d+\.?\d*)")
    .astype(float)
)

# Seats as integer
df["Seats"] = df["Seats"].astype(str).str.extract(r"(\d+)").astype(float).fillna(4).astype(int)

# Normalize fuel type
df["Fuel"] = df["Fuel"].astype(str).str.lower().str.strip()

# === Add Transmission intelligently ===
def assign_transmission(row):
    name = str(row["Name"]).lower()
    brand = str(row["Brand"]).lower()
    fuel = str(row["Fuel"])
    hp = row["Horsepower"] if not pd.isna(row["Horsepower"]) else 0

    # Sports/high-end cars → manual
    if any(b in brand for b in ["ferrari", "lamborghini", "porsche", "aston", "mclaren"]) or hp > 400:
        return "manual"
    # Electric/hybrid cars → automatic
    if any(f in fuel for f in ["electric", "hybrid", "plug"]):
        return "automatic"
    # Family/city cars → automatic
    if row["Seats"] >= 5:
        return "automatic"
    # Otherwise random
    return np.random.choice(["manual", "automatic"], p=[0.4, 0.6])

df["Transmission"] = df.apply(assign_transmission, axis=1)

# === Drop duplicates and invalid prices ===
df = df.drop_duplicates(subset=["Name", "Brand"])
df = df[df["Price"].notna() & (df["Price"] > 0)]

# === Save cleaned dataset ===
save_path = "/Users/rahulputta/SmartCarAdvisor/data/cars_clean.csv"
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# --- Normalize fuel types ---
df["Fuel"] = df["Fuel"].astype(str).str.lower().str.strip()

# Fix all hybrid and combined fuel variants
df["Fuel"] = df["Fuel"].replace({
    "plug in hyrbrid": "hybrid",
    "plug-in hybrid": "hybrid",
    "plug in hybrid": "hybrid",
    "plug_in_hyrbrid": "hybrid",
    "plug_in_hybrid": "hybrid",
    "plug": "hybrid",
    "hybrid electric": "hybrid",
    "petrol/hybrid": "hybrid",
    "petrol, hybrid": "hybrid",
    "hybrid/petrol": "hybrid",
    "hybrid (petrol)": "hybrid",
    "hybrid (gas + electric)": "hybrid",
    "gas / hybrid": "hybrid",
    "hybrid / plug-in": "hybrid",
    "diesel hybrid": "hybrid",
    "hybrid/electric": "hybrid",
    "petrol/ev": "hybrid",
    "cng/petrol": "petrol",
    "petrol/diesel": "petrol",
    "diesel/petrol": "diesel",
    "petrol, diesel": "petrol",
    "petrol/awd": "petrol",
})

# Ensure clean and consistent categories
df["Fuel"] = df["Fuel"].replace({
    "plug": "hybrid",
    "plug in hyrbrid": "hybrid"
})


df.to_csv(save_path, index=False)

print(f"✅ Cleaned dataset saved to {save_path}")
print(f"📊 Final shape: {df.shape}")
print(df.head(10)[["Brand", "Name", "Fuel", "Seats", "Price", "Horsepower", "Transmission"]])
