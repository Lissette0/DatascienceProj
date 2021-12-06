import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

st.title('NYCHA Services Impact')

st.info("Funding for NYCHA has been decreasing since 1998, the purpose of this project is to analyze the services that are the most impactful and used by public housing residents. This will demosntrate which services should recieve more funding since they help more resisdents.")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')



@st.cache
def load_data(filename = "SummerYouth.csv"):
    df = pd.read_csv(filename)
    dropCols = ['Average wage of residents','Enrolled in financial counseling services through the program','Enrolled in college-readiness courses or participated in college-readiness activities through the program']
    df = df.drop(columns=dropCols) # drop the cols from the dataframe
    df.drop(df.loc[df['Applied for the program']=='NaN'].index, inplace=True)
    df.drop(df.loc[df['Were accepted and enrolled']=='NaN'].index, inplace=True)
    df.drop(df.loc[df['NYCHA Development']=='Totals'].index, inplace=True)
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

yearsDF = load_data()

if st.checkbox('Show Raw Data'):
     st.write(yearsDF)


chart_data = pd.DataFrame(yearsDF, columns=['Applied for the program', 'Were accepted and enrolled'])
st.bar_chart(chart_data, height=400)

fig = px.bar(yearsDF, x="Year", y=["Applied for the program", "Were accepted and enrolled"], barmode='group', height=600)
# st.dataframe(df) # if need to display dataframe
st.plotly_chart(fig)



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


#code showing blah blah blah 
body = ''' 
def mystery(*args):
       print(max(args)-min(args))


mystery(17,8,74,46)
'''
#displaying the code 
if st.checkbox('Code done to get linear regression'):
    st.code(body, language = 'python')

#balloons
#st.balloons()