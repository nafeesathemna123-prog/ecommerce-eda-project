
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


# Summary Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(filtered_df):,}")

col2.metric(
    "Unique Customers",
    f"{filtered_df['Customer_ID'].nunique():,}"
)

col3.metric(
    "Unique Orders",
    f"{filtered_df['Order_ID'].nunique():,}"
)

col4.metric(
    "Total Sales",
    f"{filtered_df['Total_Amount'].sum():,.2f}"
)

st.divider()

# Sales Trend Over Time
st.subheader("📈 Sales Trend Over Time")

if "Date" in filtered_df.columns and "Total_Amount" in filtered_df.columns:
    sales_data = filtered_df.dropna(subset=["Date"]).copy()
    sales_data["Date"] = pd.to_datetime(
        sales_data["Date"], errors="coerce"
    )
    sales_data = sales_data.dropna(subset=["Date"])

    if not sales_data.empty:
        daily_sales = (
            sales_data.groupby(sales_data["Date"].dt.date)["Total_Amount"]
            .sum()
            .reset_index()
        )
        daily_sales.columns = ["Date", "Total Sales"]

        fig = px.line(
            daily_sales,
            x="Date",
            y="Total Sales",
            markers=True,
            title="Daily Sales"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No valid dates available for the sales trend.")


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



# Key Findings
st.subheader("💡 Key Findings")

col1, col2 = st.columns(2)

with col1:
    if not filtered_df.empty and "Product_Category" in filtered_df.columns:
        popular_category = filtered_df["Product_Category"].mode()

        if not popular_category.empty:
            st.info(f"🛍️ Most common product category: **{popular_category.iloc[0]}**")

    if not filtered_df.empty and "Payment_Method" in filtered_df.columns:
        popular_payment = filtered_df["Payment_Method"].mode()

        if not popular_payment.empty:
            st.info(f"💳 Most-used payment method: **{popular_payment.iloc[0]}**")

with col2:
    if not filtered_df.empty and "City" in filtered_df.columns:
        popular_city = filtered_df["City"].mode()

        if not popular_city.empty:
            st.info(f"📍 City with the most records: **{popular_city.iloc[0]}**")

    if not filtered_df.empty and "Total_Amount" in filtered_df.columns:
        average_order_value = filtered_df["Total_Amount"].mean()

        st.info(f"💰 Average amount per record: **{average_order_value:,.2f}**")

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
