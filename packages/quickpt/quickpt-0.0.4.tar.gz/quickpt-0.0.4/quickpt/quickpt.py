from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import pandas as pd
import numpy as np

def quickpt(df, graph=None, encoder=True):
    
    """
    quickpt
    ---------
    Creates a DataFrame showing the missing values, total unique values, data type, and variance of each feature.

    If the argument graph is passed, then a bar chart of the specified parameter is visualized.

    Parameters
    ----------
    graph : var, null, uniq 
        (default is None)
    
    encode : True, False
        (default is True)
    
    Description of Parameters
    -------
        - var = variance
        - null = percent of missing values in decimal form
        - uniq = sum of unique values
        - encode --> True = Uses LabelEncoder to encode categorical variables and receive summary statistics
        - encode --> False = Only shows DataFrame/Visualization of original numeric variables of input data

    Use
    ----
    - Used on preprocessed datasets that have only numerical features
    - If data has categorical features set encoder=True to LabelEncode categorical features
    """

    temp_df = df.copy()
    try:
        if encoder == True:                                       # label encode categorical variables if parameter = True
            le = LabelEncoder()                                   #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #             
            try:                                                  # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                for i in temp_df:                                 # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    if temp_df.dtypes[i] == 'O':                  # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                        temp_df[i] = le.fit_transform(temp_df[i]) #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            except:                                               # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                pass                                              #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
        percent_missing = df.isnull().sum() * 100 / len(temp_df)           # aggregate percentage of null values
        unique_values = temp_df.nunique()                                  # aggregate all unique values
        dtype = df.dtypes                                                  # grab datatypes of df
        original_feature_count = len(temp_df.columns)                      # grab original sum of features
        variance = dict(np.sqrt(temp_df.describe().iloc[2,:]))             # aggregate variance per feature
        missing_value_df = pd.DataFrame({'Features': temp_df.columns,      #  #  #  #  #  #  #
                                        'percent_missing': percent_missing,# Create DataFrame of Summary Statistics
                                        'unique_values': unique_values,
                                        'dtype': dtype,
                                        'Variance': list(variance.values())})
        missing_value_df = missing_value_df.sort_values('percent_missing',ascending=False).reset_index().drop('index',axis=1)
        message = None
    except ValueError as e:
        
        # calculates numerical features removed
        
        numeric_features = []
        original_feature_count = len(temp_df.columns)
        numerical_feature_count = 0
        
       
        for feature in temp_df:
                if temp_df.dtypes[feature] == 'int64' or temp_df.dtypes[feature] == 'int32' or temp_df.dtypes[feature] == 'float64':
                    numeric_features.append(feature)
                    numerical_feature_count += 1
        subtracted_values = original_feature_count - numerical_feature_count

        temp_df = temp_df[numeric_features]
        message = " Output shows only original numeric features, " + str(subtracted_values) + " features are not showing!"
        print(str(e) + str('; set encoder=True to temporarily encode categorical variables and show more summary statistics...') + message)
        
        # repeats 34-53 if categorical features exist and encode = False; Shows only original numerical features         
        
        percent_missing = temp_df.isnull().sum() * 100 / len(df)
        unique_values = temp_df.nunique()
        dtype = temp_df.dtypes
        variance = dict(np.sqrt(temp_df.describe().iloc[2,:]))
        missing_value_df = pd.DataFrame({'Features': temp_df.columns,
                                        'percent_missing': percent_missing,
                                        'unique_values': unique_values,
                                        'dtype': dtype,
                                        'Variance': list(variance.values())})
        missing_value_df = missing_value_df.sort_values('percent_missing',ascending=False).reset_index().drop('index',axis=1)
    # graph parameters for visualization    
    if graph == 'var':
        df = missing_value_df
        fig = px.bar(df.sort_values('Variance', ascending=False), x='Features', y='Variance')
        fig.update_xaxes(tickangle=40, tickfont_size=8)
        fig.show()
    if graph == 'null':
        df = missing_value_df
        fig = px.bar(df.sort_values('percent_missing', ascending=False), x='Features', y='percent_missing')
        fig.update_xaxes(tickangle=40, tickfont_size=8)
        fig.show()
    if graph == 'uniq':
        df = missing_value_df
        fig = px.bar(df.sort_values('unique_values', ascending=False), x='Features', y='unique_values')
        fig.update_xaxes(tickangle=40, tickfont_size=8)
        fig.show()

    return missing_value_df
    