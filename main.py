from pyswip import Prolog
import pandas as pd
import os
import numpy as np

# =======================================
# SmartCar Advisor 2025 (Console Version)
# =======================================

print("🚗 Welcome to SmartCar Advisor 2025 🚗")
print("An Intelligent Car Recommendation System — CPSC 583 Project\n")

prolog = Prolog()

# --- Load Prolog files ---
try:
    prolog.consult("car_kb.pl")
    prolog.consult("cars_facts.pl")
    num_facts = len(list(prolog.query("car(_,_,_,_,_,_,_,_)")))
    print(f"✅ Loaded Prolog knowledge base with {num_facts} car entries.\n")
except Exception as e:
    print(f"⚠️ Warning: Could not load Prolog files ({e}). Proceeding with dataset filtering only.\n")

# --- Load enhanced dataset ---
df_path = os.path.join("data", "cars_datasets.csv")
if not os.path.exists(df_path):
    print(f"❌ Dataset not found at {df_path}")
    exit()

df = pd.read_csv(df_path, encoding="latin1")

# Normalize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# --- Collect user preferences ---
try:
    budget = int(input("💰 Enter your budget (USD): "))
    fuel = input("⛽ Preferred fuel type (petrol/diesel/hybrid/electric): ").strip().lower()
    transmission = input("⚙️ Preferred transmission (manual/automatic): ").strip().lower()
    purpose = input("🚙 Main purpose (city/family/sport/offroad): ").strip().lower()
except Exception as e:
    print(f"⚠️ Input error: {e}")
    exit()

print("\n🔍 Searching for best matches...\n")

# --- Filter dataset ---
filtered_df = df[
    (df["fuel_types"].astype(str).str.lower().str.contains(fuel, na=False)) &
    (df["transmission"].astype(str).str.lower().str.contains(transmission, na=False)) &
    (df["purpose"].astype(str).str.lower().str.contains(purpose, na=False))
]

# Handle budget filtering
filtered_df = filtered_df[
    filtered_df["cars_prices"]
    .replace('[\$,]', '', regex=True)
    .astype(str)
    .str.extract('(\d+)', expand=False)
    .astype(float)
    <= budget * 1.25
]

if filtered_df.empty:
    print("❌ No cars found for your preferences. Try adjusting your filters.")
    exit()

# --- Create a SmartCar Score ---
# Add synthetic rating if missing
if "rating" not in df.columns:
    np.random.seed(42)
    filtered_df["rating"] = np.random.randint(3, 5, size=len(filtered_df))

# Price normalization
filtered_df["numeric_price"] = (
    filtered_df["cars_prices"]
    .replace('[\$,]', '', regex=True)
    .astype(str)
    .str.extract('(\d+)', expand=False)
    .astype(float)
)

results = []
for _, row in filtered_df.iterrows():
    car = row["cars_names"]
    brand = row["company_names"]
    fuel_type = row["fuel_types"]
    trans = row["transmission"]
    price = row["numeric_price"]
    purpose_type = row["purpose"]
    rating = row["rating"]

    price_fit = max(0, (budget - price) / budget) * 100
    smart_score = rating * 20 + price_fit

    reason = f"{brand} {car} is a {purpose_type} car with {fuel_type} fuel and {trans} transmission — great value for your budget."
    results.append((car, brand, smart_score, reason, price, fuel_type, trans, rating))

# --- Rank and display results ---
top_cars = sorted(results, key=lambda x: x[2], reverse=True)[:10]

print("🏆 Top SmartCar Recommendations:\n")
for rank, (car, brand, score, reason, price, fuel, trans, rating) in enumerate(top_cars, start=1):
    print(f"{rank}. ✅ {brand} {car}")
    print(f"   💬 {reason}")
    print(f"   💰 Price: ${int(price)} | ⛽ {fuel.title()} | ⚙️ {trans.title()} | ⭐ {rating}/5")
    print(f"   📊 SmartCar Score: {round(score, 2)}\n")

print("✨ Thank you for using SmartCar Advisor 2025! ✨")
