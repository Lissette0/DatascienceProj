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

st.title("Services/Programs' Demand for NYCHA residents 🌃") #title of the page
st.markdown("""---""")
st.subheader("Exploring Enrollment rates for services/programs provided to NYCHA Residents")
st.write("CSCI 39542 Data Science Project")
st.markdown("""---""")
st.subheader('Overview')
st.info("The New York City Housing Authority (NYCHA), is the largest public housing authority in North America, was created in 1935 to provide decent, affordable housing for low- and moderate-income New Yorkers. There has been a steady decline in federal and state funding for NYCHA (New York City Housing Authority) since 1998. The purpose of this project is to analyze the services that are the most impactful and used by public housing residents. This will demonstrate which services should receive more funding since they benefit more residents. Based on this, my hypothesis was that since NYCHA’s funding is plummeting, fewer residents are receiving the help they need through the services and programs that are available specifically for NYCHA residents. I use datasets from NYC Open Data to collect information on various different programs/services provided to NYCHA residents: SNAP(The Supplemental Nutrition Assistance Program), Cash Assistance, Workforce 1, and some financial services. Links and more information to these data sources can be found under ‘CITATIONS’ and ‘Data Used’. I mainly used streamlit, plotly, and matplotlib to make statistical analysis and run Linear fit trend lines on each program/service listed above. I look through the number of residents that enroll in a specific service each year and for some, how many of them reported to have benefited from that service/program. In the end, we see that the services that are most used (SNAP and Cash Assistance) are declining over the years. We also see that from all of the financial services available, the Empowerment Center Program is most beneficial to NYCHA residents. ")
st.subheader('Data Used')
with st.expander("See Descriptions"):
    st.write("""
            1) Summer Youth Employment Program (SYEP) for NYCHA Residents (CSV Data Format) : 
            This dataset contains information about the Summer Youth Employment Program (SYEP), a service offered by the Department of Youth and Community Development (DYCD) aimed at getting young New Yorkers paid work experience and career exploration opportunities. Each row in the dataset represents the number of public housing residents on a NYCHA Development-level who receive or utilize this service.

            2) SNAP and Cash Assistance for NYCHA Residents (CSV Data Format) :
            This dataset contains information about SNAP and Cash Assistance, services offered by the Department of Social Services (DSS)/Human Resources Administration (HRA) to help New Yorkers receive the federally-administered food benefits they qualify for. Each row in the dataset represents the number of public housing residents on a Borough-level who receive or utilize this service.

            3) Workforce 1 for NYCHA Residents by Borough (CSV Data Format):
            This dataset contains information about the Workforce 1 service, a service offered by the Department of Small Business Services (SBS) that connects New Yorkers to job opportunities. Each row in the dataset represents the number of public housing residents on a Borough-level who receive or utilize this service and how many of them were placed in full-time or part-time jobs.

            4) 2019 Financial Services for NYCHA Residents by Borough (CSV Data Format):
            5) 2017-18 Financial Services for NYCHA Residents by Borough (CSV Data Format):

            These 2 datasets contain information about NYCHA residents’ use of:

            a) NYC Financial Empowerment Centers: a program that provides free, one-on-one professional financial counseling and coaching to all NYC residents. Each row in the dataset represents the number of NYCHA residents on a Borough-level who utilized this service;

            b) EmpoweredNYC: is an initiative to assist New Yorkers with disabilities and their families to better manage their finances and become more financially stable. Each row in the dataset represents the number of NYCHA residents on a Borough-level who utilized this service;


            c) Residents CAN!: a program that provided free professional and peer-to-peer financial counseling and coaching to residents in targeted NYCHA developments;

            d) La Ventanilla: a program that helps connect the Mexican community in New York City to financial counseling and coaching, as well as Free Tax Preparation services


            e) Student Loan Debt clinic: is an initiative to help New Yorkers understand their student loans and how to repay them. Each row in the dataset represents the number of NYCHA residents on a Borough-level who utilized this service; and

            f) Ready to Rent: a program providing free one-on-one financial counseling to New Yorkers seeking to apply for affordable housing units through HPD’s Housing Connect lottery. Each row in the dataset represents the number of NYCHA residents on a Borough-level who utilized this service.

            This also contains information on whether or not these programs benefited them through increased credit scores and/or receiving financial counseling. 

    """)
st.subheader('Techniques')
st.info("""
With the bar graphs, I used statistical analysis of the datasets to get the sum of each service’s enrollment per year. With some datasets, I was able to do the same to get the number of residents that reported the service to be beneficial. I also did some comparisons between the number of residents who applied vs the number that were accepted and enrolled in the program. 
With the pie charts, I used Statistical analysis by finding the mean of each service/program’s enrollment for the 2-4 years, normalizing them, and visualizing it with pie charts. One shows the enrollment percentage for the 5 programs and services and the other shows the enrollment breakdown for the financial services. 
With the scatter plot line trend graph, I used Linear regression models to show the declining trend of enrollment of the services/programs. 
""")
with st.expander("CITATIONS"):
                st.write("""
                    DATA SOURCES

                    Summer Youth Employment Program (SYEP) for NYCHA Residents:
                    https://data.cityofnewyork.us/Social-Services/Summer-Youth-Employment-Program-SYEP-for-NYCHA-Res/acek-a5z6/data

                    SNAP and Cash Assistance for NYCHA Residents:
                    https://data.cityofnewyork.us/Social-Services/SNAP-and-Cash-Assistance-for-NYCHA-Residents-Local/ay6v-3gm3/data

                    Workforce 1 for NYCHA Residents by Borough:
                    https://data.cityofnewyork.us/Social-Services/Workforce-1-for-NYCHA-Residents-by-Borough-Local-L/v7hc-c85a/data

                    2017-18 Financial Services for NYCHA Residents:
                    https://data.cityofnewyork.us/City-Government/2017-18-Financial-Services-for-NYCHA-Residents-Loc/g4tm-nibn/data

                    2019 Financial Services for NYCHA Residents:
                    https://data.cityofnewyork.us/City-Government/Financial-Services-for-NYCHA-Residents-by-Borough-/2c9f-2ta9/data

                    Additional Links:
                    https://www.youtube.com/watch?v=-IM3531b1XU
                    https://docs.streamlit.io/streamlit-cloud/get-started
                    https://docs.streamlit.io/library/cheatsheet
                    https://pandas.pydata.org/docs/reference/general_functions.html
                    https://www1.nyc.gov/assets/nycha/downloads/pdf/NYCHA-Fact-Sheet_2019_08-01.pdf
                """)

#Storing/cleaning csv files to cache ################
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
#this function uses the raw data snap and cash to get the yearly sum of the number of residents that received benefits under snap and the number that recieved the cash assistance 
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

#storing Workforce 1 program for NYCHA Residents df
@st.cache
def RAWork(filename = "Workforce_1.csv"):
    df = pd.read_csv(filename)
    return df

#this uses the raw data of workforce 1 and groups the enrollment and the residents who benefited from it by the year by taking the sum
@st.cache(allow_output_mutation=True)
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

#get each financial program from fin() df and get the number of people who used the program 
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
#and how many people benefited from it by year
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


#storing the analysis from the Summer Youth df by amount applied and accepted per year
@st.cache
def year_sum():
    df = load_data()
    yearsDF = df.groupby(['Year']).sum()
    yearsDF['Year'] = [2018, 2019]
    return yearsDF

scDF = sc_data()
workDF = work_data()
finDF = financial_result1()
finDF1 = financial_result2()
yearsDF = year_sum()
raw_summeryouth = load_data()

#visulizations for all the bar graphs using the above dataframes 

st.subheader('Bar Graphs')
row4_1, row4_2 = st.columns((2,2))
row1_1, row1_2, row1_3 = st.columns((0.75,2.25,2))
with row1_1:
    plist = ["SNAP/Cash Assistance", "Financial Services", "Summer Youth", "WorkForce 1"]
    service = st.selectbox("Select a Program/Service:", plist)

with row1_2:
    if service == "SNAP/Cash Assistance":
        if st.checkbox('Show Analysis on: SNAP and Cash Assistance For NYCHA Residents'):
            st.write(scDF)
        fig0 = px.bar(scDF, x="Year", y=["Received benefits under SNAP", "Received benefits under Cash Assistance"], title="NYCHA Residents that reiceved SNAP and/or Cash Assistance ", barmode='group', height=600)
        st.plotly_chart(fig0)
        with row1_3:
            with st.expander("Conclusion"):
                st.write("""
                    For each year, both the SNAP and Cash Assistance programs decline. These two programs are shown to be the 
                    most commonly used by NYCHA residents. This could mean that there is not enough funding to continue to assist the residents with this service
                    even when it is in high demand. 
                """)

    elif service == "Summer Youth":
        #showing the raw data for Summer Youth 
        if st.checkbox('Show Raw Data: Summer Youth Employment Program (SYEP) for NYCHA Residents'):
            st.write(raw_summeryouth)
            st.write("Analysis on the raw data")
            st.write(yearsDF)
        #visualizing the analysis of the summer youth program by year 
        fig = px.bar(yearsDF, x="Year", y=["Applied for the program", "Were accepted and enrolled"], title="NYCHA Residents that Applied to Summer Youth Program Vs. were accepted" ,barmode='group', height=600)
        st.plotly_chart(fig)
        with row1_3:
            with st.expander("Conclusion"):
                st.write("""
                    The number of residents who applied for the Summer Youth program declined between 2018 and 2019, however, the 
                    amount that was accepted stayed close to the same. This could mean that there is a limited amount of spots 
                    available for NYCHA residents. 
                """)

    elif service == "Financial Services":
        if st.checkbox('Show Raw Data: 2017-19 Financial Services for NYCHA Residents'):
            rawFin = financial1()
            st.write(rawFin)
            rawFin2 = financial2()
            st.write(rawFin2)
        with row1_2:
            fig1 = px.bar(finDF, x="Year", y=["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"], title="NYCHA Residents that enrolled in the Financial Services ", barmode='group', width=600, height=400)
            st.plotly_chart(fig1)
        with row1_3:
            fig12 = px.bar(finDF1, x="Year", y=["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"], 
                            title="NYCHA Residents that Reported program to be beneficial ", barmode='group', width=600, height=400)
            st.plotly_chart(fig12)
        with st.expander("Conclusion"):
            st.write("""
                This displays all the programs that fall under Financial services.
                This graph shows that the financial service program with the most enrollment and the most reports about it being beneficial was the 'Empowerment Center Program'. This program 
                is also increasing throughout the years unlike the other programs listed in Financial services. This means that this 
                program is in high demand for NYCHA residents and should be given funding in order to keep it going. 
            """)
                
    else:
        fig01 = px.bar(workDF, x='Year', y=['Were accepted and enrolled', 'Placed into full-time or part-time jobs'], title="NYCHA Residents that enrolled/benefited from Workforce 1 Program ", barmode='group', height=600)
        st.plotly_chart(fig01)
        with row1_3:
            with st.expander("Conclusion"):
                st.write("""
                    This shows the significant difference between the number of residents that enroll in the Workforce 1 program and the number who are placed into full-time jobs. 
                    This demonstrates that while the enrollment rate is not decreasing, there should be greater demand for the program to 
                    aid residents in finding jobs. 
                """)
###end of bar graph visulization 

st.markdown("""---""")

#function to get the total amount of enrollment for financial services 
def combineFin():
    comb = financial_result1()
    comb["Total_financial"]= (comb.iloc[:, 1:-1].sum(axis=1)) + comb.iloc[: , -1]  #add all the columns for the financial services 
    comb.loc[len(comb.index)] = ['2020', None, None, None, None,None, None, None]
    return comb

comb = combineFin()

#creaing the pie charts data from the mean of enrollments for each service 
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

#doing the same as the function above put for all the services that fall under the financial services 
@st.cache
def pie_data1():  #this function takes the mean number of all the resisdents for each program/service and stores it into a series
    col_mean = finDF[["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"]].mean()
    values = [col_mean.iloc[0], col_mean.iloc[1], col_mean.iloc[2], col_mean.iloc[3],col_mean.iloc[4],col_mean.iloc[5]]
    values = [round(num, 4) for num in values]
    return values

#visuliazing the pie charts 
st.subheader('Pie Charts')
row3_1, row3_2, row3_3, row3_4 = st.columns((1,2,2,1))
with row3_1: 
    v = pie_data()
    labels = ["Financial Services", "SNAP", "Cash Assistance", "Workforce 1", "Summer Youth"]
    fig03 = go.Figure(data=[go.Pie(labels=labels, values=v)])
    fig03.update_layout(title="Percentage of Enrollment per Service/Program")
    st.plotly_chart(fig03)

with row3_3: 
    v1 = pie_data1()
    labels1 = ["Empowerment Center Program", "Residents CAN!", "La Ventanilla", "Ready to Rent", "EmpoweredNYC", "Student Loan Debt Clinic"] 
    fig04 = go.Figure(data=[go.Pie(labels=labels1, values=v1, marker_colors=["#FF97FF", "#FECB52", "#B6E880", "#FF6692", "#19D3F3", "#FFA15A"])])
    fig04.update_layout(title="Percentage of Enrollment by Financial Services",uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig04)

with st.expander("Conclusion"):
     st.write("""
         These charts show the percentage of enrollment for each Service/program. On the first chart, 'SNAP', 'Cash Assistance' and
         'Workforce 1' has the highest enrollment rates. 'Financial Services' is of very low percentage so I broke down the services that fall 
         under it on the hart to the right. Here we can tell that the financial services with the most enrollment are 'Empowerment Center Program', 'Residents CAN!', and 'Ready to Rent'. 
         This tells us that these services are in high demand, on top of that these services were also reported as most beneficial to the residents. Therefore funding should go to these 
         programs (or programs similar to this) for NYCHA residents. 

     """)

st.markdown("""---""")

st.subheader('Scatter Plot and Linear Trend Lines')

#getting Linear regression line
X = scDF["Year"]
Y = scDF["Received benefits under Cash Assistance"]
X= X.values.reshape(-1,1)
Y= Y.values.reshape(-1,1)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions


def legend_name(names):
    for i, new in enumerate(names):
        fig09.data[i].name = new

SummerYouth_enrollment = [None, 10329.0, 10643.0, None]
SummerYouthdf = pd.DataFrame(SummerYouth_enrollment, columns=['SummerYouth_enrollment'])
Workforce1_enrollment = [14319.0, 13007.0, 14268.0, None]


#scatter plot and linear trend visualizations 
row4_1, row4_2 = st.columns((2,2))
with row4_1:
    listyear = ["2017","2018","2019","2020"]
    fig09 = px.scatter(
        x=listyear,
        y=[scDF["Received benefits under Cash Assistance"].astype(float), scDF["Received benefits under SNAP"].astype(float), SummerYouthdf["SummerYouth_enrollment"], comb["Total_financial"].astype(float), Workforce1_enrollment],
        trendline="ols"
    )
    legend_name(["Cash Assistance", None, "SNAP", None, "Summer Youth", None, "Financial Services", None, "Workforce 1"])
    fig09.update_layout(
    title="Regression line For Each Service/Program",
    xaxis_title="Year",
    yaxis_title="Enrollment",
    legend_title="Service/Program")
    fig09.update_traces(marker_size=10)
    st.plotly_chart(fig09)

with row4_2:
    with st.expander("Conclusion"):
        st.write("""
            By grouping the enrollment for each service by year we can see that most of the Services
            and Programs have been declining yearly. The linear trends for each service/program also showcase this.
            SNAP and Cash Assistance programs have the highest enrollment, while Summer Youth, Financial Services, and Workforce 1 do 
            not have data to show for past 2019. However, those 3 services were the only ones to have an enrollment increase between a year 
            or two. Financial services and Workforce 1 have a significant decrease in enrollment in  2018. This could mean that the services 
            were not as available to residents due to budget cutbacks. In 2019, you see the enrollments spike up again, showing that 
            these services are useful to the residents.
        """)

st.markdown("""---""")


col1, col2, col3, col4, col5 = st.columns(5)
if col3.button("✨Thanks for reading my Project✨"):
    st.balloons()
