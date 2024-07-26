import streamlit as st
import pandas as pd
import plotly.express as px

# Your existing functions
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Other"
    return categorical_map

def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelors"

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")

    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedComp']]
    df = df.rename({'ConvertedComp': "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()

    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)
    
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df["Country"].map(country_map)

    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != 'Other']

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    
    st.title("Explore Software Developers Salaries")
    st.write(
        """### Stack Overflow Developer Survey"""
    )
    data = df["Country"].value_counts().reset_index()
    data.columns = ['Country', 'Count'] 

    # Country Distribution Pie Chart
    fig1 = px.pie(data, names='Country', values='Count', title='Number of Data from Different Countries',
                  color_discrete_sequence=px.colors.sequential.Bluyl, hole=0.3)
    
    fig1.update_traces(textinfo='percent+label')
    st.plotly_chart(fig1)
   
    # Salary Distribution by Country
    st.write("""#### Salary Distribution by Country""")
    fig2 = px.box(df, x="Country", y="Salary", title="Salary Distribution by Country",
                  color="Country", color_discrete_sequence=px.colors.sequential.Bluyl)
    fig2.update_layout(xaxis_title="Country", yaxis_title="Salary")
    st.plotly_chart(fig2)

    # Average Salary by Education Level
    st.write("""#### Average Salary by Education Level""")
    avg_salary_by_ed = df.groupby("EdLevel")["Salary"].mean().sort_values().reset_index()
    fig3 = px.bar(avg_salary_by_ed, x="Salary", y="EdLevel", title="Average Salary by Education Level",
                  color="EdLevel", color_discrete_sequence=px.colors.sequential.Bluyl)
    fig3.update_layout(xaxis_title="Average Salary", yaxis_title="Education Level")
    st.plotly_chart(fig3)

    # Salary vs. Years of Experience
    st.write("""#### Salary vs. Years of Experience""")
    fig4 = px.scatter(df, x="YearsCodePro", y="Salary", color="Country", title="Salary vs. Years of Experience",
                      color_discrete_sequence=px.colors.sequential.Bluyl)
    fig4.update_layout(xaxis_title="Years of Experience", yaxis_title="Salary")
    st.plotly_chart(fig4)

    st.write("""
        ### Insights    
        - **Country Distribution**: This pie chart shows the distribution of survey responses from different countries.
        - **Salary Distribution by Country**: The boxplot illustrates the range and median salary for each country.
        - **Average Salary by Education Level**: This bar chart shows the average salary for different education levels.
        - **Salary vs. Years of Experience**: This scatter plot shows the relationship between years of experience and salary.
    """)
