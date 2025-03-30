from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt


@st.cache_data
def load_data():
    src_file = Path.cwd() / ".." / "code" / "data" / "raw" / "EPA_fuel_economy_summary.csv"
    raw_df = pd.read_csv(src_file)
    return raw_df


df = load_data()
min_year = int(df["year"].min())
max_year = int(df["year"].max())
valid_makes = sorted(df["make"].unique())

# set up the UI
make = st.multiselect("Select a make:", valid_makes)
year_range = st.slider(
    label="Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

# Filter data based on inputs
year_filter = df["year"].between(year_range[0], year_range[1])
make_filter = df["make"].isin(make)

plot_df = df[make_filter & year_filter]

avg_fuel_economy = round(plot_df["fuelCost08"].mean(), 0)
st.metric("Average", avg_fuel_economy)

# Plot the data
fig = px.histogram(
    plot_df,
    x="fuelCost08",
    color="class_summary",
    labels={"fuelCost08": "Annual Fuel Cost"},
    nbins = 40,
    title="Fuel Cost Distribution"
)

altair_chart = (
    alt.Chart(plot_df).mark_tick().encode(y="fuel_type_summary", x="barrels08")
)
st.write(fig)
st.write(altair_chart)

st.write("Sample data", plot_df.head(10))
