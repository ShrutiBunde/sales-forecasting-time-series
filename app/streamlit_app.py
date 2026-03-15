import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

st.title("Sales Forecasting Dashboard")

# Load dataset
df = pd.read_csv("data/retail_sales.csv")

df['date'] = pd.to_datetime(df['date'])

# Store and item selection
store = st.selectbox("Select Store", df['store_id'].unique())
item = st.selectbox("Select Item", df['item_id'].unique())

# Filter data
filtered_df = df[(df['store_id'] == store) & (df['item_id'] == item)]

# Create time series
item_sales = filtered_df.groupby('date')['sales'].sum().reset_index()

# Prepare for Prophet
prophet_df = item_sales.rename(columns={"date": "ds", "sales": "y"})

# Train model
model = Prophet()
model.fit(prophet_df)

# Forecast future
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

st.subheader("Sales Forecast")

fig1 = model.plot(forecast)
st.pyplot(fig1)

st.subheader("Seasonality Components")

fig2 = model.plot_components(forecast)
st.pyplot(fig2)