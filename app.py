import streamlit as st

# ------------------- Custom Sidebar Styling -------------------
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #2f302f;
        width: 270px;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff;
        font-size: 16px;
    }
    button[kind="header"] {
        background-color: #1f1f1f !important;
        color: white !important;
    }
    .css-1oe5cao {
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Pages -------------------
page_1 = st.Page("./pages/Population_Analysis.py", title="Population Analysis", icon="📊")
page_2 = st.Page("./pages/Weather_Analysis.py", title="Weather Analysis", icon="🌡️")

# ------------------- Navigation -------------------
pg = st.navigation([page_1, page_2])
pg.run()
