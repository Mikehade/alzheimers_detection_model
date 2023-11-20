import streamlit as st
from utils import nav_page
from os import system

st.set_page_config(layout="centered")

st.title('Alzheimers AI Pipeline')

st.markdown("## AI-Enabled Pipeline for Alzheimer's Disease Diagnosis Pipeline")

#value = st.number_input('Enter a number', 1, 10)


if st.button('Start'):
    nav_page('numeric_data')


