
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Nassau Candy Optimization",
    page_icon="🏭",
    layout="wide"
)

# Load saved analysis files
df = pd.read_csv("nassau_data.csv")
recommendations = pd.read_csv("factory_recommendations.csv")
models = pd.read_csv("model_results.csv")
risk = pd.read_csv("risk_analysis.csv")
scenarios = pd.read_csv("scenario_analysis.csv")

# Dashboard title
st.title("🏭 Nassau Candy Factory Optimization")
st.caption(
    "Factory Reallocation and Shipping Optimization "
    "Recommendation System"
)

st.info(
    "Recommendations are preliminary geographic estimates. "
    "Actual shipping costs and factory capacity were unavailable."
)

# Sidebar filters
st.sidebar.header("Dashboard Filters")

if "Region" in df.columns:
    regions = sorted(df["Region"].dropna().astype(str).unique())
    selected_regions = st.sidebar.multiselect(
        "Select Region",
        regions,
        default=regions
    )
else:
    selected_regions = []

if "Ship Mode" in df.columns:
    ship_modes = sorted(df["Ship Mode"].dropna().astype(str).unique())
    selected_modes = st.sidebar.multiselect(
        "Select Ship Mode",
        ship_modes,
        default=ship_modes
    )
else:
    selected_modes = []

# Apply filters
filtered_df = df.copy()

if selected_regions and "Region" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Region"].astype(str).isin(selected_regions)
    ]

if selected_modes and "Ship Mode" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Ship Mode"].astype(str).isin(selected_modes)
    ]

# KPI section
st.header("📊 Project Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Filtered Records", f"{len(filtered_df):,}")

with col2:
    st.metric(
        "Products",
        filtered_df["Product Name"].nunique()
        if "Product Name" in filtered_df.columns else 0
    )

with col3:
    st.metric("Products to Evaluate", 13)

with col4:
    st.metric("Products to Retain", 2)

# Region analysis
st.header("🌍 Regional Analysis")

if "Region" in filtered_df.columns:
    region_counts = (
        filtered_df.groupby("Region")
        .size()
        .reset_index(name="Orders")
    )

    st.bar_chart(
        region_counts.set_index("Region")["Orders"]
    )

# Factory recommendations
st.header("🏭 Factory Reallocation Recommendations")

if "Product" in recommendations.columns:
    product_options = sorted(
        recommendations["Product"].dropna().unique()
    )

    selected_product = st.selectbox(
        "Select a Product",
        product_options
    )

    product_result = recommendations[
        recommendations["Product"] == selected_product
    ]

    st.dataframe(product_result, use_container_width=True)

# Top five recommendations
st.subheader("⭐ Top 5 Products by Potential Distance Savings")

if "Potential Savings (unit-km)" in recommendations.columns:
    top_five = recommendations.sort_values(
        "Potential Savings (unit-km)",
        ascending=False
    ).head(5)

    st.bar_chart(
        top_five.set_index("Product")[
            "Potential Savings (unit-km)"
        ]
    )

# Model performance
st.header("🤖 Lead-Time Model Performance")

st.dataframe(models, use_container_width=True)

st.warning(
    "The best tested model, Gradient Boosting, achieved an R² of 0.019. "
    "Its predictive performance is weak, so predictions should be "
    "treated as exploratory rather than reliable forecasts."
)

# Risk analysis
st.header("⚠️ Risk Analysis")

st.dataframe(risk.head(20), use_container_width=True)

# Scenario analysis
st.header("🔎 Scenario Analysis")

st.caption(
    "The following scenarios are preliminary. "
    "Validate predictions and operational feasibility before implementation."
)

st.dataframe(scenarios.head(20), use_container_width=True)

# Limitations
with st.expander("📌 Business Limitations"):
    st.write("""
    - Actual shipping-cost data is unavailable.
    - Factory operating costs and production capacity are unavailable.
    - Source lead-time values require business verification.
    - Geographic distances are straight-line estimates.
    - Factory recommendations require operational validation.
    - Predicted lead-time improvements are not guaranteed.
    """)

st.success("Dashboard application loaded successfully!")
