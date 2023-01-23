import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt

st.title("Time-Series Analysis of Customer Numbers")

# Load data
data = st.file_uploader('Upload data',type=['xlsx','csv'])
if data_file is not None :

    #AWS_BUCKET_URL = "https://drive.google.com/file/d/1DfRlDnuWYXeiRKUMUJpbE2C_-5BNt2FO/view?usp=sharing"
    #df = pd.read_csv(AWS_BUCKET_URL)
    df = pd.read_csv(data_file,encoding="shift-jis",parse_dates=True)

    df['計上日']= pd.to_datetime(df['計上日'])
    df['day'] = pd.DatetimeIndex(df['計上日']).day
    df['month'] = pd.DatetimeIndex(df['計上日']).month
    df['year'] = pd.DatetimeIndex(df['計上日']).year
    df.set_index('計上日',inplace=True)
    df['曜日'] = df.index.day_name()
    df['時間帯1'] = df['時間帯'].apply(lambda x: x[0:5])
    df.sort_values('時間帯1',inplace=True)
    #st.dataframe(df.head(100))

    col1 = st.sidebar
    col1.header('店舗を選択して下さい')
    
    data1 = df['店舗名'].unique()
    df1 = df.set_index('店舗名')
    option1 = col1.selectbox("店舗名",data1)
    df2_1 = df1.loc[option1]
    if option1 == '星置店' or '福井店':
        df2_1 = df2_1[df2_1['時間帯1']!='08:00']

    st.header('時間帯分析:')
    option2 = st.selectbox('分析したい項目を選択',
    ('客数', '売上金額(税抜)','荒利金額', '売上数量'))
    
    df_day = df[df['店舗名'] == option1]
    df_day = df_day.groupby(['計上日','曜日']).sum().reset_index()
    df_day_index = df_day['曜日'].unique()
    df_day_index = np.sort(df_day_index)


    df_day2 = df[df['店舗名'] == option1]
    df1_urage = df_day2.groupby(['計上日','day']).sum().reset_index()
    df1_urage_day = df1_urage.groupby('day').mean().reset_index()
    df_week = df1_urage_day['day'].unique()

    # Create user interface
    st.sidebar.header("Select Time Range")
    start_date = st.sidebar.date_input("Start date")
    end_date = st.sidebar.date_input("End date")
    chart_type = st.sidebar.selectbox("Select chart type", ["Line", "Bar"])

    # Filter data based on user input
    filtered_data = data[(data["date"] >= start_date) & (data["date"] <= end_date)]

    # Create chart
    if chart_type == "Line":
        plt.plot(filtered_data["date"], filtered_data["customer_numbers"])
        plt.xlabel("Date")
        plt.ylabel("Customer Numbers")
        st.pyplot()
    else:
        plt.bar(filtered_data["date"], filtered_data["customer_numbers"])
        plt.xlabel("Date")
        plt.ylabel("Customer Numbers")
        st.pyplot()

    # Add export data functionality
    if st.button("Export data"):
        st.write("Exported data to CSV.")
        filtered_data.to_csv("filtered_data.csv", index=False)
