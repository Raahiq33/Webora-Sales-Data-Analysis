
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent
CHART_DIR = BASE_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)

# 1. Load dataset
df = pd.read_csv(BASE_DIR / "sales_data.csv")

# 2. Data cleaning
df.columns = df.columns.str.strip()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

df = df.dropna(subset=["Date", "Product", "Category", "Quantity", "Price"])
df = df.drop_duplicates()
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)].copy()

if df.empty:
    raise ValueError("No valid sales records found.")

# 3. Calculate sales
df["Total_Sales"] = df["Quantity"] * df["Price"]
df["Month"] = df["Date"].dt.strftime("%Y-%m")

df.to_csv(BASE_DIR / "cleaned_sales_data.csv", index=False)

# 4. Five statistics
total_revenue = df["Total_Sales"].sum()
average_sale = df["Total_Sales"].mean()
total_quantity = df["Quantity"].sum()
highest_sale = df["Total_Sales"].max()
total_transactions = len(df)

print("\n===== SALES DATA ANALYSIS =====")
print(f"Total Revenue: LKR {total_revenue:,.2f}")
print(f"Average Sale: LKR {average_sale:,.2f}")
print(f"Total Quantity Sold: {total_quantity}")
print(f"Highest Transaction: LKR {highest_sale:,.2f}")
print(f"Total Transactions: {total_transactions}")

# 5. Grouped analysis
monthly_sales = df.groupby("Month")["Total_Sales"].sum()
category_sales = df.groupby("Category")["Total_Sales"].sum()
product_sales = df.groupby("Product")["Total_Sales"].sum()

# 6. Chart 1: Monthly sales
plt.figure(figsize=(9, 5))
monthly_sales.plot(kind="bar", color="royalblue")
plt.title("Monthly Sales Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (LKR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(CHART_DIR / "monthly_sales.png")
plt.close()

# 7. Chart 2: Category sales
plt.figure(figsize=(7, 5))
category_sales.plot(kind="pie", autopct="%1.1f%%")
plt.title("Sales by Category")
plt.ylabel("")
plt.tight_layout()
plt.savefig(CHART_DIR / "category_sales.png")
plt.close()

# 8. Chart 3: Product sales
plt.figure(figsize=(9, 5))
product_sales.sort_values().plot(kind="barh", color="seagreen")
plt.title("Revenue by Product")
plt.xlabel("Revenue (LKR)")
plt.tight_layout()
plt.savefig(CHART_DIR / "product_sales.png")
plt.close()

# 9. Save statistics
results = pd.DataFrame({
    "Statistic": [
        "Total Revenue",
        "Average Sale",
        "Total Quantity Sold",
        "Highest Transaction",
        "Total Transactions"
    ],
    "Value": [
        total_revenue,
        average_sale,
        total_quantity,
        highest_sale,
        total_transactions
    ]
})
results.to_csv(BASE_DIR / "analysis_results.csv", index=False)

# 10. Three findings
print("\n===== KEY FINDINGS =====")
print(f"1. Highest revenue month: {monthly_sales.idxmax()}")
print(f"2. Best-selling category by revenue: {category_sales.idxmax()}")
print(f"3. Top product by revenue: {product_sales.idxmax()}")

print("\nSUCCESS! Analysis completed.")
print("3 charts saved in the charts folder.")
print("CSV reports generated successfully.")
