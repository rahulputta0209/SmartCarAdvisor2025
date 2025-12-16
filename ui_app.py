import streamlit as st
from pyswip import Prolog
import pandas as pd
import numpy as np
import os

# ======================================
# SmartCar Advisor 2025 — Streamlit UI
# ======================================

st.set_page_config(page_title="SmartCar Advisor", page_icon="🚗", layout="wide")
st.title("🚗 SmartCar Advisor: An Intelligent Car Recommendation System")

# --- Initialize Prolog ---
prolog = Prolog()
base = os.path.dirname(__file__)

# --- Load Prolog files safely ---
try:
    kb_path = os.path.join(base, "car_kb.pl")
    facts_path = os.path.join(base, "cars_facts.pl")

    if os.path.exists(kb_path) and os.path.exists(facts_path):
        prolog.consult(kb_path)
        prolog.consult(facts_path)
        num_facts = len(list(prolog.query("car(_,_,_,_,_,_,_,_)")))
    else:
        st.sidebar.warning("⚠️ Missing Prolog files (car_kb.pl or cars_facts.pl). Using dataset filtering only.")
except Exception as e:
    st.sidebar.error(f"⚠️ Could not load Prolog files: {e}")

# --- Load dataset ---
possible_paths = [
    "data/cars_datasets.csv",
    "cars_datasets.csv",
    "/Users/rahulputta/Downloads/cars_datasets.csv"
]
data_path = next((p for p in possible_paths if os.path.exists(p)), None)

if not data_path:
    st.error("❌ cars_datasets.csv not found — please place it in /data or project folder.")
    st.stop()

df = pd.read_csv(data_path, encoding="latin1")

# --- Rename columns for consistency ---
column_map = {
    "Company Names": "brand",
    "Cars Names": "name",
    "Cars Prices": "price",
    "Fuel Types": "fuel_types",
    "Transmission": "transmission",
    "Seats": "seats",
    "Purpose": "purpose"
}
df = df.rename(columns=column_map)

# --- Add missing Rating column ---
if "rating" not in df.columns:
    df["rating"] = np.random.randint(3, 6, size=len(df))  # random 3–5 stars

# --- Clean and parse price values ---
def parse_price(p):
    if isinstance(p, str):
        p = p.replace("$", "").replace(",", "").replace("-", "").strip()
        try:
            return float(p)
        except:
            return np.nan
    return p

df["price"] = df["price"].apply(parse_price)

# --- Sidebar Filters ---
st.sidebar.header("🔧 Customize Your Preferences")

budget = st.sidebar.number_input("💰 Budget (USD)", min_value=5000, max_value=250000, value=50000, step=5000)
fuel_display = st.sidebar.selectbox("⛽ Fuel Type", ["Petrol", "Hybrid", "Electric", "Diesel"])
fuel = fuel_display.lower()
transmission = st.sidebar.selectbox("⚙️ Transmission", ["automatic", "manual"])
purpose_display = st.sidebar.selectbox("🚙 Purpose", ["City", "Family", "Sport", "Offroad"])
purpose = purpose_display.lower()

run_button = st.sidebar.button("Find My Car 🚘")

# --- When user clicks the button ---
if run_button:
    st.subheader("🔍 Searching for the best matches...")

    # --- Filter dataset ---
    filtered_df = df[
        (df["fuel_types"].astype(str).str.lower().str.contains(fuel, na=False)) &
        (df["transmission"].astype(str).str.lower().str.contains(transmission, na=False)) &
        (df["purpose"].astype(str).str.lower().str.contains(purpose, na=False)) &
        (df["price"].fillna(0) <= budget * 1.25)
    ]

    if filtered_df.empty:
        st.warning("❌ No cars found matching your filters. Try adjusting your preferences.")
    else:
        results = []
        for _, row in filtered_df.iterrows():
            car = row["name"]
            brand = row["brand"]
            price = row["price"]
            rating = row["rating"]
            fuel_type = row["fuel_types"]
            trans = row["transmission"]
            car_purpose = row["purpose"]

            # Safely handle missing or NaN price
            if pd.isna(price):
                price_display = "Unknown"
                price = budget
            else:
                price_display = f"${int(price):,}"

            # Handle missing rating
            if pd.isna(rating):
                rating = 3

            price_fit = max(0, (budget - price) / budget) * 100
            smart_score = rating * 20 + price_fit

            reason = f"💡 The {brand} {car} is a {car_purpose} car with {fuel_type} fuel and {trans} transmission — ideal for your needs."
            results.append((car, smart_score, reason, price_display, row))

        # --- Rank by SmartCar Score ---
        top_cars = sorted(results, key=lambda x: x[1], reverse=True)[:10]

        st.subheader("🏆 Top SmartCar Recommendations")
        for rank, (car, score, reason, price_display, row) in enumerate(top_cars, start=1):
            with st.container():
                st.markdown(f"### {rank}.  **🚘 {car.title()}**")
                st.progress(min(score / 200, 1.0))
                st.write(reason)
                st.caption(
                    f"💰 Price: {price_display} | 🚘 Brand: {row['brand']} | "
                    f"⛽ Fuel: {row['fuel_types']} | ⚙️ {row['transmission']} | ⭐ {row['rating']}/5"
                )
                st.divider()

