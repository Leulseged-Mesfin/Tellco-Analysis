import pandas as pd
import numpy as np

def percentage_missing_values(df):
    total_number_cells = df.shape[0]
    countMissing = df.isnull().sum()
    # totalMissing = countMissing.sum()
    return f"The telecom contains {round(((countMissing/total_number_cells) * 100), 2)}% missing values."




# def drop_high_missing_value_columns(df):
#     """
#     Drops columns from the DataFrame that have more than 30% missing values.

#     Parameters:
#     df (pd.DataFrame): The DataFrame from which columns will be dropped.

#     Returns:
#     pd.DataFrame: The DataFrame with columns dropped.
#     """
#     # Calculate the threshold for missing values (30%)
#     threshold = 0.30
    
#     # Calculate the percentage of missing values for each column
#     missing_percentage = df.isnull().mean()
    
#     # Determine columns to drop
#     columns_to_drop = missing_percentage[missing_percentage > threshold].index
    
#     # Drop the columns with missing values above the threshold
#     df_dropped = df.drop(columns=columns_to_drop)
    
#     return df_dropped
