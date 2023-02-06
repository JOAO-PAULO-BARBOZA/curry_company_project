# Importations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium as fl
from streamlit_folium import folium_static

# Functions

def clean_code(df2):

    df2 = df2[df2['Delivery_person_Age'] != 'NaN ']
    df2 = df2[df2['City'] != 'NaN ']
    df2 = df2[df2['multiple_deliveries'] != 'NaN ']
    df2 = df2[df2['Road_traffic_density'] != 'NaN ']
    df2 = df2[df2['Festival'] != 'NaN ']

    df2['ID'] = df2['ID'].str.strip() # It's needed to call the method 'str' before the 'strip'
    df2['Delivery_person_Age'] = df2['Delivery_person_Age'].astype(int)
    df2['Delivery_person_Ratings'] = df2['Delivery_person_Ratings'].astype(float)
    df2['Order_Date'] = pd.to_datetime(df2['Order_Date'], format="%d-%m-%Y")
    df2['multiple_deliveries'] = df2['multiple_deliveries'].astype(int)
    df2['Road_traffic_density'] = df2['Road_traffic_density'].str.strip()
    df2['Type_of_order'] = df2['Type_of_order'].str.strip()
    df2['Type_of_vehicle'] = df2['Type_of_vehicle'].str.strip()
    df2['City'] = df2['City'].str.strip()

    # Removing unnecessery information in the column 'Time_taken(min)'
    # The information 'min' was removed of all lines
    df2['Time_taken(min)'] = df2['Time_taken(min)'].str.split(' ').apply(lambda x: x[1])
    df2['Time_taken(min)'] = df2['Time_taken(min)'].astype(int)
    
    return df2


def metrics_calc(df2, option, festival=None, calc=None):

    """ THIS FUNCTIONS CALCULATE THE METRICS OF DF2 BASED IN FOLLOWING 6 OPTIONS

        1 - NUMBER OF UNIQUE DELIVER PERSON
        2 - AVERAGE DISTANCE FROM THE RESTAURANT TO THE DELIVERY LOCATION
        3 - AVERAGE DISTANCE AND STANDARD DEVIATION FROM THE RESTAURANT TO THE 
        DELIVERY LOCATION DURING FESTIVALS (YES/NO)
        
        TO THE OPTION 3 IS NECESSAY INFORMATE THE ARGUMENTS festival(yes/no),
        AND WHAT KIND OF CALCULE WILL BE DONE, avg OR std.
    """

    if option == 1:
        res = len(df2['Delivery_person_ID'].unique())
        return res
    
    elif option == 2:
        
        update_dataset(df2) 
        
        avg_distance = df2['Distance(km)'].mean()

        return round(avg_distance, 1)
    
    elif (option == 3) and  (festival == 'yes') and (calc == 'avg'):
        # The average time of delivery during Festivals

        df_aux = df2[['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['del_time_avg', 'del_time_std']
        df_aux = df_aux.reset_index()

        res = round(df_aux['del_time_avg'][1], 1)

        return res
     
    elif (option == 3) and  (festival == 'no') and (calc == 'avg'):
        # The average time of delivery during Festivals

        df_aux = df2[['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['del_time_avg', 'del_time_std']
        df_aux = df_aux.reset_index()

        res = round(df_aux['del_time_avg'][0], 1)
        
        return res

    elif (option == 3) and  (festival == 'yes') and (calc == 'std'):
        # The average time of delivery during Festivals

        df_aux = df2[['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['del_time_avg', 'del_time_std']
        df_aux = df_aux.reset_index()

        res = round(df_aux['del_time_std'][1], 1)
        
        return res

    elif (option == 3) and  (festival == 'no') and (calc == 'std'):
        # The average time of delivery during Festivals

        df_aux = df2[['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['del_time_avg', 'del_time_std']
        df_aux = df_aux.reset_index()

        res = round(df_aux['del_time_std'][0], 1)
        
        return res


def update_dataset(df2):

    from haversine import haversine
        
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 
        'Delivery_location_latitude', 'Delivery_location_longitude']

    df2['Distance(km)'] = (df2[cols].apply(lambda x: haversine((x[0], x[1]), (x[2], x[3])), axis=1))

    return df2

def create_sidebar(df2):                                                                                                          

    from PIL import Image

    img = Image.open('fast-time.png') # 'Image' was imported from PIL lib.
    st.sidebar.image(img, width=120)
    
    st.sidebar.markdown('# Cury Company')                       
    st.sidebar.markdown('## Fastest Delivery in Town')                                                                            
    st.sidebar.markdown('''___''')      

    # Filter                                                                                                                          
    date_slider = st.sidebar.slider(
        'Date limit',
        value=pd.datetime(2022, 4, 13),
        min_value=pd.datetime(2022, 2, 11),
        max_value=pd.datetime(2022, 4, 6),
        format='DD-MM-YYYY'
    )

    st.sidebar.markdown('''___''')

    traffic_opt = st.sidebar.multiselect(
        'Traffic Conditions',
        ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
    )

    selected_lines = df2[df2['Order_Date'] < date_slider]

    df2 = selected_lines

    selected_lines = df2[df2['Road_traffic_density'].isin(traffic_opt)]
    df2 = selected_lines 
    

    st.sidebar.markdown('''___''')
    st.sidebar.markdown('###### *_Powered by J. Paulo B. Barboza_*')


    return selected_lines

def fastest_lowest(df2, a=False):

    df_aux = (df2[['Delivery_person_ID', 'City', 'Time_taken(min)']]
                      .groupby(['City', 'Delivery_person_ID'])
                      .mean()
                      .reset_index())

    # The 10 lowest delivery person in Metropolitian
    lowest_Metropolitian = (df_aux[df_aux['City'] == 'Metropolitian']
                                     .sort_values('Time_taken(min)', ascending=a).head(10))

    # The 10 lowest delivery person in Urban
    lowest_Urban = (df_aux[df_aux['City'] == 'Urban']
                                     .sort_values('Time_taken(min)', ascending=a).head(10))

    # The 10 lowest delivery person in Semi-Urban
    lowest_Semi_Urban = (df_aux[df_aux['City'] == 'Semi-Urban']
                                     .sort_values('Time_taken(min)', ascending=a).head(10))

    df4 = pd.concat([lowest_Metropolitian, lowest_Urban, lowest_Semi_Urban])
    return df4



















