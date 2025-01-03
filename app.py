import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("processed_dataset.csv")
    return data

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

# Filter Kategori
selected_category = st.sidebar.multiselect(
    "Select Categories", options=df["Category"].unique(), default=df["Category"].unique()
)

# Filter Grup Umur: Menambahkan 'All' di awal opsi
selected_age_group = st.sidebar.selectbox(
    "Select Age Group", options=["All"] + list(df["Age Group"].unique()), index=0
)

# Filtered dataset
if selected_age_group == "All":
    filtered_data = df[df["Category"].isin(selected_category)]  # Tidak memfilter berdasarkan Age Group
else:
    filtered_data = df[(df["Category"].isin(selected_category)) & (df["Age Group"] == selected_age_group)]  # Filter berdasarkan kategori dan age group

# Main Title
st.title("Interactive Dashboard: Consumer Shopping Trends")

# Tabs for better organization
tab1, tab2, tab3 = st.tabs(["Overview", "Analisis Musiman", "Performa Customer"])

# Tab 1: Overview
with tab1:
    st.header("1. Trend Pembelian")
    
    # Visualization 1: Pembelian berdasarkan kategori
    st.subheader("Pembelian berdasarkan kategori")
    bar_fig = px.bar(
        filtered_data,
        x="Category",
        y="Purchase Amount (USD)",
        color="Category",
        labels={"Category": "Product Category", "Purchase Amount (USD)": "Total Purchase ($)"}
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    # Visualization 2: Rating vs Purchase Amount
    st.subheader("Rating vs Jumlah Pembelian (Berdasarkan Age Group)")
    scatter_fig = px.scatter(
        filtered_data,
        x="Review Rating",
        y="Purchase Amount (USD)",
        animation_frame="Age Group",
        color="Category",
        size="Purchase Frequency (Yearly)",
        labels={"Review Rating": "Rating", "Purchase Amount (USD)": "Total Purchase ($)"}
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

    # Visualization 3: Purchase Frequency by Payment Method
    st.subheader("Frekuensi Pembelian bBerdasarkan Payment Method")
    pie_fig = px.pie(
        filtered_data,
        names="Preferred Payment Method",
        values="Purchase Frequency (Yearly)",
    )
    st.plotly_chart(pie_fig, use_container_width=True)

# Tab 2: Analisis Musiman
with tab2:
    st.header("2. Analisis Musiman")
    
    # Visualization: Total Purchase Amount by Season
    st.subheader("Total Jumlah Pembelian Berdasarkan Musim")
    season_data = filtered_data.groupby("Season")["Total Purchase Amount"].sum().reset_index()
    season_bar_fig = px.bar(
        season_data,
        x="Season",
        y="Total Purchase Amount",
        color="Season",
        labels={"Season": "Season", "Total Purchase Amount": "Total Purchase ($)"}
    )
    st.plotly_chart(season_bar_fig, use_container_width=True)

# Tab 3: Performa Customer
with tab3:
    st.header("3. Performa Customer")

    # Visualization: Frequency of Purchases
    st.subheader("Frekuensi Pembelian")

    # Group data by Frequency of Purchases and count occurrences
    frequency_data = df["Frequency of Purchases"].value_counts().reset_index()
    frequency_data.columns = ["Frequency of Purchases", "Count"]

    # Bar Chart for Frequency of Purchases
    frequency_bar_fig = px.bar(
        frequency_data,
        x="Frequency of Purchases",
        y="Count",
        color="Frequency of Purchases",
        labels={"Frequency of Purchases": "Frequency", "Count": "Number of Customers"},
        text="Count"
    )
    frequency_bar_fig.update_traces(textposition="outside")
    st.plotly_chart(frequency_bar_fig, use_container_width=True)

    # New Visualization: Purchase Amount by Age Group
    st.subheader("Jumlah Pembelian Berdasarkan Age Group")

    # Group data by Age Group and calculate the total purchase amount for each group
    age_group_data = filtered_data.groupby("Age Group")["Total Purchase Amount"].sum().reset_index()

    # Bar chart for purchase amount by Age Group
    age_group_bar_fig = px.bar(
        age_group_data,
        x="Age Group",
        y="Total Purchase Amount",
        color="Age Group",
        labels={"Age Group": "Age Group", "Total Purchase Amount": "Total Purchase ($)"},
        text="Total Purchase Amount"
    )
    age_group_bar_fig.update_traces(textposition="outside")
    st.plotly_chart(age_group_bar_fig, use_container_width=True)

# Sidebar Insights
st.sidebar.write("### Insights and Highlights")
st.sidebar.markdown("""
- **Pembelian Utama**: Pakaian mendominasi pembelian.
- **Tren Musiman**: Musim dingin adalah musim yang paling aktif dalam hal jumlah total pembelian.
- **Performa Customer**: Customer rentang umur 18-35 mendominasi pembelian.
""")
