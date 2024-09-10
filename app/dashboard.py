import pandas as pd
import streamlit as st
import plotly.express as px
import os
import sys
import requests
from io import StringIO

# Adjust system path to include the parent directory
parent_path = os.path.abspath('..')
if parent_path not in sys.path: 
    sys.path.insert(0, parent_path)

# Function to fetch data from a GitHub repository
def fetch_data_from_github():
    url = 'https://raw.githubusercontent.com/Leulseged-Mesfin/Tellco-Analysis/task-3/Data/data.csv'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Convert content to a DataFrame
        return pd.read_csv(StringIO(response.text))
    else:
        st.error(f"Error fetching data from GitHub. Status code: {response.status_code}")
        return pd.DataFrame()

# Load data into DataFrame
df = fetch_data_from_github()

# Function to drop rows with missing values in key columns
def remove_nan_rows(df):
    important_columns = ['Bearer Id', 'Start', 'End', 'IMSI', 'MSISDN/Number']
    df.dropna(subset=important_columns, inplace=True)

# Function to handle missing values with mean/mode
def impute_missing_data(df):
    columns_to_fill = [
        'DL TP < 50 Kbps (%)', '50 Kbps < DL TP < 250 Kbps (%)',
        '250 Kbps < DL TP < 1 Mbps (%)', 'DL TP > 1 Mbps (%)',
        'UL TP < 10 Kbps (%)', '10 Kbps < UL TP < 50 Kbps (%)',
        '50 Kbps < UL TP < 300 Kbps (%)', 'UL TP > 300 Kbps (%)',
        'Last Location Name', 'Avg RTT DL (ms)', 'Avg RTT UL (ms)',
        'Nb of sec with Vol DL < 6250B', 'Nb of sec with Vol UL < 1250B'
    ]
    
    for col in columns_to_fill:
        if col != 'Last Location Name':
            df[col].fillna(df[col].mean(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0], inplace=True)

# Handling missing values for specific task
def impute_task_specific_values(df):
    task_specific_columns = {
        'MSISDN/Number': 'mean',
        'Avg RTT DL (ms)': 'mean',
        'Avg RTT UL (ms)': 'mean',
        'Avg Bearer TP DL (kbps)': 'mean',
        'Avg Bearer TP UL (kbps)': 'mean',
        'TCP DL Retrans. Vol (Bytes)': 'mean',
        'TCP UL Retrans. Vol (Bytes)': 'mean',
        'Total_Avg_RTT': 'mean'
    }
    
    for col, method in task_specific_columns.items():
        if col in df.columns:
            df[col].fillna(df[col].mean(), inplace=True)

    if 'Handset Type' in df.columns:
        df['Handset Type'].fillna(df['Handset Type'].mode()[0], inplace=True)

# Streamlit app layout
st.title("Dashboard for Telecom Data Analytics")

# Sidebar for navigation
st.sidebar.title("Choose Analysis")
options = ["Dataset Exploration", "User Overview", "User Engagement", "User Experience"]
selected_option = st.sidebar.selectbox("Select Analysis", options)

# Dataset Exploration
if selected_option == "Dataset Exploration":
    st.subheader("Explore Dataset")

    # Dropdown for data exploration
    exploration = st.selectbox("Choose a view:", ["Head", "Tail", "Summary Stats", "Missing Data Info"])
    
    if exploration == "Head":
        st.dataframe(df.head())
    elif exploration == "Tail":
        st.dataframe(df.tail())
    elif exploration == "Summary Stats":
        st.dataframe(df.describe())
    elif exploration == "Missing Data Info":
        st.dataframe(df.isnull().sum())

        # Choose how to handle missing values
        missing_option = st.selectbox("Handle missing data:", ["None", "Drop Rows", "Fill Mean/Mode", "Task-specific Fill"])
        
        if missing_option == "Drop Rows":
            remove_nan_rows(df)
            st.success("Dropped rows with missing values.")
        elif missing_option == "Fill Mean/Mode":
            impute_missing_data(df)
            st.success("Filled missing data with mean/mode.")
        elif missing_option == "Task-specific Fill":
            impute_task_specific_values(df)
            st.success("Task-specific data filling applied.")

        # Display a bar chart of missing values
        missing_values = df.isnull().sum()
        if missing_values.any():
            st.bar_chart(missing_values)

# User Overview Analysis
elif selected_option == "User Overview":
    st.subheader("User Overview Analysis")
    
    # Top 10 handsets
    st.write("Top 10 Handsets")
    handset_counts = df['Handset Type'].value_counts().head(10)
    st.bar_chart(handset_counts)
    
    # Top 3 handset manufacturers
    st.write("Top 3 Manufacturers")
    manufacturer_counts = df['Handset Manufacturer'].value_counts().head(3)
    st.bar_chart(manufacturer_counts)
    
# User Engagement Analysis
elif selected_option == "User Engagement":
    st.subheader("User Engagement Analysis")
    
    # Show top users by data consumption
    df['Total Data'] = df['Total UL (Bytes)'] + df['Total DL (Bytes)']
    user_data = df.groupby('MSISDN/Number').agg({
        'Bearer Id': 'count',
        'Dur. (ms)': 'sum',
        'Total Data': 'sum'
    }).sort_values('Total Data', ascending=False).head(10)
    
    st.write("Top 10 Users by Data Usage")
    st.bar_chart(user_data['Total Data'])

# User Experience Analysis
elif selected_option == "User Experience":
    st.subheader("User Experience Analysis")
    
    # Analyze TCP and RTT
    df['Total_TCP'] = df['TCP DL Retrans. Vol (Bytes)'] + df['TCP UL Retrans. Vol (Bytes)']
    top_tcp_users = df[['MSISDN/Number', 'Total_TCP']].sort_values('Total_TCP', ascending=False).head(10)
    
    st.write("Top 10 Users by TCP Data")
    st.bar_chart(top_tcp_users.set_index('MSISDN/Number'))
    
    df['Total_RTT'] = df['Avg RTT DL (ms)'] + df['Avg RTT UL (ms)']
    top_rtt_users = df[['MSISDN/Number', 'Total_RTT']].sort_values('Total_RTT', ascending=False).head(10)
    
    st.write("Top 10 Users by RTT")
    st.bar_chart(top_rtt_users.set_index('MSISDN/Number'))






# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
# import sys
# import requests
# from io import StringIO

# # Adjust system path to include the parent directory
# parent_path = os.path.abspath('..')
# if parent_path not in sys.path: 
#     sys.path.insert(0, parent_path)

# # Function to fetch data from a GitHub repository
# def fetch_data_from_github():
#     url = 'https://raw.githubusercontent.com/Leulseged-Mesfin/Tellco-Analysis/task-3/Data/data.csv'
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         # Convert content to a DataFrame
#         return pd.read_csv(StringIO(response.text))
#     else:
#         st.error(f"Error fetching data from GitHub. Status code: {response.status_code}")
#         return pd.DataFrame()

# # Load data into DataFrame
# df = fetch_data_from_github()

# # Function to drop rows with missing values in key columns
# def remove_nan_rows(df):
#     important_columns = ['Bearer Id', 'Start', 'End', 'IMSI', 'MSISDN/Number']
#     df.dropna(subset=important_columns, inplace=True)

# # Function to handle missing values with mean/mode
# def impute_missing_data(df):
#     columns_to_fill = [
#         'DL TP < 50 Kbps (%)', '50 Kbps < DL TP < 250 Kbps (%)',
#         '250 Kbps < DL TP < 1 Mbps (%)', 'DL TP > 1 Mbps (%)',
#         'UL TP < 10 Kbps (%)', '10 Kbps < UL TP < 50 Kbps (%)',
#         '50 Kbps < UL TP < 300 Kbps (%)', 'UL TP > 300 Kbps (%)',
#         'Last Location Name', 'Avg RTT DL (ms)', 'Avg RTT UL (ms)',
#         'Nb of sec with Vol DL < 6250B', 'Nb of sec with Vol UL < 1250B'
#     ]
    
#     for col in columns_to_fill:
#         if col != 'Last Location Name':
#             df[col].fillna(df[col].mean(), inplace=True)
#         else:
#             df[col].fillna(df[col].mode()[0], inplace=True)

# # Handling missing values for specific task
# def impute_task_specific_values(df):
#     task_specific_columns = {
#         'MSISDN/Number': 'mean',
#         'Avg RTT DL (ms)': 'mean',
#         'Avg RTT UL (ms)': 'mean',
#         'Avg Bearer TP DL (kbps)': 'mean',
#         'Avg Bearer TP UL (kbps)': 'mean',
#         'TCP DL Retrans. Vol (Bytes)': 'mean',
#         'TCP UL Retrans. Vol (Bytes)': 'mean',
#         'Total_Avg_RTT': 'mean'
#     }
    
#     for col, method in task_specific_columns.items():
#         if col in df.columns:
#             df[col].fillna(df[col].mean(), inplace=True)

#     if 'Handset Type' in df.columns:
#         df['Handset Type'].fillna(df['Handset Type'].mode()[0], inplace=True)

# # Streamlit app layout
# st.title("Telecom Data Analytics Dashboard")

# # Sidebar for navigation
# st.sidebar.title("Choose Analysis")
# options = ["Dataset Exploration", "User Overview", "User Engagement", "User Experience"]
# selected_option = st.sidebar.selectbox("Select Analysis", options)

# # Dataset Exploration
# if selected_option == "Dataset Exploration":
#     st.subheader("Explore Dataset")

#     # Dropdown for data exploration
#     exploration = st.selectbox("Choose a view:", ["Head", "Tail", "Summary Stats", "Missing Data Info"])
    
#     if exploration == "Head":
#         st.dataframe(df.head())
#     elif exploration == "Tail":
#         st.dataframe(df.tail())
#     elif exploration == "Summary Stats":
#         st.dataframe(df.describe())
#     elif exploration == "Missing Data Info":
#         st.dataframe(df.isnull().sum())

#         # Choose how to handle missing values
#         missing_option = st.selectbox("Handle missing data:", ["None", "Drop Rows", "Fill Mean/Mode", "Task-specific Fill"])
        
#         if missing_option == "Drop Rows":
#             remove_nan_rows(df)
#             st.success("Dropped rows with missing values.")
#         elif missing_option == "Fill Mean/Mode":
#             impute_missing_data(df)
#             st.success("Filled missing data with mean/mode.")
#         elif missing_option == "Task-specific Fill":
#             impute_task_specific_values(df)
#             st.success("Task-specific data filling applied.")

# # User Overview Analysis
# elif selected_option == "User Overview":
#     st.subheader("User Overview Analysis")
    
#     # Top 10 handsets
#     st.write("Top 10 Handsets")
#     handset_counts = df['Handset Type'].value_counts().head(10)

#     # Use Matplotlib to create the bar chart
#     plt.figure(figsize=(10, 5))
#     plt.barh(handset_counts.index, handset_counts.values)
#     plt.xlabel('Count')
#     plt.ylabel('Handset Type')
#     plt.title('Top 10 Handsets')
#     st.pyplot(plt)

#     # Top 3 handset manufacturers
#     st.write("Top 3 Manufacturers")
#     manufacturer_counts = df['Handset Manufacturer'].value_counts().head(3)

#     # Plot manufacturers
#     plt.figure(figsize=(5, 5))
#     sns.barplot(x=manufacturer_counts.values, y=manufacturer_counts.index)
#     plt.title('Top 3 Manufacturers')
#     st.pyplot(plt)

# # User Engagement Analysis
# elif selected_option == "User Engagement":
#     st.subheader("User Engagement Analysis")
    
#     # Show top users by data consumption
#     df['Total Data'] = df['Total UL (Bytes)'] + df['Total DL (Bytes)']
#     user_data = df.groupby('MSISDN/Number').agg({
#         'Bearer Id': 'count',
#         'Dur. (ms)': 'sum',
#         'Total Data': 'sum'
#     }).sort_values('Total Data', ascending=False).head(10)
    
#     st.write("Top 10 Users by Data Usage")

#     # Plot data using Matplotlib
#     plt.figure(figsize=(10, 5))
#     plt.barh(user_data.index.astype(str), user_data['Total Data'])
#     plt.xlabel('Total Data (Bytes)')
#     plt.ylabel('User')
#     plt.title('Top 10 Users by Total Data Usage')
#     st.pyplot(plt)

# # User Experience Analysis
# elif selected_option == "User Experience":
#     st.subheader("User Experience Analysis")
    
#     # Analyze TCP and RTT
#     df['Total_TCP'] = df['TCP DL Retrans. Vol (Bytes)'] + df['TCP UL Retrans. Vol (Bytes)']
#     top_tcp_users = df[['MSISDN/Number', 'Total_TCP']].sort_values('Total_TCP', ascending=False).head(10)
    
#     st.write("Top 10 Users by TCP Data")

#     # Plot TCP data
#     plt.figure(figsize=(10, 5))
#     plt.barh(top_tcp_users['MSISDN/Number'].astype(str), top_tcp_users['Total_TCP'])
#     plt.xlabel('Total TCP (Bytes)')
#     plt.ylabel('User')
#     plt.title('Top 10 Users by TCP Data Usage')
#     st.pyplot(plt)

#     # Analyze RTT
#     df['Total_RTT'] = df['Avg RTT DL (ms)'] + df['Avg RTT UL (ms)']
#     top_rtt_users = df[['MSISDN/Number', 'Total_RTT']].sort_values('Total_RTT', ascending=False).head(10)
    
#     st.write("Top 10 Users by RTT")

#     # Plot RTT data
#     plt.figure(figsize=(10, 5))
#     plt.barh(top_rtt_users['MSISDN/Number'].astype(str), top_rtt_users['Total_RTT'])
#     plt.xlabel('Total RTT (ms)')
#     plt.ylabel('User')
#     plt.title('Top 10 Users by RTT')
#     st.pyplot(plt)