import streamlit as st
import pandas as pd
import utils

# Page configuration

st.set_page_config(page_title='Home', 
        page_icon=None, 
        initial_sidebar_state="auto", menu_items=None)

# Data uploading

df = pd.read_csv('train.csv')
df2 = df.copy()

# Cleaning the code

df2 = utils.clean_code(df2)

#============================================================
#                STREAMLIT SIDEBAR  
#===========================================================

# loading the siderbar

df2 = utils.create_sidebar(df2)


