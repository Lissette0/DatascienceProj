import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np 
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide", page_title='NYCHA DataScience', page_icon="✨")

st.title('Impact NYCHA Services has on Residents') #title of the page

st.info("Funding for NYCHA has been decreasing since 1998, the purpose of this project is to analyze the services that are the most impactful and used by public housing residents. This will demosntrate which services should recieve more funding since they help more residents.")

st.info("The New York City Housing Authority (NYCHA), is the largest public housing authority in North America, was created in 1935 to provide decent, affordable housing for low- and moderate-income New Yorkers.  NYCHA is home to 1 in 15 New Yorkers. 564,301 New Yorkers in total are served by NYCHA’s public housing and Section 8 programs")


#Storing/cleaning csv files to cache ################


#storing Summer youth Service dataframe 
@st.cache
def load_data(filename = "SummerYouth.csv"):
    df = pd.read_csv(filename)
    dropCols = ['Average wage of residents','Enrolled in financial counseling services through the program','Enrolled in college-readiness courses or participated in college-readiness activities through the program']
    df = df.drop(columns=dropCols) # drop the cols from the dataframe
    df.drop(df.loc[df['NYCHA Development']=='Totals'].index, inplace=True)
    return df

#storing SNAP and Cash Assistance for NYCHA Residents df
@st.cache
def RAWsnap(filename = "SNAPandCASH.csv"):
    df = pd.read_csv(filename)
    return df

@st.cache
def sc_data():
    snapdf = RAWsnap()
    dropCols = ['Submitted applications for benefits under SNAP','Were income-eligible for SNAP benefits','Submitted applications for benefits under Cash Assistance', 'Were income-eligible for Cash Assisstance']
    snapdf = snapdf.drop(columns=dropCols) # drop the cols from the dataframe
    snapdf['Year'] = snapdf['Year'].astype(str)
    snap = snapdf.groupby(['Year'], as_index=False)['Received benefits under SNAP'].sum()
    cash = snapdf.groupby(['Year'], as_index=False)['Received benefits under Cash Assistance'].sum()
    result = pd.merge(snap, cash, on=["Year"])
    return result

#end of snap and cash analysis ###########################



#storing Workforce 1 program for NYCHA Residents df
@st.cache
def RAWork(filename = "Workforce_1.csv"):
    df = pd.read_csv(filename)
    return df

#this function...
@st.cache()
def work_data():
    workdf = RAWork()
    workdf.drop(workdf.loc[workdf['Borough']=='Unknown'].index, inplace=True)
    dropCols = ['Applied for the program','Average Wage','Enrolled in college-readiness courses or participated in college-readiness activities through the program']
    workdf = workdf.drop(columns=dropCols)
    workdf['Placed into full-time or part-time jobs'] = (workdf.iloc[:, 3:8].sum(axis=1))
    workdf.drop(workdf.iloc[:,3:8] , axis=1, inplace=True)
    workdf["Were accepted and enrolled"] = workdf['Were accepted and enrolled'].astype(float)
    workdf["Placed into full-time or part-time jobs"] = workdf['Placed into full-time or part-time jobs'].astype(float)
    enroll = workdf.groupby(['Year'], as_index=False)['Were accepted and enrolled'].sum()
    bene = workdf.groupby(['Year'], as_index=False)['Placed into full-time or part-time jobs'].sum()
    result = pd.merge(enroll, bene, on=["Year"])
    return result



row2_1, row2_2 = st.columns((2,2))

with row2_1: 
    scDF = sc_data()
    fig0 = px.bar(scDF, x="Year", y=["Received benefits under SNAP", "Received benefits under Cash Assistance"], title="NYCHA Residents that reiceved SNAP and/or Cash Assistance ", barmode='group', height=600)
    st.plotly_chart(fig0)

with row2_2:
    st.warning("make a selectbox to put this on its own")
    workDF = work_data()
    fig01 = px.bar(workDF, x='Year', y=['Were accepted and enrolled', 'Placed into full-time or part-time jobs'], title="NYCHA Residents that enrolled/benefited from Workforce 1 Program ", barmode='group', height=600)
    st.plotly_chart(fig01)








#storing 2017-18 financial programs dataframe
@st.cache
def financial1(filename = "2019Financial_services.csv"):
    df = pd.read_csv(filename)
    return df

#storing 2019 financial programs dataframe
@st.cache
def financial2(filename = "2017-18_Financial_Services.csv"):
    df = pd.read_csv(filename)
    return df

if st.checkbox('Show Raw Data: 2017-19 Financial Services for NYCHA Residents'):
    rawFin = financial1()
    st.write(rawFin)
    rawFin2 = financial2()
    st.write(rawFin2)

#joining and cleaning the data from the two financial program data frames 
@st.cache
def fin():
    df1 = financial1()
    df2 = financial2()
    df1 = df1.append(df2)  #join 2019 data with the 2017-18 values dataframe
    nan_value = float("NaN")
    df1.replace("", nan_value, inplace=True) #replace empty values with NaN
    df1.dropna(how='all', axis=1, inplace=True) #drop columns that contain nothing in them 
    df1.fillna(0, inplace = True)   #fill NaN values with zero  
    df1.apply(pd.to_numeric, errors='ignore')
    return df1

#get each financial program from fin() df and get the number of people who used the program and how many people benefited from it by year

def finProgram(stringC):
    df = fin()
    new_df = df[df.columns[df.columns.to_series().str.contains(stringC)]] #get all the columns that contain the string (aka the name of the financial program)
    new_df['Reported_as_Beneficial']= (new_df.iloc[:, 1:-1].sum(axis=1)) + new_df.iloc[: , -1]  #add all the columns where resident reported the program to be helpful
    new_df.drop(new_df.iloc[:,1:-1] , axis=1, inplace=True) #drop uneeded cols
    #boro = df1.iloc[:,1] 
    #dfml.insert(loc=0, column='Borough', value=boro)
    years = df.iloc[:,0]
    new_df.insert(loc=0, column='Year', value=years) # insert years to the df 
    result= new_df.groupby(['Year'], as_index=False).sum() #group by year to get sum by year 
    return result


#Financial empowerment center program analysis
def program1():
    df = finProgram(stringC='Empowerment Center Program')
    df.rename(columns={ df.columns[1]: "Empowerment Center Program" }, inplace = True)
    return df

def program2():
    df = finProgram(stringC='CAN!')
    df.rename(columns={ df.columns[1]: "Residents CAN!" }, inplace = True)
    return df 

def program3():
    df = finProgram(stringC='La Ventanilla')
    df.rename(columns={ df.columns[1]: "La Ventanilla" }, inplace = True)
    return df

def program4():
    df = finProgram(stringC='Ready to Rent')
    df.rename(columns={ df.columns[1]: "Ready to Rent" }, inplace = True)
    return df

def program5():
    df = finProgram(stringC='EmpoweredNYC')
    df.rename(columns={ df.columns[1]: "EmpoweredNYC" }, inplace = True)
    return df

def program6():
    df = finProgram(stringC='Student Loan Debt Clinic')
    df.rename(columns={ df.columns[1]: "Student Loan Debt Clinic" }, inplace = True)
    return df

def financial_result1():
    lst = [2017,2018,2019]
    df1 = program1()
    col1 = df1.iloc[:, 1]
    df2 = program2()
    col2 = df2.iloc[:, 1]
    df3 = program3()
    col3 = df3.iloc[:, 1]
    df4 = program4()
    col4 = df4.iloc[:, 1]
    df5 = program5()
    col5 = df5.iloc[:, 1]
    df6 = program6()
    col6 = df6.iloc[:, 1]
    result = pd.DataFrame(lst, columns =['Year'])
    result = result.join([col1, col2, col3, col4, col5, col6])
    return result



def financial_result2():
    lst = [2017,2018,2019]
    df1 = program1()
    df1.rename(columns={ df1.columns[2]: "Empowerment Center Program" }, inplace = True)
    col1 = df1.iloc[:, 2]
    df2 = program2()
    df2.rename(columns={ df2.columns[2]: "Residents CAN!" }, inplace = True)
    col2 = df2.iloc[:, 2]
    df3 = program3()
    df3.rename(columns={ df3.columns[2]: "La Ventanilla" }, inplace = True)
    col3 = df3.iloc[:, 2]
    df4 = program4()
    df4.rename(columns={ df4.columns[2]: "Ready to Rent" }, inplace = True)
    col4 = df4.iloc[:, 2]
    df5 = program5()
    df5.rename(columns={ df5.columns[2]: "EmpoweredNYC" }, inplace = True)
    col5 = df5.iloc[:, 2]
    df6 = program6()
    df6.rename(columns={ df6.columns[2]: "Student Loan Debt Clinic" }, inplace = True)
    col6 = df6.iloc[:, 2]
    result = pd.DataFrame(lst, columns =['Year'])
    result = result.join([col1, col2, col3, col4, col5, col6])
    return result


row4_1, row4_2 = st.columns((2,2))
with row4_1:
    finDF = financial_result1()
    fig1 = px.bar(finDF, x="Year", y=["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"], title="NYCHA Residents that enrolled in the Financial Services ", barmode='group', height=600)
    st.plotly_chart(fig1)

with row4_2:
    finDF1 = financial_result2()
    fig12 = px.bar(finDF1, x="Year", y=["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"], 
                    title="NYCHA Residents that Reported program to be beneficial ", barmode='group', height=600)
    st.plotly_chart(fig12)




def combineFin():
    comb = financial_result1()
    comb["Total_financial"]= (comb.iloc[:, 1:-1].sum(axis=1)) + comb.iloc[: , -1]  #add all the columns where resident reported the program to be helpful
    comb.loc[len(comb.index)] = ['2020', None, None, None, None,None, None, None]
    return comb

comb = combineFin()


#storing the analysis from the Summer Youth df by amount applied and accepted per year
@st.cache
def year_sum():
    df = load_data()
    yearsDF = df.groupby(['Year']).sum()
    yearsDF['Year'] = [2018, 2019]
    return yearsDF



yearsDF = year_sum()
raw_summeryouth = load_data()
#showing the raw data for Summer Youth 
if st.checkbox('Show Raw Data: Summer Youth Employment Program (SYEP) for NYCHA Residents'):
     st.write(raw_summeryouth)
     st.write("Analysis on the raw data")
     st.write(yearsDF)


#visualizing the analysis of the summer youth program by year 
fig = px.bar(yearsDF, x="Year", y=["Applied for the program", "Were accepted and enrolled"], title="NYCHA Residents that Applied to Summer Youth Program Vs. were accepted" ,barmode='group', height=600)
st.plotly_chart(fig)




@st.cache
def pie_data():  #this function takes the mean number of all the resisdents for each program/service and stores it into a series
    df = finDF[["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"]]
    dfmean = df.mean().mean()
    values = [dfmean]
    col_mean = scDF["Received benefits under SNAP"].mean()
    values.append(col_mean)
    col_mean = scDF["Received benefits under Cash Assistance"].mean()
    values.append(col_mean)
    col_mean = workDF["Were accepted and enrolled"].mean()
    values.append(col_mean)
    col_mean = yearsDF["Were accepted and enrolled"].mean()
    values.append(col_mean)
    values = [round(num, 4) for num in values]
    return values

@st.cache
def pie_data1():  #this function takes the mean number of all the resisdents for each program/service and stores it into a series
    col_mean = finDF[["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"]].mean()
    values = [col_mean.iloc[0], col_mean.iloc[1], col_mean.iloc[2], col_mean.iloc[3],col_mean.iloc[4],col_mean.iloc[5]]
    values = [round(num, 4) for num in values]
    return values


row3_1, row3_2 = st.columns((2,2))
with row3_1: 
    v = pie_data()
    labels = ["Financial Services", "SNAP", "Cash Assistance", "Workforce 1", "Summer Youth"]
    fig03 = go.Figure(data=[go.Pie(labels=labels, values=v)])
    st.plotly_chart(fig03)

with row3_2: 
    v1 = pie_data1()
    labels1 = ["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"] 
    fig04 = go.Figure(data=[go.Pie(labels=labels1, values=v1, marker_colors=["#FF97FF", "#FECB52", "#B6E880", "#FF6692", "#19D3F3", "#FFA15A"])])
    fig04.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig04)



# rfig = px.scatter(scDF, x="Year", y="Received benefits under Cash Assistance", trendline="ols")
# st.write(rfig)

# df = px.data.tips()
# fig09 = px.scatter(df, x="total_bill", y="tip", trendline="ols")
# st.write(fig09)


#getting Linear regression line
X = scDF["Year"]
Y = scDF["Received benefits under Cash Assistance"]
X= X.values.reshape(-1,1)
Y= Y.values.reshape(-1,1)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions


def custom_legend_name(new_names):
    for i, new_name in enumerate(new_names):
        fig09.data[i].name = new_name

SummerYouth_enrollment = [None, 10329.0, 10643.0, None]
SummerYouthdf = pd.DataFrame(SummerYouth_enrollment, columns=['SummerYouth_enrollment'])

# work = work_data()
# work.loc[len(work.index)] = ['2020',None,None]
with st.echo(code_location='below'):
    listyear = ["2017","2018","2019","2020"]
    fig09 = px.scatter(
        x=listyear,
        y=[scDF["Received benefits under Cash Assistance"].astype(float), scDF["Received benefits under SNAP"].astype(float), SummerYouthdf["SummerYouth_enrollment"], comb["Total_financial"].astype(float)],
        trendline="ols"
    )
    custom_legend_name(["Cash Assistance", None, "SNAP", None, "Summer Youth", None, "Financial Services"])
    fig09.update_layout(
    title="Regression line For Each Service/Program",
    xaxis_title="Year",
    yaxis_title="Enrollment",
    legend_title="Service/Program")
    fig09.update_traces(marker_size=10)
    st.plotly_chart(fig09)

# row1_1, row1_2 = st.columns((1,4))
# with row1_1:
#     plist = ["SNAP", "Cash Assistance", "Financial Services", "Summer Youth", "WorkForce 1"]
#     service = st.selectbox("Select a Program/Service:", plist)

# with row1_2:
#     if service == "Cash Assistance":
#         rfig1 = px.scatter(scDF, x="Year", y="Received benefits under Cash Assistance", trendline="ols")
#         rfig1.update_traces(marker_size=10)
#         st.plotly_chart(rfig1)
#     elif service == "Summer Youth":
#         rfig2 = px.scatter(yearsDF, x="Year", y="Were accepted and enrolled", trendline="ols")
#         rfig2.update_traces(marker_size=10)
#         st.plotly_chart(rfig2)
#     elif service == "SNAP":
#         rfig3 = px.scatter(scDF, x="Year", y="Received benefits under SNAP", trendline="ols")
#         rfig3.update_traces(marker_size=10)
#         st.plotly_chart(rfig3)
#     else:
#         st.write("get cash")

st.warning('More Visualizations to come...')





body = ''' 
#DBA
'''
#displaying the code 
if st.checkbox('Code done to get linear regression'):
    st.code(body, language = 'python')

col1, col2, col3, col4, col5 = st.columns(5)
if col3.button("✨Thanks for reading my Project✨"):
    st.balloons()
