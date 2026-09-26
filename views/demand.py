
import datetime as dt

import numpy as np
import pandas as pd
import streamlit as st

from utils import (
    load_model,
    load_latest_features
)


st.title("📈 Taxi Demand Forecast")

st.info(
    "Forecast uses the latest historical station-demand "
    "state and the trained Phase 4 demand model."
)


bundle = load_model(
    "taxi_demand_model.pkl"
)

model = bundle["model"]

preprocessor = bundle[
    "preprocessor"
]

feature_columns = bundle[
    "feature_columns"
]


df = load_latest_features()


df["station_label"] = (
    df["pickup_zone"].fillna("Unknown")
    + " | "
    + df["pickup_borough"].fillna("Unknown")
    + " | ID "
    + df["PULocationID"].astype(str)
)


selected_index = st.selectbox(

    "Select Pickup Zone",

    options=df.index,

    format_func=lambda i:
        df.loc[i, "station_label"]
)


row = df.loc[
    [selected_index]
].copy()


latest_time = pd.to_datetime(
    df["timestamp"]
).max()


forecast_date = st.date_input(
    "Forecast Date",
    value=latest_time.date()
)


forecast_hour = st.slider(
    "Forecast Hour",
    0,
    23,
    int(latest_time.hour)
)


forecast_dt = pd.Timestamp(
    dt.datetime.combine(
        forecast_date,
        dt.time(
            hour=forecast_hour
        )
    )
)


# Calendar features

row["pickup_hour"] = (
    forecast_dt.hour
)

row["day_of_week"] = (
    forecast_dt.dayofweek
)

row["day"] = (
    forecast_dt.day
)

row["is_weekend"] = int(
    forecast_dt.dayofweek
    in [5, 6]
)


# Cyclical features

row["hour_sin"] = np.sin(
    2 * np.pi *
    forecast_dt.hour / 24
)

row["hour_cos"] = np.cos(
    2 * np.pi *
    forecast_dt.hour / 24
)

row["dow_sin"] = np.sin(
    2 * np.pi *
    forecast_dt.dayofweek / 7
)

row["dow_cos"] = np.cos(
    2 * np.pi *
    forecast_dt.dayofweek / 7
)


if st.button(
    "Predict Demand",
    type="primary"
):

    X = row[
        feature_columns
    ]

    X_t = (
        preprocessor
        .transform(X)
    )

    prediction = float(
        model.predict(X_t)[0]
    )

    prediction = max(
        prediction,
        0
    )

    st.metric(
        "Predicted Taxi Demand",
        f"{prediction:.0f} trips"
    )

    if prediction >= 50:

        st.error(
            "High-demand zone"
        )

    elif prediction >= 20:

        st.warning(
            "Moderate-demand zone"
        )

    else:

        st.success(
            "Low-demand zone"
        )


st.subheader(
    "Demand Drivers"
)

st.write(
    row[
        [
            "lag_1",
            "lag_3",
            "lag_24",
            "lag_168",
            "rolling_3h",
            "rolling_24h"
        ]
    ]
)
