import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

st.title('Impact NYCHA Services has on residents')

st.info("Funding for NYCHA has been decreasing since 1998, the purpose of this project is to analyze the services that are the most impactful and used by public housing residents. This will demosntrate which services should recieve more funding since they help more residents.")

st.info("The New York City Housing Authority (NYCHA), is the largest public housing authority in North America, was created in 1935 to provide decent, affordable housing for low- and moderate-income New Yorkers.  NYCHA is home to 1 in 15 New Yorkers. 564,301 New Yorkers in total are served by NYCHA’s public housing and Section 8 programs")


#Storing/cleaning csv files to cache ################

@st.cache
def load_data(filename = "SummerYouth.csv"):
    df = pd.read_csv(filename)
    dropCols = ['Average wage of residents','Enrolled in financial counseling services through the program','Enrolled in college-readiness courses or participated in college-readiness activities through the program']
    df = df.drop(columns=dropCols) # drop the cols from the dataframe
    df.drop(df.loc[df['NYCHA Development']=='Totals'].index, inplace=True)
    return df

@st.cache
def load_data1(filename = "SNAPandCASH.csv"):
    df = pd.read_csv(filename)
    return df

@st.cache
def year_sum():
    df = load_data()
    yearsDF = df.groupby(['Year']).sum()
    yearsDF['Year'] = [2018, 2019]
    return yearsDF

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

yearsDF = year_sum()

if st.checkbox('Show Raw Data'):
     st.write(yearsDF)


row1_4, row1_3 = st.columns((2,3))
with row1_4:
    chart_data = pd.DataFrame(yearsDF, columns=['Applied for the program', 'Were accepted and enrolled'])
    st.bar_chart(chart_data, height=400)

with row1_3:
    fig = px.bar(yearsDF, x="Year", y=["Applied for the program", "Were accepted and enrolled"], barmode='group', height=600)
# st.dataframe(df) # if need to display dataframe
    st.plotly_chart(fig)


row1_1, row1_2 = st.columns((3,2))

with row1_1:
    chart_data = pd.DataFrame( np.random.randn(20, 3), columns=['SNAP and Cash Service', 'Finanical Services', 'REEF/Workforce Service'])
    st.line_chart(chart_data)

with row1_2: 
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'SNAP and CASH Service', 'Summer Youth Service', 'Financial Services', 'Workforce Service'
    sizes = [15, 30, 45, 10]
    explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

#st.bar_chart([yearsDF['Applied for the program'], yearsDF['Were accepted and enrolled']])
# data = load_data(10000)

#data_load_state = st.text('Loading data...')

#data_load_state.text("Done! (using st.cache)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)




st.warning('More Visualizations to come...')


body = ''' 
#DBA
'''
#displaying the code 
if st.checkbox('Code done to get linear regression'):
    st.code(body, language = 'python')

