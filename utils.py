

# utils.py

import pandas as pd
import numpy as np


# ---------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------

def engineer_features(
    df,
    date_col,
    product_col,
    qty_col,
    price_col,
    gst_col=None
):

    df = df.copy()

    # ---------------------------------------------------
    # CLEAN COLUMN NAMES
    # ---------------------------------------------------

    df.columns = df.columns.str.strip()

    # ---------------------------------------------------
    # DATE FIX
    # ---------------------------------------------------

    df[date_col] = pd.to_datetime(
        df[date_col],
        dayfirst=True,
        errors="coerce"
    )

    # ---------------------------------------------------
    # NUMERIC CONVERSION
    # ---------------------------------------------------

    df[qty_col] = pd.to_numeric(
        df[qty_col],
        errors="coerce"
    )

    df[price_col] = pd.to_numeric(
        df[price_col],
        errors="coerce"
    )

    # GST OPTIONAL
    if gst_col and gst_col in df.columns:

        df[gst_col] = pd.to_numeric(
            df[gst_col],
            errors="coerce"
        ).fillna(0)

    # ---------------------------------------------------
    # REMOVE INVALID ROWS
    # ---------------------------------------------------

    df = df.dropna(
        subset=[
            date_col,
            qty_col,
            price_col
        ]
    )

    # ---------------------------------------------------
    # SORT
    # ---------------------------------------------------

    df = df.sort_values(
        [product_col, date_col]
    )

    # ---------------------------------------------------
    # REVENUE CALCULATION
    # ---------------------------------------------------

    # BEFORE GST
    df["Taxable Amount"] = (
        df[qty_col] *
        df[price_col]
    )

    # GST
    if gst_col and gst_col in df.columns:

        df["GST Amount"] = (
            df["Taxable Amount"] *
            df[gst_col] / 100
        )

    else:

        df["GST Amount"] = 0

    # FINAL REVENUE
    df["Net Amount"] = (
        df["Taxable Amount"] +
        df["GST Amount"]
    )

    # ---------------------------------------------------
    # DATE FEATURES
    # ---------------------------------------------------

    df["month"] = (
        df[date_col].dt.month
    )

    df["day"] = (
        df[date_col].dt.day
    )

    df["day_of_week"] = (
        df[date_col].dt.dayofweek
    )

    df["week"] = (
        df[date_col]
        .dt.isocalendar()
        .week.astype(int)
    )

    df["is_weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    # ---------------------------------------------------
    # LAG FEATURES
    # ---------------------------------------------------

    df["lag_1"] = (
        df.groupby(product_col)[qty_col]
        .shift(1)
    )

    df["lag_7"] = (
        df.groupby(product_col)[qty_col]
        .shift(7)
    )

    # ---------------------------------------------------
    # TREND FEATURES
    # ---------------------------------------------------

    df["trend_3"] = (
        df.groupby(product_col)[qty_col]
        .transform(
            lambda x:
            x.rolling(3).mean().shift(1)
        )
    )

    df["trend_7"] = (
        df.groupby(product_col)[qty_col]
        .transform(
            lambda x:
            x.rolling(7).mean().shift(1)
        )
    )

    # ---------------------------------------------------
    # LOG FEATURES
    # ---------------------------------------------------

    df["log_price"] = np.log1p(
        df[price_col]
    )

    df["log_qty"] = np.log1p(
        df[qty_col]
    )

    # ---------------------------------------------------
    # PRICE FEATURES
    # ---------------------------------------------------

    df["avg_price"] = (
        df.groupby(product_col)[price_col]
        .transform("mean")
    )

    df["price_ratio"] = (
        df[price_col] /
        (df["avg_price"] + 1e-6)
    )

    # ---------------------------------------------------
    # PRODUCT ID
    # ---------------------------------------------------

    df["prod_id"] = (
        df[product_col]
        .astype("category")
        .cat.codes
    )

    # ---------------------------------------------------
    # REMOVE NULLS CREATED BY LAGS
    # ---------------------------------------------------

    df = df.dropna()

    return df


# ---------------------------------------------------
# FAST / SLOW PRODUCT CLASSIFICATION
# ---------------------------------------------------

def classify_product(speed):

    if speed >= 50:

        return "🔥 Fast Moving"

    elif speed >= 20:

        return "⚡ Medium Moving"

    else:

        return "🐢 Slow Moving"


# ---------------------------------------------------
# EXTREME PRICE DETECTION
# ---------------------------------------------------

def is_extreme_price(
    price,
    data,
    price_col
):

    mean = data[price_col].mean()

    std = data[price_col].std()

    return price > mean + (3 * std)


# ---------------------------------------------------
# NEXT WEEK FORECAST
# ---------------------------------------------------

def generate_week_forecast(
    model,
    latest_row,
    price_col
):

    predictions = []

    lag = latest_row["lag_1"]

    for i in range(7):

        row = [[
            latest_row["prod_id"],
            latest_row[price_col],
            np.log1p(
                latest_row[price_col]
            ),
            latest_row["price_ratio"],
            latest_row["month"],
            latest_row["day"],
            latest_row["week"],
            latest_row["day_of_week"],
            latest_row["is_weekend"],
            lag,
            latest_row["lag_7"],
            latest_row["trend_3"],
            latest_row["trend_7"]
        ]]

        pred_log = model.predict(row)[0]

        pred = int(
            np.expm1(pred_log)
        )

        predictions.append(pred)

        lag = pred

    return predictions

