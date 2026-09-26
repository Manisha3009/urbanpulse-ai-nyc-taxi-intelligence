
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import load_model


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


st.title(
    "🧠 Machine Learning Performance"
)


# Demand Metrics

st.subheader(
    "Demand Forecasting"
)

demand_metrics = pd.read_csv(
    BASE_DIR /
    "demand_model_metrics.csv"
)

st.dataframe(
    demand_metrics,
    width="stretch"
)


# Fare metrics

st.subheader(
    "Fare Prediction Models"
)

fare_metrics = pd.read_csv(
    BASE_DIR /
    "fare_model_metrics.csv"
)

st.dataframe(
    fare_metrics,
    width="stretch"
)


fig = px.bar(
    fare_metrics,
    x="Model",
    y="RMSE",
    title="Fare Model RMSE Comparison"
)

st.plotly_chart(
    fig,
    width="stretch"
)


# Demand Feature Importance

st.subheader(
    "Demand Model Feature Importance"
)

bundle = load_model(
    "taxi_demand_model.pkl"
)

model = bundle["model"]

preprocessor = bundle[
    "preprocessor"
]


try:

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )


    importance = pd.DataFrame({

        "Feature":
            feature_names,

        "Importance":
            model.feature_importances_
    })


    top = (
        importance
        .sort_values(
            "Importance",
            ascending=False
        )
        .head(20)
    )


    fig2 = px.bar(
        top,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 20 Demand Features"
    )


    fig2.update_layout(
        yaxis={
            "categoryorder":
            "total ascending"
        }
    )


    st.plotly_chart(
        fig2,
        width="stretch"
    )


except Exception as e:

    st.warning(
        f"Feature importance unavailable: {e}"
    )
