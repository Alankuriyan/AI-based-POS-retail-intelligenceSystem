import pandas as pd

# Load CSV
df = pd.read_csv("monthly_revenue.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Correct date parsing (IMPORTANT)
df['Date'] = pd.to_datetime(
    df['Date'],
    dayfirst=True,
    errors='coerce'
)

# Convert numeric columns
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')
df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')

# Remove invalid rows
df = df.dropna(subset=['Date', 'Qty', 'Rate'])

# Revenue calculation
df['Revenue'] = df['Qty'] * df['Rate']

# Extract month
df['Month'] = df['Date'].dt.to_period('M')

# Monthly revenue
monthly_revenue = (
    df.groupby('Month')['Revenue']
    .sum()
    .reset_index()
)

# Rename columns
monthly_revenue.columns = ['Month', 'Total Revenue']

# Print result
print("\nMonthly Revenue:\n")
print(monthly_revenue)

# Save result
monthly_revenue.to_csv("monthly_revenue.csv", index=False)

print("\nSaved as monthly_revenue.csv")