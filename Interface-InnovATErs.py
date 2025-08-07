import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load trained model
model = joblib.load("Farm_Irrigation_System (1).pkl")

# Page settings
st.set_page_config(page_title="AgroStream - Smart Irrigation System", page_icon="💧", layout="centered")

# Custom CSS for dark mode UI
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
        .dataframe th, .dataframe td {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Project Header
st.title("🌿 AgroStream")
st.subheader("Smart Irrigation Automation using AI")
st.markdown("A machine learning-powered decision system to optimize sprinkler operations across farms.")
st.subheader("Sensor Input Panel")

# Input sliders
sensor_values = []
cols = st.columns(4)

for i in range(20):
    with cols[i % 4]:
        val = st.slider(f"Sensor {i}", 0.0, 1.0, 0.5, 0.01, key=f"sensor_{i}")
        sensor_values.append(val)

# Display input summary
st.markdown("### Sensor Values Preview")
sensor_df = pd.DataFrame({
    'Sensor': [f"Sensor {i}" for i in range(20)],
    'Value': sensor_values
})
st.dataframe(sensor_df, use_container_width=True)

# Predict button
if st.button("Predict Sprinkler Status"):
    input_array = np.array(sensor_values).reshape(1, -1)
    prediction = model.predict(input_array)[0]

    st.markdown("---")
    st.subheader("Sprinkler Prediction Results")

    results = []
    result_cols = st.columns(4)

    for i, status in enumerate(prediction):
        result = "ON" if status == 1 else "OFF"
        with result_cols[i % 4]:
            if status == 1:
                st.success(f"Sprinkler {i} (parcel_{i}): ON")
            else:
                st.error(f"Sprinkler {i} (parcel_{i}): OFF")
        results.append({
            "Sprinkler": f"Sprinkler {i}",
            "Parcel": f"parcel_{i}",
            "Status": result
        })

    # Summary table
    st.markdown("### Summary Table")
    result_df = pd.DataFrame(results)
    st.dataframe(result_df, use_container_width=True)

    # Download option
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name='AgroStream_Sprinkler_Results.csv',
        mime='text/csv'
    )
