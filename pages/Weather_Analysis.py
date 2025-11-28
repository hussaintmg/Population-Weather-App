import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Weather Analysis", layout="wide")
st.title("🌡️ Weather Analysis Dashboard")

# Sidebar title
with st.sidebar:
    st.markdown(
        "<h2 style='color:white; margin-top: 0;'>Weather Dashboard</h2>",
        unsafe_allow_html=True
    )

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("./data/pakistan_weather_data.csv")
    
    # Fix datetime column: convert YYYY-MM-DD:HH to proper datetime
    df['datetime'] = pd.to_datetime(df['datetime'].str.replace(":", " "), format='%Y-%m-%d %H', errors='coerce')
    
    # Convert other datetime columns
    df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'], errors='coerce')
    df['timestamp_local'] = pd.to_datetime(df['timestamp_local'], errors='coerce')
    
    # Drop rows with invalid datetime
    df = df.dropna(subset=['datetime'])
    
    # Ensure numeric columns
    numeric_cols = [
        'solar_rad','slp','ts','dewpt','uv','wind_gust_spd','ghi','dhi','precip',
        'pop','ozone','app_temp','clouds_low','clouds_mid','snow_depth','dni',
        'rh','pres','snow','temp','clouds','vis','clouds_hi','wind_spd'
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
cities = st.sidebar.multiselect(
    "Select Cities",
    options=df["city"].unique(),
    default=df["city"].unique()
)
countries = st.sidebar.multiselect(
    "Select Countries",
    options=df["country"].unique(),
    default=df["country"].unique()
)

# Date input fix: ensure valid datetime.date
if df.empty:
    st.warning("No valid datetime data found!")
else:
    min_date = df['datetime'].min().date()
    max_date = df['datetime'].max().date()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Filter Data
filtered_df = df[
    (df["city"].isin(cities)) &
    (df["country"].isin(countries)) &
    (df["datetime"].dt.date >= date_range[0]) &
    (df["datetime"].dt.date <= date_range[1])
]

# Summary Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Avg Temp (°C)", f"{filtered_df['temp'].mean():.2f}")
col2.metric("Avg Humidity (%)", f"{filtered_df['rh'].mean():.2f}")
col3.metric("Total Precipitation (mm)", f"{filtered_df['precip'].sum():.2f}")
col4.metric("Avg Wind Speed (m/s)", f"{filtered_df['wind_spd'].mean():.2f}")
col5.metric("Avg Solar Radiation", f"{filtered_df['solar_rad'].mean():.2f}")

# Temperature Trend
st.subheader("Temperature Trend Over Time")
fig, ax = plt.subplots(figsize=(12,6))
for city in filtered_df["city"].unique():
    city_data = filtered_df[filtered_df["city"] == city]
    ax.plot(city_data["datetime"], city_data["temp"], label=city)
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature Trend by City")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Precipitation Trend
st.subheader("Precipitation Trend Over Time")
fig2, ax2 = plt.subplots(figsize=(12,6))
for city in filtered_df["city"].unique():
    city_data = filtered_df[filtered_df["city"] == city]
    ax2.plot(city_data["datetime"], city_data["precip"], label=city)
ax2.set_xlabel("Date")
ax2.set_ylabel("Precipitation (mm)")
ax2.set_title("Precipitation Trend by City")
ax2.legend()
plt.xticks(rotation=45)
st.pyplot(fig2)

# Correlation Heatmap
st.subheader("Weather Parameters Correlation")
numeric_cols = [
    'temp','app_temp','dewpt','rh','precip','wind_spd','wind_gust_spd',
    'solar_rad','slp','uv','pop','ozone','dni','ghi','dhi'
]
corr_df = filtered_df[numeric_cols]
fig3, ax3 = plt.subplots(figsize=(10,8))
sns.heatmap(corr_df.corr(), annot=True, cmap="coolwarm", ax=ax3)
st.pyplot(fig3)

# Filtered Data Table
st.subheader("Filtered Weather Data")
st.dataframe(filtered_df)

# Download CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_weather.csv", "text/csv")
