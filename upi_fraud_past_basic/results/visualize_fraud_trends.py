import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter import filedialog

# 🚀 Start
print("🚀 Script started!")

# Function to select CSV file
def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select the Predictions CSV File", filetypes=[("CSV files", "*.csv")])
    return file_path

# Step 1: Select CSV file
csv_file = select_csv_file()
if not csv_file:
    print("❌ ERROR: No file selected! Exiting...")
    exit()

# Step 2: Define results and visualization folder
RESULTS_FOLDER = os.path.dirname(csv_file)
VISUALS_FOLDER = os.path.join(RESULTS_FOLDER, "visuals")
os.makedirs(VISUALS_FOLDER, exist_ok=True)

print(f"📂 Selected file: {csv_file}")
print(f"📂 Saving visualizations in: {VISUALS_FOLDER}")

# Step 3: Load Data
try:
    df = pd.read_csv(csv_file)
    print("✅ Data loaded successfully!")
except Exception as e:
    print(f"❌ ERROR: Failed to load CSV -> {e}")
    exit()

# Step 4: Check Required Columns
required_columns = ["Transaction_ID", "Transaction_Amount", "Is_Fraudulent_Predicted", "Timestamp", "Location", "Transaction_Type"]
missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    print(f"❌ ERROR: Missing columns in CSV -> {missing_cols}")
    exit()

print("✅ All required columns are present!")

# Step 5: Convert Timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"], dayfirst=True, errors="coerce")
df["Date"] = df["Timestamp"].dt.date

### **1️⃣ Fraud vs. Non-Fraud Count Plot**
plt.figure(figsize=(6, 4))
sns.countplot(x=df["Is_Fraudulent_Predicted"], hue=df["Is_Fraudulent_Predicted"], palette=["blue", "red"], legend=False)
plt.title("Fraud vs. Non-Fraud Transactions")
plt.xlabel("Fraudulent (1) vs. Non-Fraudulent (0)")
plt.ylabel("Count")
plt.savefig(os.path.join(VISUALS_FOLDER, "fraud_vs_non_fraud.png"))
plt.close()
print("✅ Fraud vs. Non-Fraud Transactions saved!")

### **2️⃣ Fraud by Transaction Amount (Boxplot)**
if "Transaction_Amount" in df.columns:
    plt.figure(figsize=(6, 4))
    sns.boxplot(
        x=df["Is_Fraudulent_Predicted"].astype(str),  
        y=df["Transaction_Amount"],  
        hue=df["Is_Fraudulent_Predicted"].astype(str),  
        palette=["green", "red"],
        legend=False  
    )
    plt.title("Fraud vs. Transaction Amount")
    plt.xlabel("Fraudulent (1) vs. Non-Fraudulent (0)")
    plt.ylabel("Transaction Amount")
    plt.savefig(os.path.join(VISUALS_FOLDER, "fraud_vs_transaction_amount.png"))
    plt.close()
    print("✅ Fraud vs. Transaction Amount boxplot saved!")

### **3️⃣ Fraud Trend Over Time (Line Chart)**
fraud_over_time = df[df["Is_Fraudulent_Predicted"] == 1].groupby("Date").size()

plt.figure(figsize=(8, 5))
fraud_over_time.plot(kind="line", color="red", marker="o")
plt.title("Fraud Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Fraud Cases")
plt.grid(True)
plt.savefig(os.path.join(VISUALS_FOLDER, "fraud_trend_over_time.png"))
plt.close()
print("✅ Fraud trend over time saved!")

### **4️⃣ Fraud by Location (Top 10 Cities)**
fraud_by_location = df[df["Is_Fraudulent_Predicted"] == 1]["Location"].value_counts().head(10)

plt.figure(figsize=(8, 5))
sns.barplot(x=fraud_by_location.values, y=fraud_by_location.index, hue=fraud_by_location.index, palette="Reds", legend=False)
plt.title("Top 10 Locations with Most Fraudulent Transactions")
plt.xlabel("Number of Fraud Cases")
plt.ylabel("Location")
plt.savefig(os.path.join(VISUALS_FOLDER, "fraud_by_location.png"))
plt.close()
print("✅ Fraud by location saved!")

### **5️⃣ Fraud vs. Non-Fraud Transaction Amount (Histogram)**
plt.figure(figsize=(8, 5))
sns.histplot(df[df["Is_Fraudulent_Predicted"] == 1]["Transaction_Amount"], bins=30, color="red", label="Fraud", kde=True)
sns.histplot(df[df["Is_Fraudulent_Predicted"] == 0]["Transaction_Amount"], bins=30, color="blue", label="Non-Fraud", kde=True)
plt.title("Transaction Amount Distribution (Fraud vs. Non-Fraud)")
plt.xlabel("Transaction Amount")
plt.ylabel("Frequency")
plt.legend()
plt.savefig(os.path.join(VISUALS_FOLDER, "fraud_vs_transaction_histogram.png"))
plt.close()
print("✅ Fraud vs. Non-Fraud transaction amount histogram saved!")

### **6️⃣ Fraud Percentage Pie Chart**
fraud_count = df["Is_Fraudulent_Predicted"].value_counts()
labels = ["Non-Fraud", "Fraud"]
colors = ["blue", "red"]

plt.figure(figsize=(6, 6))
plt.pie(fraud_count, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140, explode=[0, 0.1], shadow=True)
plt.title("Fraud Percentage in Transactions")
plt.savefig(os.path.join(VISUALS_FOLDER, "fraud_percentage_pie_chart.png"))
plt.close()
print("✅ Fraud percentage pie chart saved!")

### **7️⃣ Fraud by Transaction Type**
plt.figure(figsize=(8, 5))
sns.countplot(y=df[df["Is_Fraudulent_Predicted"] == 1]["Transaction_Type"], hue=df[df["Is_Fraudulent_Predicted"] == 1]["Transaction_Type"], palette="Reds", legend=False)
plt.title("Fraud by Transaction Type")
plt.xlabel("Count")
plt.ylabel("Transaction Type")
plt.savefig(os.path.join(VISUALS_FOLDER, "fraud_by_transaction_type.png"))
plt.close()
print("✅ Fraud by transaction type saved!")

# 🎯 Complete
print("\n🎯 Fraud visualization completed successfully!")
