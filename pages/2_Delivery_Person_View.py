# Necessary importations

import streamlit as st
import pandas as pd
import plotly.express as px
import folium as fl
from streamlit_folium import folium_static
from haversine import haversine
import utils

# Page configuration

st.set_page_config(page_title='Delivery Person View', 
        page_icon='🚚', layout="wide", 
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


#============================================================================================
#                STREAMLIT LAYOUT  
#===========================================================================================

st.header('Marketplace - Customer View') 

# Creating the tables

managerial_view, tactical_view, geographical_view = st.tabs(['Managerial View', '_', '_'])  


with managerial_view:
    
    with st.container():
    
        st.markdown('### Overall Metrics')
        # Creating the columns
        the_greatest_age, the_lowest_age, best_ve_condition, worst_ve_condition = st.columns(4) 
        
        with the_greatest_age:
        
            the_greatest_age.metric(value=df2['Delivery_person_Age'].max(), label='The greatest age')
        
        with the_lowest_age:

            the_lowest_age.metric(value=df2['Delivery_person_Age'].min(), label='The lowest age')
        
        with best_ve_condition:
            
            best_ve_condition.metric(value=df2['Vehicle_condition'].max(), label='Best vehicle condition')
        
        with worst_ve_condition:
            worst_ve_condition.metric(value=df2['Vehicle_condition'].min(), label='Worst vehicle condition')

        st.markdown('''___''')
    
    with st.container():
        
        col01, col02 = st.columns(2)
        
        with col01:
            
            st.markdown('##### The average rating per delivery person.')

            avg_ratings_dperson = (df2[['Delivery_person_ID', 'Delivery_person_Ratings']]
                    .groupby('Delivery_person_ID')
                    .mean()
                    .reset_index())
 
            st.dataframe(avg_ratings_dperson) 

        with col02:
            
            with st.container():
                
                st.markdown('##### The average rating and standard deviation per traffic type.')
                
                std_avg_rating_by_trafic = (df2[['Delivery_person_Ratings', 'Road_traffic_density']]
                                    .groupby('Road_traffic_density')
                                    .agg({'Delivery_person_Ratings':['mean', 'std']}))

                std_avg_rating_by_trafic.columns = ['delivery_avg', 'delivery_std']
                std_avg_rating_by_trafic = std_avg_rating_by_trafic.reset_index()
                
                st.dataframe(std_avg_rating_by_trafic)
            

            with st.container():
                
                st.markdown('##### The average rating and standard deviation per weather conditions.')
                
                std_avg_rating_by_weatherconditions = (df2[['Delivery_person_Ratings', 'Weatherconditions']]
                                    .groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean', 'std']}))

                std_avg_rating_by_weatherconditions.columns = ['delivery_avg', 'delivery_std']
                std_avg_rating_by_weatherconditions = std_avg_rating_by_weatherconditions.reset_index()
                
                st.dataframe(std_avg_rating_by_weatherconditions)

    st.markdown('''___''')

    with st.container():

        col01, col02 = st.columns(2)

        with col01:
            
            st.markdown('##### The 10 fastest delivery person  per city')
            
            df = utils.fastest_lowest(df2, True)
            
            st.dataframe(df)

        with col02:

            st.markdown('##### The 10 lowest delivery person  per city')
            
            df = utils.fastest_lowest(df2)
            
            st.dataframe(df)






























































