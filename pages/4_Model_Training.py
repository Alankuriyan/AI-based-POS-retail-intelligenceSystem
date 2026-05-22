# pages/3_Model_Training.py

import streamlit as st
import pandas as pd
import joblib
import os

from xgboost import XGBRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from utils import engineer_features

st.title("Model Training")

# ---------------------------------------------------
# CHECK DATA
# ---------------------------------------------------

if "raw_df" not in st.session_state:

    st.warning(
        "⚠ Upload dataset first"
    )

else:

    df = st.session_state["raw_df"]

    cols = df.columns.tolist()

    # ---------------------------------------------------
    # COLUMN SELECTION
    # ---------------------------------------------------

    prod_col = st.selectbox(
        "Product Column",
        cols
    )

    date_col = st.selectbox(
        "Date Column",
        cols
    )

    qty_col = st.selectbox(
        "Quantity Column",
        cols
    )

    price_col = st.selectbox(
        "Price Column",
        cols
    )

    # ---------------------------------------------------
    # TRAIN BUTTON
    # ---------------------------------------------------

    if st.button(" Train XGBoost"):

        # ---------------------------------------------------
        # NUMERIC FIX
        # ---------------------------------------------------

        df[qty_col] = pd.to_numeric(
            df[qty_col],
            errors="coerce"
        )

        df[price_col] = pd.to_numeric(
            df[price_col],
            errors="coerce"
        )

        # ---------------------------------------------------
        # PRODUCT ID
        # ---------------------------------------------------

        df["prod_id"] = (
            df[prod_col]
            .astype("category")
            .cat.codes
        )

        # ---------------------------------------------------
        # FEATURE ENGINEERING
        # ---------------------------------------------------

        data = engineer_features(
            df,
            date_col,
            prod_col,
            qty_col,
            price_col
        )

        # ---------------------------------------------------
        # FEATURES
        # ---------------------------------------------------

        features = [

            "prod_id",

            price_col,

            "log_price",

            "price_ratio",

            "month",

            "day",

            "week",

            "day_of_week",

            "is_weekend",

            "lag_1",

            "lag_7",

            "trend_3",

            "trend_7"
        ]

        # ---------------------------------------------------
        # X AND Y
        # ---------------------------------------------------

        X = data[features]

        y = data["log_qty"]

        # ---------------------------------------------------
        # TRAIN TEST SPLIT
        # ---------------------------------------------------

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )
        )

        # ---------------------------------------------------
        # MODEL
        # ---------------------------------------------------

        model = XGBRegressor(

            n_estimators=300,

            learning_rate=0.05,

            max_depth=6,

            random_state=42
        )

        # ---------------------------------------------------
        # TRAIN MODEL
        # ---------------------------------------------------

        model.fit(
            X_train,
            y_train
        )

        # ---------------------------------------------------
        # PREDICT
        # ---------------------------------------------------

        pred = model.predict(
            X_test
        )

        acc = r2_score(
            y_test,
            pred
        )

        # ---------------------------------------------------
        # CREATE MODELS FOLDER
        # ---------------------------------------------------

        os.makedirs(
            "models",
            exist_ok=True
        )

        # ---------------------------------------------------
        # SAVE MODEL
        # ---------------------------------------------------

        joblib.dump(
            model,
            "models/retail_model.pkl"
        )

        # ---------------------------------------------------
        # SAVE PROCESSED DATA
        # ---------------------------------------------------

        joblib.dump(
            data,
            "models/processed_data.pkl"
        )

        # ---------------------------------------------------
        # SAVE METADATA
        # ---------------------------------------------------

        metadata = {

            "prod_col": prod_col,

            "date_col": date_col,

            "qty_col": qty_col,

            "price_col": price_col,

            "features": features
        }

        joblib.dump(
            metadata,
            "models/metadata.pkl"
        )

        # ---------------------------------------------------
        # SAVE SESSION STATE
        # ---------------------------------------------------

        st.session_state["model"] = model

        st.session_state["data"] = data

        st.session_state["prod_col"] = prod_col

        st.session_state["date_col"] = date_col

        st.session_state["qty_col"] = qty_col

        st.session_state["price_col"] = price_col

        st.session_state["features"] = features

        # ---------------------------------------------------
        # SUCCESS
        # ---------------------------------------------------

        st.success(
            f"✅ Model Saved Successfully | Accuracy: {round(acc, 3)}"
        )