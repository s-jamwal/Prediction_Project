import streamlit as st
import pickle
import numpy as np
from PIL import Image
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
data = load_model()
regressor_loader = data["model"]
le_Country = data["le_Country"]
le_education = data["le_education"]
def show_predict_page():
    
    st.title("💻 Software Developer Salary Prediction")
    st.write("""### Please provide some information to predict the salary""")


    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden"
    )
    educations = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad"
    )
    country = st.selectbox("🌎 Country", countries)
    education = st.selectbox("🎓 Education Level", educations)
    experience = st.slider("💼 Years of Experience", 0, 50, 3)
    btn = st.button("💵 Compute Salary")
    if btn:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_Country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)
        salary = regressor_loader.predict(X)
        st.subheader(f"🎉 The estimated salary is ${salary[0]:,.2f}")