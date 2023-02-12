import streamlit as st
import pandas as pd
import utils

# Page configuration

st.set_page_config(page_title='Home', 
        page_icon="🏠", 
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

#============================================================



st.write('# Curry Company Growth Dashboard')

st.markdown("""
        Growth Dashboard was maked to keep tracking the restaurants and delivery person metrics and growth.

        ### How to use this Dashboard?
        #### -*Company view:*
            *#####- Managerial view: Behavior general metrics.*
            - Strategic view: Weekly growth indicators. 
            - Geographical view: Geolocation insights.
        - Delivery person view: 
            - monitoring of weekly growth indicators.
        - Restaurants view:
            - weekly restaurant growth indicators.
        ### Ask for help:
         https://www.linkedin.com/in/joao-paulo-barboza/
        """)














