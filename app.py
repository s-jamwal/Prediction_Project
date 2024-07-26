import streamlit as st
from predictPage import show_predict_page
from explorePage import show_explore_page

sidePage = st.sidebar.selectbox("Explore or Predict" , ("Predict","Explore"))

if sidePage =="Predict":
    show_predict_page()
else:
    show_explore_page()










