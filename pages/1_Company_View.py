# Necessary importations

import streamlit as st
import pandas as pd
import plotly.express as px
import folium as fl
from streamlit_folium import folium_static
from haversine import haversine
import utils

# Page configuration

st.set_page_config(page_title='Company View', 
        page_icon="🏢", layout="wide", 
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

st.header('Marketplace - Company View') 

#============================================================================================
#                STREAMLIT LAYOUT  
#===========================================================================================

# Creating the tables

managerial_view, tactical_view, geographical_view = st.tabs(['Managerial View', 'Tactical View', 'Geographical View'])


# Order quantity per day.

with managerial_view:
    
    with st.container():        
    
        st.markdown('## Order Quantity per day')
        #Line selection     
        df_aux = df2.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    
        #drawing the graphic
        fig = px.bar(df_aux, x='Order_Date', y='ID')

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''___''')
    
    with st.container():
        col01, col02 = st.columns(2)

        with col01:
        
            st.markdown('## Order distribution by type of traffic')    
            # Order distribution by type of traffic
            df_aux = df2[['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            df_aux['percentage'] = df_aux['ID']/df_aux['ID'].sum()
            #drawing the graphic
            fig = px.pie(df_aux, values='percentage', names='Road_traffic_density')
            st.plotly_chart(fig, use_container_width=True)

        with col02:
           
            st.markdown('## Order volume Comparison per city and type of traffic')    
            
            # Order's volume Comparison by city and type of traffic
            df_aux = (df2[['ID', 'City', 'Road_traffic_density']]
                    .groupby(['City', 'Road_traffic_density'])
                    .count()
                    .reset_index())
            
            #drawing the graphic
            fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
            st.plotly_chart(fig, use_container_width=True)            
        
        st.markdown('''___''')

with tactical_view:
     
    with st.container():

        st.markdown('## Order quantity per Week')    
        
        # Order quantity per Week.
        df2['week_of_year'] = df2['Order_Date'].dt.strftime('%U') #('%U') The counting of the days start from sunday
        df_aux = df2[['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        px.line(df_aux, x='week_of_year', y='ID')
        
        #drawing the graphic
        fig = px.line(df_aux, x='week_of_year', y='ID')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''___''')
    
    with st.container():
        
        st.markdown('## Order quantity per delivery person and per week')    
        
        # Grouping the quantity of orders by week of year
        df_aux01 = df2[['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        
        # Grouping the quantity of orders by unique id of delivery person
        df_aux02 = df2[['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
        
        # merging both dataframes
        df_aux = pd.merge(df_aux01, df_aux02, how='inner')
        
        # Quantity of delivery by each delivery person in a certain week of the year = qd_bydp_week
        df_aux['qd_bydp_week'] = df_aux['ID']/df_aux['Delivery_person_ID']

        #drawing the graphic
        fig = px.line(df_aux, x='week_of_year', y='qd_bydp_week')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''___''')

with geographical_view:    
    st.container():
    col01, col02 = st.columns(2)    
        with col01:
        
            # The central location of each city by type of traffic
            df_aux = (df2[['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                    .groupby(['City', 'Road_traffic_density'])
                    .median()
                    .reset_index())

            #drawing the graphic
            _map = fl.Map()

            for index, location in df_aux.iterrows():
                fl.Marker([location['Delivery_location_latitude'], 
                        location['Delivery_location_longitude']]).add_to(_map)
            folium_static(_map, width=1024, height=600)
       
        with col02:
        
            st.markdown('## The central location of each city by type of traffic')
            
            st.dataframe(df_aux)    







