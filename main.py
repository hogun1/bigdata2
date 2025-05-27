python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
streamlit run app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Title and description
st.title("Seoul Bike Rentals Analysis")
st.markdown("Interactive visualization of Seoul public bike rentals using Plotly and Streamlit.")

# Load data
@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path, parse_dates=['date'])
    return df

data = load_data('data/seoul_bike_data.csv')

# Sidebar filters
st.sidebar.header("Filters")
min_date, max_date = data['date'].min(), data['date'].max()
date_range = st.sidebar.date_input(
    "Select date range", [min_date, max_date],
    min_value=min_date, max_value=max_date
)
if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))
    filtered = data.loc[mask]
else:
    filtered = data.copy()

# Time Series Plot
st.subheader("Daily Rental Counts")
if not filtered.empty:
    ts = filtered.groupby('date')['rental_count'].sum().reset_index()
    fig_ts = px.line(ts, x='date', y='rental_count', title='Daily Rental Counts Over Time')
    st.plotly_chart(fig_ts, use_container_width=True)
else:
    st.warning("No data in selected range.")

# Scatter Plot with Regression
st.subheader("Temperature vs. Rental Count")
fig_scatter = px.scatter(
    filtered, x='avg_temp', y='rental_count',
    trendline='ols', title='Avg Temperature vs. Rentals'
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Additional Insights
st.subheader("Statistical Summary")
st.write(filtered[['rental_count', 'avg_temp', 'humidity', 'wind_speed']].describe())
