# 🚗 SmartCar Advisor 2025  
### Intelligent Car Recommendation System — CPSC 583 Project  
*Developed by Rahul Putta, Ibad Ur Rahman Mohammed, and Sasidhar Jonnalagadda*

---

## 🧠 Overview  
**SmartCar Advisor 2025** is an **intelligent expert system** that recommends the best car based on user preferences like budget, fuel type, transmission, and purpose (city, family, sport, offroad).  
It combines **Prolog-based reasoning** with **Python (Streamlit UI)** and a **realistic car dataset** to deliver personalized, explainable car recommendations.  

---

## 🎯 Features  
✅ **User-Friendly Interface:** Built using Streamlit for real-time car search and visualization  
✅ **Knowledge-Based Reasoning:** Prolog rules provide expert logic and explanations  
✅ **Dynamic Filtering:** Python + Pandas filters refine results by budget and performance  
✅ **Explainable Output:** Each recommendation includes reasoning and SmartCar Score  
✅ **Dataset Integration:** 1200+ real-world cars with brand, price, fuel, transmission, and purpose  

---

## ⚙️ Technologies Used  
- 🐍 **Python 3.10+**  
- 🧠 **Prolog (SWI-Prolog via PySwip)**  
- 📊 **Pandas, NumPy**  
- 🌐 **Streamlit**  
- 💾 **cars_dataset.csv** — Clean dataset of 1200+ realistic car models  

---

## 📂 Project Structure  
SmartCarAdvisor/
│
├── ui_app.py # Streamlit web application
├── main.py # Command-line interface
├── car_kb.pl # Knowledge base (rules)
├── cars_facts.pl # Prolog facts from dataset
├── data/
│ └── cars_datasets.csv # Main dataset
├── requirements.txt
└── README.md


---

## 🚀 How to Run

### 1️⃣ Clone the Repository

git clone https://github.com/rahulputta0209/SmartCarAdvisor2025.git
cd SmartCarAdvisor2025

2️⃣ Set Up Environment
python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows
pip install -r requirements.txt


3️⃣ Run the Streamlit App
streamlit run ui_app.py

SmartCar Score Formula

The SmartCar Score evaluates each car using:

SmartCarScore = (Rating × 20) + BudgetFit + PerformanceScore

Where:

Rating = User or dataset rating (1–5 stars)

BudgetFit = How closely the car price fits the budget

PerformanceScore = Bonus for horsepower, acceleration, etc.

📊 Example Input / Output

Input:

Budget: $40,000  
Fuel: Petrol  
Transmission: Automatic  
Purpose: Family

Output:

🏆 Top Recommendations:
1. Toyota Camry — Smooth petrol engine, automatic, ideal for family use
2. Honda Accord — Reliable family sedan with 5⭐ rating
3. Kia Sorento — Spacious SUV within your budget

🧪 Lessons Learned

Integrating Prolog with Python improves reasoning explainability

Data cleaning and normalization are critical for real-world accuracy

Building an end-to-end pipeline with Streamlit UI + Knowledge Base simplifies presentation and usability

Explainable AI adds significant value to user trust


