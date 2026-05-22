# AI Retail Demand Forecasting & Inventory Management System

## Overview

This project is an AI-powered retail demand forecasting and inventory management system developed using Python and Streamlit. The system helps shop owners manage inventory, analyze sales trends, generate POS bills, and predict future product demand using machine learning.

The application combines:
- Retail analytics
- Inventory management
- POS billing
- Demand forecasting
- Data visualization

into a single dashboard-based platform.

---

# Main Features

## Inventory Management
- Add and update stock
- Inventory tracking
- Low stock monitoring
- CSV-based storage
- PostgreSQL stock backup support

## POS Billing System
- Product-based billing interface
- Add-to-cart system
- Checkout functionality
- Automatic stock reduction
- Sales ledger generation

## AI Demand Forecasting
- Next-day demand prediction
- Weekly demand forecasting
- Inventory risk analysis
- Stock usage analysis

## Dashboard & Analytics
- Daily sales trends
- Revenue analytics
- Top-selling products
- Fast-moving products
- Slow-moving products
- AI retail insights

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Streamlit | Web application framework |
| Python | Backend logic |
| Pandas | Data handling and cleaning |
| NumPy | Mathematical operations |
| Scikit-learn | Machine learning |
| XGBoost | Forecasting algorithm |
| Joblib | Model saving/loading |
| Plotly | Data visualization |
| CSV Files | Local storage |
| PostgreSQL | Optional database backup |

---

# Machine Learning Features Extracted

The forecasting model uses the following extracted features:

| Feature | Description |
|---|---|
| prod_id | Product identifier |
| price | Product price |
| log_price | Log-transformed price |
| price_ratio | Price comparison ratio |
| month | Month feature |
| day | Day feature |
| week | Week feature |
| day_of_week | Weekday feature |
| is_weekend | Weekend indicator |
| lag_1 | Previous day demand |
| lag_7 | Previous week demand |
| trend_3 | 3-day trend |
| trend_7 | 7-day trend |

---

# Project Structure

```bash
minix/
│
├── app.py
├── datasets/
├── inventory/
├── ledger/
├── models/
├── pages/
├── components/
├── assets/
└── requirements.txt
```

---

# System Workflow

1. Upload sales dataset
2. Upload purchase dataset
3. Clean and process data
4. Extract machine learning features
5. Train forecasting model
6. Save trained model
7. Predict future demand
8. Analyze inventory trends
9. Generate POS bills
10. Update stock automatically

---

# Dashboard Modules

## Dashboard
Displays:
- Daily sales trends
- Revenue analytics
- Product insights
- Fast & slow-moving products

## Inventory Management
- Inventory stock control
- Product addition
- Stock updates
- PostgreSQL backup button

## POS System
- Product grid interface
- Cart and checkout
- Auto stock reduction
- Ledger generation

## Forecasting System
- Next-day prediction
- Weekly forecasting
- Inventory analysis
- Restock suggestions

---

# Model Storage

## Trained Model
```bash
models/retail_model.pkl
```

## Processed Feature Dataset
```bash
models/processed_data.pkl
```

---

# Local Storage Files

| File | Purpose |
|---|---|
| stock_data.csv | Inventory stock |
| sales_ledger.csv | POS sales history |
| purchase_ledger.csv | Purchase history |
| rates.csv | Product pricing |
| processed_data.pkl | Extracted ML features |
| retail_model.pkl | Trained ML model |

---

# PostgreSQL Integration

Currently PostgreSQL is used only for:
- Saving inventory stock backup

Main system operations still use CSV-based storage.

---

# Installation

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

---

# Current Limitations

## 1. CSV-Based Architecture
Most of the system currently depends on CSV files instead of a complete database system.

## 2. Single User Application
No multi-user handling currently exists.

## 3. No Authentication
The project does not include login or access control.

## 4. Product Name Matching Issues
Inventory matching depends on consistent product names.

Example:
```text
Egg
egg
Egg 
```

can create mismatches if cleaning is inconsistent.

## 5. Prediction Accuracy Depends on Dataset Quality
Forecasting performance depends heavily on clean and structured sales data.

## 6. POS System Limitations
Current POS does not support:
- Barcode scanning
- Receipt printing
- Multi-payment methods
- Tax invoice printing

## 7. Weekly & Monthly Graph Issues
Graph inconsistencies may occur because of:
- Incorrect date formatting
- Empty filters
- Missing date records

## 8. Manual Model Retraining
The ML model must be retrained manually after uploading new datasets.

## 9. Inventory Accuracy Depends on Purchases
Incorrect or incomplete purchase uploads can affect stock accuracy.

---

# Errors Encountered During Development

## CSV Parsing Errors

Example:
```text
ParserError: Expected 2 fields in line X, saw 3
```

Cause:
- Broken CSV rows
- Extra commas
- Invalid formatting

---

## Pickle Loading Errors

Example:
```text
_pickle.UnpicklingError
```

Cause:
- Corrupted `.pkl` file
- Invalid model loading

---

## Inventory Showing 0 Stock

Problem:
- Prediction page showed 0 stock even when stock existed.

Cause:
- Product name mismatch

Fix:
- Added product cleaning using:
```python
str.strip().lower()
```

---

## Empty Monthly Graphs

Cause:
- Invalid datetime conversion
- Incorrect month extraction
- Empty filters

---

## POS Price Mapping Errors

Cause:
- Product names between inventory and sales dataset did not match.

Fix:
- Added `rates.csv` mapping system.

---

# Future Improvements

- Full PostgreSQL integration
- Multi-user authentication
- Cloud deployment
- Barcode support
- Auto ML retraining
- Real-time inventory sync
- Supplier management
- AI recommendations

---

# Development Note

Most of the implementation code in this project was generated with the assistance of ChatGPT, while the overall system logic, workflow decisions, debugging process, feature planning, and project architecture were guided and designed manually by the developer.

---

# Author

Alan Kurian Joy

---

# License

This project is developed for educational and research purposes only.