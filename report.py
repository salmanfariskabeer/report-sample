import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# Load Data
# -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("supermarket_monthly_sales.csv")
    return df

df = load_data()

st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")

st.title("📊 Supermarket Sales & Profit Dashboard")

# -------------------
# Sidebar Filters
# -------------------
st.sidebar.header("Filters")

months = st.sidebar.multiselect(
    "Select Month(s):",
    options=sorted(df["Month"].unique()),
    default=sorted(df["Month"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category:",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

customer_types = st.sidebar.multiselect(
    "Select Customer Type:",
    options=df["CustomerType"].unique(),
    default=df["CustomerType"].unique()
)

payment_methods = st.sidebar.multiselect(
    "Select Payment Method:",
    options=df["PaymentMethod"].unique(),
    default=df["PaymentMethod"].unique()
)

# Apply filters
df_filtered = df[
    (df["Month"].isin(months)) &
    (df["Category"].isin(categories)) &
    (df["CustomerType"].isin(customer_types)) &
    (df["PaymentMethod"].isin(payment_methods))
]

# -------------------
# Check Empty Data
# -------------------
if df_filtered.empty:
    st.warning("⚠️ No data available for the selected filters. Try adjusting filters.")
    st.stop()

# -------------------
# KPIs
# -------------------
total_sales = df_filtered["SalesAmount"].sum()
total_profit = df_filtered["Profit"].sum()
avg_ticket = df_filtered["SalesAmount"].mean()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"AED {total_sales:,.2f}")
col2.metric("📈 Total Profit", f"AED {total_profit:,.2f}")
col3.metric("🛒 Avg Sales/Transaction", f"AED {avg_ticket:,.2f}")
col4.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# -------------------
# Charts
# -------------------

# Monthly Sales & Profit
monthly_summary = df_filtered.groupby("Month")[["SalesAmount", "Profit"]].sum().reset_index()
fig1 = px.bar(monthly_summary, x="Month", y=["SalesAmount", "Profit"], barmode="group",
              title="Monthly Sales & Profit")
st.plotly_chart(fig1, use_container_width=True)

# Top Categories by Sales
category_sales = df_filtered.groupby("Category")[["SalesAmount", "Profit"]].sum().reset_index()
top_categories = category_sales.sort_values(by="SalesAmount", ascending=False).head(10)
fig2 = px.bar(top_categories, x="Category", y="SalesAmount", color="Profit",
              title="Top 10 Categories by Sales", text="SalesAmount")
st.plotly_chart(fig2, use_container_width=True)

# Profit Contribution by Category
fig3 = px.pie(category_sales, values="Profit", names="Category", title="Profit Contribution by Category")
st.plotly_chart(fig3, use_container_width=True)

# Category Profit Margin
category_sales["ProfitMargin(%)"] = (category_sales["Profit"] / category_sales["SalesAmount"]) * 100
fig4 = px.bar(category_sales.sort_values(by="ProfitMargin(%)", ascending=False).head(15),
              x="Category", y="ProfitMargin(%)", title="Top Categories by Profit Margin")
st.plotly_chart(fig4, use_container_width=True)

# Day of Week Trends
dow_summary = df_filtered.groupby("DayOfWeek")[["SalesAmount", "Profit"]].sum().reset_index()
fig5 = px.line(dow_summary, x="DayOfWeek", y="SalesAmount", markers=True, title="Sales by Day of Week")
st.plotly_chart(fig5, use_container_width=True)

# -------------------
# Raw Data
# -------------------
with st.expander("View Raw Data"):
    st.dataframe(df_filtered)
