
import streamlit as st


st.set_page_config(
    page_title="UrbanPulse AI",
    page_icon="🚕",
    layout="wide"
)


home = st.Page(
    "views/home.py",
    title="Executive Overview",
    icon="🏠",
    default=True
)

demand = st.Page(
    "views/demand.py",
    title="Demand Forecast",
    icon="📈"
)

fare = st.Page(
    "views/fare.py",
    title="Fare Prediction",
    icon="💵"
)

anomaly = st.Page(
    "views/anomaly.py",
    title="Anomaly Detection",
    icon="⚠️"
)

sql = st.Page(
    "views/sql_analytics.py",
    title="SQL Analytics",
    icon="🗄️"
)

models = st.Page(
    "views/models.py",
    title="ML Performance",
    icon="🧠"
)


pg = st.navigation([
    home,
    demand,
    fare,
    anomaly,
    sql,
    models
])

pg.run()
