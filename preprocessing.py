import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess(df, option):

    """
    This function is to cover all the preprocessing steps on the sales dataframe. It involves selecting important features, encoding categorical data, handling missing values,feature scaling and splitting the data
    """

    #Defining the map function
    def binary_map(feature):
        return feature.map({'Yes':1, 'No':0})

    # Encode binary categorical features
    binary_list =['Technology\nPrimary', 'Country', 'B2B Sales Medium','Client Employee Sizing','Business from Client Last Year','Opportunity Sizing','Client Revenue Sizing']
    df[binary_list] = df[binary_list].apply(binary_map)

    #Drop values based on operational options
    if (option == "Online"):
        columns = ['',]