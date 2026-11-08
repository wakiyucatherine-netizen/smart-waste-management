
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load saved files
df = pd.read_csv("waste_bin_data.csv")
model = joblib.load("waste_prediction_model.pkl")

# Dashboard title
st.title("Smart Waste Management System")
st.write("AI-Based IoT Waste Bin Monitoring Dashboard")

# Calculate statistics
total = len(df)
normal = (df["Bin_Status"] == "Normal").sum()
warning = (df["Bin_Status"] == "Warning").sum()
collection = (df["Bin_Status"] == "Collection Required").sum()

# Display summary
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Readings", total)
col2.metric("Normal", normal)
col3.metric("Warning", warning)
col4.metric("Collection Required", collection)

# Display dataset
st.subheader("Waste Bin Monitoring")
st.dataframe(df)

# Display fill-level graph
st.subheader("Waste Bin Fill Levels")

fig, ax = plt.subplots()
ax.bar(df["Bin_ID"], df["Fill_Level"])
ax.set_xlabel("Bin ID")
ax.set_ylabel("Fill Level (%)")
ax.set_title("Waste Bin Fill Levels")

st.pyplot(fig)

# Predict future fill level
st.subheader("AI Waste Level Prediction")

current_level = st.slider(
    "Select current bin fill level (%)",
    0, 100, 50
)

prediction = model.predict(
    pd.DataFrame({"Fill_Level": [current_level]})
)[0]

prediction = max(0, min(100, prediction))

st.metric("Predicted Future Fill Level", f"{prediction:.2f}%")

if prediction > 80:
    st.error("Collection Required")
elif prediction > 70:
    st.warning("Prepare for Waste Collection")
else:
    st.success("Bin is Normal")

