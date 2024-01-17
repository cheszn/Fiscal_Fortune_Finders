#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

#import the saved
import joblib
model = joblib.load(r"./best_model_xgb.sav")


def Online_input():
    
    #Based on our optimal features selection
    st.sidebar.subheader("Client data")
    
    
    Tech = st.sidebar.selectbox('Primary Technology:', ('ERP Implementation', 'Technical Business Solutions', 'Analytics', 'Legacy Modernaization'))
    Country = st.sidebar.selectbox('Country:', ('France','Germany', 'United Kingdom', 'Italy', 'Spain', 'Sweden','Netherlands'))
    sales_medium = st.sidebar.selectbox('B2B Sales Medium:', ('Partners','Enterprise Sellers','Marketing','Online Leads','Tele Sales'))
    Sales_Velocity = st.sidebar.number_input('Sales Velocity', min_value=0, max_value=200, value=0)
    Sales_stage = st.sidebar.number_input('Sales Stage Iteration',min_value=0, max_value=30, value=0)
    Opportunity_Usd = st.sidebar.number_input('The exact $ value', min_value=0, max_value=10000000, value=0)
    Revenue_size = st.sidebar.selectbox('Company revenue:', ('100k or less', '100k to 250k', '250k to 500k','500k to 1m','More than 1M'))
    Company_size = st.sidebar.selectbox('Company Size:', ('1k or less', '1k to 5k','5K to 15k', '15k to 25k', 'More than 25k'))
    Previous_Business = st.sidebar.selectbox('Previous Business:',('0 (No business)','0 - 25,000', '25,000 - 50,000', '50,000 to 100,000', 'More than 100,000'))
    Opportunity_sizing = st.sidebar.selectbox('Deal_Valuation:', ('10k or less','10k to 20k','20k to 30k','30k to 40k','40k to 50k','50k to 60k','More than 60k'))

    

        
    user_data = pd.DataFrame({
                'Technology': [Tech],
                'Country': [Country],
                'B2B Sales Medium': [sales_medium],
                'Sales Velocity': Sales_Velocity,
                'Sales Stage Iterations': [Sales_stage],
                'Opportunity Size (USD)': [Opportunity_Usd],
                'Client Revenue Sizing': [Revenue_size],
                'Client Employee Sizing':[Company_size],
                'Business from Client Last Year': [Previous_Business],
                'Opportunity Sizing': [Opportunity_sizing]
                
                })
        

        # Process user input and predict
    if st.sidebar.button('Predict'):
        # Directly pass the user input data to the model for prediction
        prediction = model.predict(pd.DataFrame(user_data))[0]
        feedback = "Won" if prediction == 1 else "Loss"
        st.write(f"Prediction: {feedback}")


# Initialize batch_data at the beginning of your script (global scope)
batch_data = None


def batch_prediction_interface():
    global batch_data  # Declare batch_data as global to modify the global instance
    st.sidebar.header("Batch Prediction")
    uploaded_file = st.file_uploader(
        "Upload CSV for Batch Prediction", type=["csv"])

    if uploaded_file is not None:
        try:
            batch_data = pd.read_csv(uploaded_file)
            predictions = model.predict(batch_data)
            batch_data['predictions'] = predictions
            st.write(batch_data)
        except Exception as e:
            st.error(f"An error occurred: {e}")

#Setting Application title
st.title('Sales Prediction App')

#Setting Application description
st.markdown("""
     :dart:  This Streamlit app aims to predict if a case(client) will be won or lost .
    The application is functional for both manual prediction and uploading data prediction. \n
    """)
st.markdown("<h3></h3>", unsafe_allow_html=True)

    #Setting Application sidebar default
image = Image.open('sales.jpeg')


prediction_method = st.sidebar.selectbox("Select Prediction Method", [
                                         "Online Prediction", "Batch Prediction"])

if prediction_method == "Online Prediction":
    Online_input()
elif prediction_method == "Batch Prediction":
    batch_prediction_interface()
