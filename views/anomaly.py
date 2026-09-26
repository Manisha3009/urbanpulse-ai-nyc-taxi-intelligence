
import numpy as np
import pandas as pd
import streamlit as st

from utils import load_model


st.title(
    "⚠️ Trip Anomaly Detection"
)


bundle = load_model(
    "taxi_anomaly_model.pkl"
)

model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]


distance = st.number_input(
    "Trip Distance",
    min_value=0.1,
    value=5.0
)

fare = st.number_input(
    "Fare Amount",
    min_value=0.0,
    value=20.0
)

total = st.number_input(
    "Total Amount",
    min_value=0.0,
    value=25.0
)

tip = st.number_input(
    "Tip Amount",
    min_value=0.0,
    value=3.0
)

duration = st.number_input(
    "Trip Duration (minutes)",
    min_value=1.0,
    value=20.0
)


speed = (
    distance /
    (duration / 60)
)

fare_per_mile = (
    fare / distance
)

revenue_per_minute = (
    total / duration
)


if st.button(
    "Analyze Trip",
    type="primary"
):

    row = {

        "trip_distance":
            distance,

        "fare_amount":
            fare,

        "total_amount":
            total,

        "tip_amount":
            tip,

        "trip_duration_minutes":
            duration,

        "avg_speed_mph":
            speed,

        "fare_per_mile":
            fare_per_mile,

        "revenue_per_minute":
            revenue_per_minute
    }


    X = pd.DataFrame(
        [row]
    )[features]


    X_scaled = (
        scaler
        .transform(
            X.values
        )
    )


    prediction = int(
        model.predict(
            X_scaled
        )[0]
    )


    score = float(
        -model
        .decision_function(
            X_scaled
        )[0]
    )


    st.metric(
        "Anomaly Score",
        f"{score:.3f}"
    )


    if prediction == -1:

        st.error(
            "Suspicious Trip Detected"
        )

    else:

        st.success(
            "Normal Trip"
        )


    st.write(
        f"Average Speed: {speed:.2f} mph"
    )

    st.write(
        f"Fare / Mile: ${fare_per_mile:.2f}"
    )
