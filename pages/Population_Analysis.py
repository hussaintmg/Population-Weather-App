import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sidebar title
with st.sidebar:
    st.markdown(
        "<h2 style='color:white; margin-top: 0;'>Population Dashboard</h2>",
        unsafe_allow_html=True
    )

st.title("📊 Population Analysis")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("./data/pakistan_data.csv")
    # Ensure numeric columns are numeric
    df["ALL SEXES (RURAL)"] = pd.to_numeric(df["ALL SEXES (RURAL)"], errors="coerce").fillna(0)
    df["ALL SEXES (URBAN)"] = pd.to_numeric(df["ALL SEXES (URBAN)"], errors="coerce").fillna(0)
    # Total population column
    df["TOTAL_POPULATION"] = df["ALL SEXES (RURAL)"] + df["ALL SEXES (URBAN)"]
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

districts = st.sidebar.multiselect(
    "Select Districts",
    options=df["DISTRICT"].unique(),
    default=df["DISTRICT"].unique()
)

provinces = st.sidebar.multiselect(
    "Select Provinces",
    options=df["PROVINCE"].unique(),
    default=df["PROVINCE"].unique()
)

# Filter data
filtered_df = df[
    (df["DISTRICT"].isin(districts)) &
    (df["PROVINCE"].isin(provinces))
]

# Summary Cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Population", f"{filtered_df['TOTAL_POPULATION'].sum():,}")
col2.metric("Average Population", f"{int(filtered_df['TOTAL_POPULATION'].mean()):,}")
col3.metric("Districts Selected", len(filtered_df["DISTRICT"].unique()))

# Population Trend Bar Chart (Rural vs Urban)
st.subheader("Population Distribution (Rural vs Urban)")

pop_df = filtered_df.groupby("DISTRICT")[["ALL SEXES (RURAL)", "ALL SEXES (URBAN)"]].sum()

fig, ax = plt.subplots(figsize=(12,80))
pop_df.plot(kind="barh", stacked=True, ax=ax, color=["#1f77b4", "#ff7f0e"])
ax.set_ylabel("District")
ax.set_xlabel("Population")
ax.set_title("Rural and Urban Population by District")
st.pyplot(fig)

# Top 10 Populated Districts
st.subheader("Top 10 Populated Districts")

top_districts = filtered_df.groupby("DISTRICT")["TOTAL_POPULATION"].sum().sort_values(ascending=False).head(10)

fig2, ax2 = plt.subplots(figsize=(10,4))
top_districts.plot(kind="bar", ax=ax2, color="#2ca02c")
ax2.set_ylabel("Population")
ax2.set_xlabel("District")
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
ax2.set_title("Top 10 Districts by Total Population")
st.pyplot(fig2)

# Show filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Download Button
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_population.csv", "text/csv")
