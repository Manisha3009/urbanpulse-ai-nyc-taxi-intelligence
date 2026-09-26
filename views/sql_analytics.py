
import streamlit as st

from utils import run_query


st.title("🗄️ Advanced SQL Analytics")


analysis = st.selectbox(
    "Select Analysis",
    [
        "Top Pickup Zones",
        "Peak Hours",
        "Revenue by Borough",
        "Payment Analysis",
        "Rush Hour Analysis",
        "Zone Ranking"
    ]
)


if analysis == "Top Pickup Zones":

    query = """
    SELECT
        pickup_zone,
        COUNT(*) AS trips,
        SUM(total_amount) AS revenue

    FROM fact_trips

    WHERE pickup_zone != 'Unknown'

    GROUP BY pickup_zone

    ORDER BY trips DESC

    LIMIT 20
    """


elif analysis == "Peak Hours":

    query = """
    SELECT
        pickup_hour,
        COUNT(*) AS trips

    FROM fact_trips

    GROUP BY pickup_hour

    ORDER BY trips DESC
    """


elif analysis == "Revenue by Borough":

    query = """
    SELECT
        pickup_borough,
        COUNT(*) AS trips,
        SUM(total_amount) AS revenue,
        AVG(fare_amount) AS avg_fare

    FROM fact_trips

    WHERE pickup_borough != 'Unknown'

    GROUP BY pickup_borough

    ORDER BY revenue DESC
    """


elif analysis == "Payment Analysis":

    query = """
    SELECT

        CASE
            WHEN payment_type = 1 THEN 'Credit Card'
            WHEN payment_type = 2 THEN 'Cash'
            WHEN payment_type = 3 THEN 'No Charge'
            WHEN payment_type = 4 THEN 'Dispute'
            WHEN payment_type = 5 THEN 'Unknown'
            WHEN payment_type = 6 THEN 'Voided'
            ELSE 'Other'
        END AS payment_method,

        COUNT(*) AS trips,

        AVG(tip_amount) AS avg_tip,

        SUM(total_amount) AS revenue

    FROM fact_trips

    GROUP BY payment_type

    ORDER BY trips DESC
    """


elif analysis == "Rush Hour Analysis":

    query = """
    SELECT

        CASE
            WHEN is_rush_hour = 1
            THEN 'Rush Hour'
            ELSE 'Non-Rush Hour'
        END AS period,

        COUNT(*) AS trips,

        AVG(fare_amount) AS avg_fare,

        AVG(trip_duration_minutes)
            AS avg_duration

    FROM fact_trips

    GROUP BY period
    """


else:

    query = """
    SELECT

        pickup_borough,
        pickup_zone,

        COUNT(*) AS trips,

        RANK() OVER (
            PARTITION BY pickup_borough
            ORDER BY COUNT(*) DESC
        ) AS zone_rank

    FROM fact_trips

    WHERE pickup_borough != 'Unknown'

    GROUP BY
        pickup_borough,
        pickup_zone

    ORDER BY
        pickup_borough,
        zone_rank
    """


result = run_query(
    query
)

st.dataframe(
    result,
    width="stretch"
)

st.caption(
    "DuckDB SQL query executed on the "
    "million-scale processed trip warehouse."
)
