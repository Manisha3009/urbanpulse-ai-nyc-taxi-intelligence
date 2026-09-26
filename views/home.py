
import streamlit as st
import plotly.express as px

from utils import (
    run_query,
    get_live_weather
)


st.title("🚕 UrbanPulse AI")

st.caption(
    "NYC Taxi Demand, Fare Prediction & "
    "Anomaly Intelligence Platform"
)


# =====================
# KPIs
# =====================

kpi = run_query("""
SELECT

    COUNT(*) AS total_trips,

    SUM(total_amount) AS revenue,

    AVG(fare_amount) AS avg_fare,

    AVG(trip_distance) AS avg_distance

FROM fact_trips
""").iloc[0]


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Trips",
    f"{int(kpi['total_trips']):,}"
)

c2.metric(
    "Total Revenue",
    f"${kpi['revenue']:,.0f}"
)

c3.metric(
    "Average Fare",
    f"${kpi['avg_fare']:.2f}"
)

c4.metric(
    "Average Distance",
    f"{kpi['avg_distance']:.2f} mi"
)


# =====================
# WEATHER
# =====================

st.subheader("🌦 Live NYC Weather")

try:

    weather = get_live_weather()

    w1, w2, w3, w4 = st.columns(4)

    w1.metric(
        "Temperature",
        f"{weather['temperature_2m']} °C"
    )

    w2.metric(
        "Humidity",
        f"{weather['relative_humidity_2m']}%"
    )

    w3.metric(
        "Rain",
        f"{weather['rain']} mm"
    )

    w4.metric(
        "Wind",
        f"{weather['wind_speed_10m']} km/h"
    )

except Exception as e:

    st.warning(
        f"Weather unavailable: {e}"
    )


# =====================
# TOP ZONES
# =====================

st.subheader("📍 Highest Demand Pickup Zones")

top_zones = run_query("""
SELECT

    pickup_zone,

    COUNT(*) AS trips

FROM fact_trips

WHERE pickup_zone != 'Unknown'

GROUP BY pickup_zone

ORDER BY trips DESC

LIMIT 10
""")


fig = px.bar(
    top_zones,
    x="trips",
    y="pickup_zone",
    orientation="h",
    title="Top 10 Pickup Zones"
)

fig.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig,
    width="stretch"
)


# =====================
# HOURLY DEMAND
# =====================

hourly = run_query("""
SELECT

    pickup_hour,

    COUNT(*) AS trips

FROM fact_trips

GROUP BY pickup_hour

ORDER BY pickup_hour
""")


fig2 = px.line(
    hourly,
    x="pickup_hour",
    y="trips",
    markers=True,
    title="Taxi Demand by Hour"
)

st.plotly_chart(
    fig2,
    width="stretch"
)
