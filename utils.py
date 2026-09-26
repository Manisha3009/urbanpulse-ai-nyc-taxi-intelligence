
from pathlib import Path

import duckdb
import joblib
import pandas as pd
import requests
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent


@st.cache_resource
def load_model(filename):

    path = BASE_DIR / filename

    return joblib.load(path)


@st.cache_data
def load_latest_features():

    path = BASE_DIR / "latest_demand_features.parquet"

    return pd.read_parquet(path)


@st.cache_data(ttl=600)
def get_live_weather():

    url = "https://api.open-meteo.com/v1/forecast"

    params = {

        "latitude": 40.7128,
        "longitude": -74.0060,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "rain",
            "weather_code",
            "wind_speed_10m"
        ],

        "timezone": "America/New_York"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()["current"]


@st.cache_data(ttl=600)
def run_query(sql):

    db_path = BASE_DIR / "urbanpulse_deploy.db"

    con = duckdb.connect(
        str(db_path),
        read_only=True
    )

    try:
        result = con.execute(sql).df()

    finally:
        con.close()

    return result
