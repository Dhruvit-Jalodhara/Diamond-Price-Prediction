import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="Diamond Price Predictor",
    page_icon="💎",
    layout="wide"
)

model = pickle.load(open("Models/model.pkl", "rb"))
standard_scaler = pickle.load(open("Models/scaler.pkl", "rb"))

with st.sidebar:

    st.title("💎 Diamond Predictor")

    st.markdown("---")

    st.info("""
    ### Project Information

    This machine learning application predicts
    diamond prices based on:

    • Carat Weight
    • Cut Quality
    • Color Grade
    • Clarity Grade
    • Diamond Dimensions

    Built using:

    • Streamlit
    • Scikit-Learn
    • Pandas
    • NumPy
    """)

    st.markdown("---")

    st.success("🚀 Machine Learning Project")

st.markdown("""
<div style="
background: linear-gradient(90deg,#2563eb,#7c3aed);
padding:25px;
border-radius:15px;
text-align:center;
color:white;
margin-bottom:20px;">
<h1>💎 Diamond Price Prediction</h1>
<p>Predict the market value of diamonds using Machine Learning</p>
</div>
""", unsafe_allow_html=True)

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

    carat = st.number_input("Carat", min_value=0.1, max_value=5.5, value=1.0)

    cut = st.selectbox(
        "Cut",
        ["Fair", "Good", "Very Good", "Premium", "Ideal"]
    )

    color = st.selectbox(
        "Color",
        ["D", "E", "F", "G", "H", "I", "J"]
    )

    clarity = st.selectbox(
        "Clarity",
        ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]
    )

with col2:

    depth = st.number_input("Depth", min_value=40.0, max_value=80.0, value=61.5)

    table = st.number_input("Table", min_value=40.0, max_value=100.0, value=57.0)

    x = st.number_input("Length (x)", min_value=0.0, max_value=15.0, value=5.7)

    y = st.number_input("Width (y)", min_value=0.0, max_value=15.0, value=5.7)

    z = st.number_input("Depth (z)", min_value=0.0, max_value=15.0, value=3.5)

cut_mapping = {
    'Fair': 0,
    'Good': 1,
    'Very Good': 2,
    'Premium': 3,
    'Ideal': 4
}

color_mapping = {
    'J': 0,
    'I': 1,
    'H': 2,
    'G': 3,
    'F': 4,
    'E': 5,
    'D': 6
}

clarity_mapping = {
    'I1': 0,
    'SI2': 1,
    'SI1': 2,
    'VS2': 3,
    'VS1': 4,
    'VVS2': 5,
    'VVS1': 6,
    'IF': 7
}

encoded_cut = cut_mapping[cut]
encoded_color = color_mapping[color]
encoded_clarity = clarity_mapping[clarity]

if st.button("💰 Predict Diamond Price", use_container_width=True):

    input_df = pd.DataFrame({
        "carat": [carat],
        "cut": [encoded_cut],
        "color": [encoded_color],
        "clarity": [encoded_clarity],
        "depth": [depth],
        "table": [table],
        "x": [x],
        "y": [y],
        "z": [z]
    })

    transformed_data = standard_scaler.transform(input_df)

    prediction = model.predict(transformed_data)[0]

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg,#2563eb,#7c3aed);
            padding:25px;
            border-radius:15px;
            text-align:center;
            color:white;
            margin-top:10px;
            margin-bottom:20px;
        ">
            <h2>💎 Estimated Diamond Price</h2>
            <h1>${prediction:,.2f}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    quality_score = (
        carat * 20 +
        encoded_cut * 10 +
        encoded_color * 5 +
        encoded_clarity * 5
    )

    quality_score = min(100, quality_score)

    st.subheader("✨ Diamond Quality Score")

    st.progress(int(quality_score))

    st.write(f"**Score:** {quality_score:.0f}/100")

    if prediction < 2000:
        category = "💍 Budget Diamond"
    elif prediction < 10000:
        category = "💎 Premium Diamond"
    else:
        category = "👑 Luxury Diamond"

    st.info(f"Category: {category}")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Carat", carat)
    metric2.metric("Cut", cut)
    metric3.metric("Color", color)

    summary_df = pd.DataFrame({
        "Carat": [carat],
        "Cut": [cut],
        "Color": [color],
        "Clarity": [clarity],
        "Depth": [depth],
        "Table": [table],
        "X": [x],
        "Y": [y],
        "Z": [z]
    })

    st.subheader("📋 Input Summary")

    st.dataframe(summary_df, use_container_width=True)

    with st.expander("🔍 View Encoded Features"):
        st.dataframe(input_df, use_container_width=True)
