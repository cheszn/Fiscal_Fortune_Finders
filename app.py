#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

#load the model from disk
import joblib
model = joblib.load(r"./best_model_xgb.sav")

#Import python scripts
from preprocessing import preprocess

def main():
    #Setting Application title
    st.title('Sales Prediction App')

    #Setting Application description
    st.markdown("""
     :dart:  This Streamlit app aims to predict if a case(client) will be won or lost .
    The application is functional for both manual prediction and uploading data prediction. \n
    """)
    st.markdown("<h3></h3>", unsafe_allow_html=True)

    #Setting Application sidebar default
    image = Image.open('sales.jpg')
    add_selectbox = st.sidebar.selectbox(
	"How would you like to predict?", ("Online", "Batch"))
    st.sidebar.info('This app is created to predict Sales deal closure')
    st.sidebar.image(image)


    if add_selectbox == "Online":
        st.info("Input data below")
        #Based on our optimal features selection
        st.subheader("Client data")
        Company_size = st.selectbox('Company Size:', ('1k or less', '1k to 5k','5K to 15k', '15k to 25k', 'More than 25k'))
        Revenue_size = st.selectbox('Company revenue:', ('100k or less', '100k to 250k', '250k to 500k','500k to 1m','More than 1M'))
        sales_medium = st.selectbox('B2B Sales Medium:', ('Partners','Enterprise Sellers','Marketing','Online Leads','Tele Sales'))
        Tech = st.selectbox('Primary Technology:', ('ERP Implementation', 'Technical Business Solutions', 'Analytics', 'Legacy Modernaization'))


        st.subheader("Business Informtion")
        Opportunity_sizing = st.selectbox('Deal_Valuation:', ('10k or less','10k to 20k','20k to 30k','30k to 40k','40k to 50k','50k to 60k','More than 60k'))
        Previous_Business = st.selectbox('Previous Business:',('0 (No business)','0 - 25,000', '25,000 - 50,000', '50,000 to 100,000', 'More than 100,000'))
        Opportunity_Usd = st.number_input('The exact $ value', min_value=0, max_value=10000000, value=0)


        st.subheader("Sales Information")
        Sales_Velocity = st.number_input('Sales Velocity', min_value=0, max_value=200, value=0)
        Sales_stage = st.number_input('Sales Stage Iteration',min_value=0, max_value=30, value=0)

        st.subheader("Country")
        Country = st.selectbox('Country:', ('France','Germany', 'United Kingdom', 'Italy', 'Spain', 'Sweden','Netherlands'))



        data = {
                'Client Employee Sizing':Company_size,
                'Client Revenue Sizing': Revenue_size,
                'B2B Sales Medium': sales_medium,
                'Technology\nPrimary': Tech,
                'Opportunity Sizing': Opportunity_sizing,
                'Opportunity Size (USD)': Opportunity_Usd,
                'Business from Client Last Year': Previous_Business,
                'Sales Velocity': Sales_Velocity,
                'Sales Stage Iterations': Sales_stage,
                'Country': Country
                }
        features_df = pd.DataFrame.from_dict([data])
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        st.write('Overview of input is shown below')
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        st.dataframe(features_df)


        #Preprocess inputs
        preprocess_df = preprocess(features_df, 'Online')

        prediction = model.predict(preprocess_df)

        if st.button('Predict'):
            if prediction == 1:
                st.warning('Yes, the deal will be won.')
            else:
                st.success('No, the deal will be lost.')
        

    else:
        st.subheader("Dataset upload")
        uploaded_file = st.file_uploader("Upload a file")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            #Get overview of data
            st.write(data.head())
            st.markdown("<h3></h3>", unsafe_allow_html=True)
            #Preprocess inputs
            preprocess_df = preprocess(data, "Batch")
            if st.button('Predict'):
                #Get batch prediction
                prediction = model.predict(preprocess_df)
                prediction_df = pd.DataFrame(prediction, columns=["Predictions"])
                prediction_df = prediction_df.replace({1:'Yes, the deal will be won.', 
                                                    0:'No, the deal will be lost.'})

                st.markdown("<h3></h3>", unsafe_allow_html=True)
                st.subheader('Prediction')
                st.write(prediction_df)
            
if __name__ == '__main__':
        main()







