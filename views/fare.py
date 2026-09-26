
import pandas as pd
import streamlit as st

from utils import (
    load_model,
    run_query
)


st.title("💵 Taxi Fare Prediction")


bundle = load_model(
    "taxi_fare_model.pkl"
)

model = bundle["model"]

preprocessor = bundle[
    "preprocessor"
]

features = bundle[
    "features"
]


pickup = run_query("""
SELECT DISTINCT

    pickup_location_id,
    pickup_zone

FROM dim_pickup_zone

WHERE pickup_zone != 'Unknown'

ORDER BY pickup_zone
""")


dropoff = run_query("""
SELECT DISTINCT

    dropoff_location_id,
    dropoff_zone

FROM dim_dropoff_zone

WHERE dropoff_zone != 'Unknown'

ORDER BY dropoff_zone
""")


pickup_idx = st.selectbox(
    "Pickup Zone",
    pickup.index,
    format_func=lambda x:
        pickup.loc[x, "pickup_zone"]
)


dropoff_idx = st.selectbox(
    "Drop-off Zone",
    dropoff.index,
    format_func=lambda x:
        dropoff.loc[x, "dropoff_zone"]
)


distance = st.number_input(
    "Trip Distance (miles)",
    min_value=0.1,
    value=3.0
)


passengers = st.slider(
    "Passengers",
    1,
    6,
    1
)


hour = st.slider(
    "Pickup Hour",
    0,
    23,
    12
)


weekday = st.selectbox(
    "Day of Week",
    options=list(range(7)),
    format_func=lambda x:
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ][x]
)


duration = st.number_input(
    "Estimated Duration (minutes)",
    min_value=1.0,
    value=15.0
)


if st.button(
    "Estimate Fare",
    type="primary"
):

    input_df = pd.DataFrame([{

        "trip_distance":
            distance,

        "passenger_count":
            passengers,

        "pickup_hour":
            hour,

        "day_of_week":
            weekday,

        "is_weekend":
            int(
                weekday in [5, 6]
            ),

        "PULocationID":
            int(
                pickup.loc[
                    pickup_idx,
                    "pickup_location_id"
                ]
            ),

        "DOLocationID":
            int(
                dropoff.loc[
                    dropoff_idx,
                    "dropoff_location_id"
                ]
            ),

        "trip_duration_minutes":
            duration,

        "is_rush_hour":
            int(
                hour in [
                    7,8,9,
                    16,17,18,19
                ]
            ),

        "is_night_trip":
            int(
                hour in [
                    22,23,
                    0,1,2,3,4
                ]
            )
    }])


    X = input_df[
        features
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
        "Estimated Fare",
        f"${prediction:.2f}"
    )
