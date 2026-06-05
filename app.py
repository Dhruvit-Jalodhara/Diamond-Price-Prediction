import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load Model and Scaler
model = pickle.load(open('Models/model.pkl', 'rb'))
standard_scaler = pickle.load(open('Models/scaler.pkl', 'rb'))

# Page Config
st.set_page_config(
    page_title="Diamond Price Predictor",
    page_icon="💎",
    layout="centered"
)

# Title & Description
st.title("💎 Diamond Price Predictor")

st.markdown("""
### About This Application

This machine learning application predicts the market price of a diamond using its physical and quality characteristics.

#### Features Used for Prediction:
- 💎 Carat Weight
- ✨ Cut Quality
- 🎨 Color Grade
- 🔍 Clarity Grade
- 📏 Depth Percentage
- 📐 Table Percentage
- 📊 Dimensions (x, y, z)

Fill in the diamond details and click **Predict Price** to receive an estimated valuation.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    carat = st.number_input( "Carat", min_value=0.1, max_value=5.5, value=1.0 )

    cut = st.selectbox( "Cut", ["Fair", "Good", "Very Good", "Premium", "Ideal"] )

    color = st.selectbox( "Color", ["D", "E", "F", "G", "H", "I", "J"] )

    clarity = st.selectbox( "Clarity", ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"] )

with col2:
    depth = st.number_input( "Depth", min_value=40.0, max_value=80.0, value=61.5 )

    table = st.number_input( "Table", min_value=40.0, max_value=100.0, value=57.0 )

    x = st.number_input( "Length (x)", min_value=0.0, max_value=15.0, value=5.7 )

    y = st.number_input( "Width (y)", min_value=0.0, max_value=15.0, value=5.7 )

    z = st.number_input( "Depth (z)", min_value=0.0, max_value=15.0, value=3.5 )

## Encoding 

cut_mapping = { 'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4 }
encodec_cut = cut_mapping[cut]

color_mapping = { 'J' : 0 , 'I' : 1 , 'H' : 2 , 'G' : 3 , 'F' : 4 , 'E' : 5 , 'D' : 6 }
encodec_color = color_mapping[color]

clarity_mapping = { 'I1' : 0 ,'SI2' : 1 , 'SI1' : 2 , 'VS2' : 3 , 'VS1' : 4 , 'VVS2' : 5 , 'VVS1' : 6, 'IF' : 7 }
encodec_clarity = clarity_mapping[clarity]


if st.button("Predict Price 💰", use_container_width=True):

    input_df = pd.DataFrame({
        "carat": [carat],
        "cut": [encodec_cut],
        "color": [encodec_color],
        "clarity": [encodec_clarity],
        "depth": [depth],
        "table": [table],
        "x": [x],
        "y": [y],
        "z": [z]
    })

    transformed_data = standard_scaler.transform(input_df)

    prediction = model.predict(transformed_data)[0]

    st.success(f"Estimated Diamond Price: ${prediction:,.2f}")

    st.subheader("Input Summary")

    st.dataframe(input_df,hide_index=True)