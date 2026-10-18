
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce EDA Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 E-Commerce Consumer Trends Dashboard")
st.write(
    "Explore customer behaviour, product categories, "
    "sales patterns, and payment preferences."
)

@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_customer_behavior_dataset.csv")

df = load_data()

# Convert date column if available
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Sidebar filters
st.sidebar.header("Dashboard Filters")
filtered_df = df.copy()

if "Gender" in df.columns:
    genders = st.sidebar.multiselect(
        "Gender",
        sorted(df["Gender"].dropna().unique()),
        default=sorted(df["Gender"].dropna().unique())
    )
    filtered_df = filtered_df[filtered_df["Gender"].isin(genders)]

if "City" in df.columns:
    cities = st.sidebar.multiselect(
        "City",
        sorted(df["City"].dropna().unique()),
        default=sorted(df["City"].dropna().unique())
    )
    filtered_df = filtered_df[filtered_df["City"].isin(cities)]

if "Product_Category" in df.columns:
    categories = st.sidebar.multiselect(
        "Product Category",
        sorted(df["Product_Category"].dropna().unique()),
        default=sorted(df["Product_Category"].dropna().unique())
    )
    filtered_df = filtered_df[
        filtered_df["Product_Category"].isin(categories)
    ]

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", f"{len(filtered_df):,}")

if "Customer_ID" in filtered_df.columns:
    col2.metric(
        "Unique Customers",
        f"{filtered_df['Customer_ID'].nunique():,}"
    )
else:
    col2.metric("Columns", len(filtered_df.columns))

if "Order_ID" in filtered_df.columns:
    col3.metric(
        "Unique Orders",
        f"{filtered_df['Order_ID'].nunique():,}"
    )
else:
    col3.metric("Missing Values", int(filtered_df.isna().sum().sum()))

st.divider()

# Charts
left, right = st.columns(2)

with left:
    if "Product_Category" in filtered_df.columns:
        category_counts = (
            filtered_df["Product_Category"]
            .value_counts()
            .rename_axis("Product Category")
            .reset_index(name="Orders")
        )
        fig = px.bar(
            category_counts,
            x="Product Category",
            y="Orders",
            title="Records by Product Category",
            color="Product Category"
        )
        st.plotly_chart(fig, use_container_width=True)

with right:
    if "Payment_Method" in filtered_df.columns:
        payment_counts = (
            filtered_df["Payment_Method"]
            .value_counts()
            .rename_axis("Payment Method")
            .reset_index(name="Count")
        )
        fig = px.pie(
            payment_counts,
            names="Payment Method",
            values="Count",
            title="Payment Method Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    if "City" in filtered_df.columns:
        city_counts = (
            filtered_df["City"]
            .value_counts()
            .rename_axis("City")
            .reset_index(name="Count")
        )
        fig = px.bar(
            city_counts,
            x="City",
            y="Count",
            title="Customer Records by City"
        )
        st.plotly_chart(fig, use_container_width=True)

with right:
    if "Device_Type" in filtered_df.columns:
        device_counts = (
            filtered_df["Device_Type"]
            .value_counts()
            .rename_axis("Device")
            .reset_index(name="Count")
        )
        fig = px.pie(
            device_counts,
            names="Device",
            values="Count",
            title="Device Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

# Numeric summaries
st.subheader("Numerical Summary")
st.dataframe(
    filtered_df.describe(include="all").transpose(),
    use_container_width=True
)

# Dataset preview
st.subheader("Explore Dataset")
st.dataframe(filtered_df, use_container_width=True)

st.download_button(
    "Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_ecommerce_data.csv",
    mime="text/csv"
)
