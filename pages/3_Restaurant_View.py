# Necessary importations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium as fl
from streamlit_folium import folium_static
import utils

# Page configuration

st.set_page_config(page_title='Rrestaurant View', 
        page_icon='🍱', layout="wide", 
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

st.header('Marketplace - Customer View') 

#============================================================================================
#                STREAMLIT LAYOUT  
#===========================================================================================

# Creating the tables

managerial_view, tactical_view, geographical_view = st.tabs(['Managerial View', '_', '_'])
                                                                
with managerial_view:                                           
    
    with st.container():
        
        col01, col02, col03, col04, col05, col06 = st.columns(6)
        
        with col01 :
           
            # The quantity of delivery person
            
            aux = utils.metrics_calc(df2, 1)

            col01.metric(value=aux, label='D. person quant.')

        with col02 :

            aux = utils.metrics_calc(df2, 2)
            
            col02.metric(value=aux, label= "AVG Distance")

        with col03 :
            
            # The average time of delivery during Festivals

            aux = utils.metrics_calc(df2, 3, 'yes', 'avg')
            
            col03.metric(value=aux, label='AVG Festival(yes)')
            
        with col04 :
            
            # The average time and std of delivery during Festivals                                                         
            
            aux = utils.metrics_calc(df2, 3, 'yes', 'std')
            
            col04.metric(value=aux, label='STD Festival(yes)')
    
        with col05 :
            
            aux = utils.metrics_calc(df2, 3, 'no', 'avg')

            col05.metric(value=aux, label='AVG Festival(no)')
    
        with col06 :
            
            aux = utils.metrics_calc(df2, 3, 'no', 'std')

            col06.metric(value=aux, label='STD Festival(no)')

        
    with st.container():

        col01, col02 = st.columns(2)           
        
        with col01:
        
            df_aux = (df2[['City', 'Time_taken(min)',]].groupby('City')
                              .agg({'Time_taken(min)': ['mean', 'std']}))
            
        
            df_aux.columns = ['Time_avg', 'Time_std']
            df_aux = df_aux.reset_index()

            fig = go.Figure()

            fig.add_trace(go.Bar(name='Control',
                                x=df_aux['City'],
                                y=df_aux['Time_avg'],
                                error_y= dict(type = 'data', array=df_aux['Time_std'])))

            fig.update_layout(barmode='group')
            st.plotly_chart(fig, use_container_width=True) 
     
        with col02:

            df_aux = (df2[['City','Type_of_order', 'Time_taken(min)',]].groupby(['City', 'Type_of_order'])
                              .agg({'Time_taken(min)': ['mean', 'std']}))
            df_aux.columns = ['Time_avg', 'Time_std']
            df_aux = df_aux.reset_index()

            st.dataframe(df_aux)

    with st.container():
        
        col01, col02 = st.columns(2)

        with col01:
     
            df2 = utils.update_dataset(df2)
            
            avg_distance = df2['Distance(km)'].mean()
            avg_distance_by_city = df2[['City', 'Distance(km)']].groupby('City').mean().reset_index()

            #Drawing a Pie Graphic
            fig = go.Figure( data = [go.Pie(labels = avg_distance_by_city["City"], 
                values = avg_distance_by_city['Distance(km)'], pull=[0, 0.1, 0])])
        
            st.plotly_chart(fig, use_container_width=True)

   
        with col02:
                
            df_aux = (df2[['City','Road_traffic_density', 'Time_taken(min)',]]
                    .groupby(['City', 'Road_traffic_density'])
                    .agg({'Time_taken(min)': ['mean', 'std']}))
            
            df_aux.columns = ['Time_avg', 'Time_std']
            df_aux = df_aux.reset_index()

            fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], 
                    values='Time_avg', color='Time_std', color_continuous_scale='RdBu', 
                    color_continuous_midpoint=df_aux['Time_std'].mean())


            st.plotly_chart(fig, use_container_width=True)





