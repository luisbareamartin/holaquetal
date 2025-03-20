
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Luis Barea - Airbnb Analysis")

@st.cache_data
def load_data():
    file_path = "airbnb.csv"
    df = pd.read_csv(file_path)
    df = df.rename(columns={"room_type": "listing_type", "neighbourhood": "neighborhood"})
    df.dropna(subset=["price"], inplace=True)  # Remove rows without price
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
listing_types = st.sidebar.multiselect("Select listing types", df["listing_type"].unique(), default=df["listing_type"].unique())
neighborhoods = st.sidebar.multiselect("Select neighborhoods", df["neighborhood"].unique(), default=df["neighborhood"].unique())
filtered_df = df[(df["listing_type"].isin(listing_types)) & (df["neighborhood"].isin(neighborhoods))]

# Tabs
tab1, tab2 = st.tabs(["Analysis", "Simulator"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        # Reemplazo BoxPlot por un Violin Plot más visual
        fig1 = px.violin(filtered_df, x="listing_type", y="minimum_nights", box=True, points="all", title="Minimum Nights by Listing Type (Violin Plot)")
        st.plotly_chart(fig1)

    with col2:
        # Cambio de BoxPlot a Histogram con precio
        fig2 = px.histogram(filtered_df, x="price", color="listing_type", nbins=50, barmode='overlay', title="Price Distribution by Listing Type")
        st.plotly_chart(fig2)

    # Cambio de bar chart a treemap para reviews
    top_reviews = filtered_df.groupby(["neighborhood", "listing_type"]).agg({"reviews_per_month": "sum"}).reset_index()
    fig3 = px.treemap(top_reviews, path=["neighborhood", "listing_type"], values="reviews_per_month", title="Reviews per Month by Neighborhood and Type")
    st.plotly_chart(fig3)

    # Cambio el scatter por un Bubble Chart donde el tamaño representa el precio
    fig4 = px.scatter(filtered_df, x="number_of_reviews_ltm", y="price", size="price", color="listing_type",
                      title="Reviews vs Price (Bubble Chart)", hover_data=["neighborhood"])
    st.plotly_chart(fig4)

with tab2:
    st.header("Price Simulator")
    selected_neighborhood = st.selectbox("Select a neighborhood", df["neighborhood"].unique())
    selected_type = st.selectbox("Select listing type", df["listing_type"].unique())
    num_nights = st.slider("Number of nights", 1, 30, 2)

    similar_listings = df[(df["neighborhood"] == selected_neighborhood) & 
                          (df["listing_type"] == selected_type) & 
                          (df["minimum_nights"] >= num_nights)]
    price_range = (similar_listings["price"].quantile(0.25), similar_listings["price"].quantile(0.75))

    st.write(f"Recommended price range for your selection: **${price_range[0]:.2f} - ${price_range[1]:.2f}**")

# Sidebar Instructions
st.sidebar.markdown("## Instructions")
st.sidebar.info("Upload this code to Streamlit Cloud and submit the link on Moodle.")
