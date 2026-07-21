import streamlit as st
import pickle
import pandas as pd


# model=pickle.load(open("C:\Users\ACS\Downloads\swiggy delivery time project.pkl","rb"))
# df=pd.read_csv("C:\Users\ACS\Downloads\swiggy_demographic (1).csv")
# st.title("swiggy delivery time predicion")
#st.markdown("predict swiggy delivery time probability in real time")

import streamlit as st
import pandas as pd
import pickle
import os

# Page setup
col1, col2, col3 = st.columns([1,1,1])

# with col2:
#     st.image("Pic.jpeg", width=700)

# Header
st.markdown(
    "<h1 style='text-align: center; color: black;'>Swiggy Delivery Time Prediction</h1>",
    unsafe_allow_html=True
)

col1, col2, col3,col4,= st.columns([1,2,2,1])

st.markdown(
    "<h4 style='font-weight: bold; color: black;'>Enter Order Details</h4>",
    unsafe_allow_html=True
)

# Load dataset 
df=pd.read_csv('swiggy_demographic.csv')

# Load trained model
# with open(r"C:\swiggy\swiggy delivery time project.pkl", 'rb') as f:
#     trained_model = pickle.load(f)
#trained_model=pickle.load(open(r"C:\swiggy\swiggy delivery time project.pkl","rb"))


with open(r'swiggy delivery time project.pkl','rb') as f:
    trained_model=pickle.load(f)


# ----------- User Inputs -----------

col1, col2, col3 ,col4= st.columns(4)

# ------------------ 1. RIDER DETAILS ------------------
with col1:
    st.subheader("👨‍🦱 Rider Details")
    
    age = st.number_input("Rider Age", min_value=18, max_value=60, value=25)
    ratings = st.slider('Rider Ratings', min_value=1.0, max_value=5.0, value=4.5, step=0.1)
    vehicle_condition = st.selectbox('Vehicle Condition', [0, 1, 2, 3])
    type_of_vehicle = st.selectbox('Type of vehicle', df['type_of_vehicle'].unique())

# ------------------ 2. DEMOGRAPHIC / LOCATION ------------------
with col2:
    st.subheader("📍 Location Details")

    city_name = st.selectbox('City Name', df['city_name'].dropna().unique())
    city_type = st.selectbox('City Type', df['city_type'].dropna().unique())
    weather = st.selectbox('Weather', df['weather'].dropna().unique())
    traffic = st.selectbox('Traffic', df['traffic'].dropna().unique())
    distance = st.number_input("Distance (km)", min_value=0.5, max_value=50.0, value=5.0)

# ------------------ 3. ORDER DETAILS ------------------
with col3:
    st.subheader("📦 Order Details")

    type_of_order = st.selectbox("Type of Order", df['type_of_order'].unique())
    multiple_deliveries = st.selectbox("Multiple Deliveries", [0, 1, 2, 3])
    festival = st.selectbox("Festival", df['festival'].dropna().unique())
    order_day = st.slider("Order Day", min_value=1, max_value=31, value=15)
    order_month = st.slider("Order Month", min_value=1, max_value=12, value=3)
with col4: 
    st.subheader("📦 Order Details")
    
    order_day_of_week = st.selectbox("Day of Week", df['order_day_of_week'].unique())
    is_weekend_label = st.selectbox("Is it Weekend?", ["No", "Yes"])
    # Convert to numeric for model
    is_weekend = 1 if is_weekend_label == "Yes" else 0
    pickup_time_minutes = st.number_input("Pickup Time (minutes)", min_value=1, max_value=60, value=10)
    order_time_hour = st.number_input("Order Time Hour (0-23)", min_value=0, max_value=23, value=18)
    order_time_of_day = st.selectbox('Order Time of Day', df['order_time_of_day'].unique())


# ----------- CREATE INPUT DATAFRAME -----------
input_df = pd.DataFrame([[
    age, ratings, weather, traffic, vehicle_condition,
    type_of_order, type_of_vehicle, multiple_deliveries,
    festival, city_type, city_name,
    order_day, order_month, order_day_of_week,
    is_weekend, pickup_time_minutes,
    order_time_hour, order_time_of_day, distance
]], columns=[
    'age', 'ratings', 'weather', 'traffic', 'vehicle_condition',
    'type_of_order', 'type_of_vehicle', 'multiple_deliveries',
    'festival', 'city_type', 'city_name',
    'order_day', 'order_month', 'order_day_of_week',
    'is_weekend', 'pickup_time_minutes',
    'order_time_hour', 'order_time_of_day', 'distance'
])

# ----------- PREDICTION -----------

if st.button("PREDICT⏱️"):
    prediction = trained_model.predict(input_df)
    st.success(f"Estimated Delivery Time: {prediction[0]:.2f} minutes ⏱️")