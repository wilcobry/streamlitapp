import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from my_plots import *
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_csv('housing_finalapp.csv')
data = load_data()
data['Zipcode'] = data['Zipcode'].astype(str)

st.title('My Cool Housing App')

with st.sidebar:
    input_city = st.text_input('Enter a city in Utah County:', 'Provo')
    n_beds = st.radio('Number of beds', [1, 2, 3, 4, 5, 6])
    price_range = st.slider("Select a price range:",
                            min_value = int(data['Price'].min()),
                            max_value = int(data['Price'].max()),
                            value = (400000, 600000),
                            step = 10000)
    square_feet = st.slider("Select a house size:",
                            min_value = int(data['Sq_Footage'].min()),
                            max_value = int(data['Sq_Footage'].max()),
                            value = (1000, 2000),
                            step = 500)



tab1, tab2, tab3 = st.tabs(['City', 'Rooms by Price', 'Square Footage'])

with tab1: 
    st.header(f"Distribution of Housing Prices in {input_city}")
    city_data = data[data['City']==input_city].copy()
    fig = px.histogram(city_data, x='Price', 
                       nbins = 30,
                       labels = {
                           'Category': 'Price ($)',
                           'Values': 'Count'
                       })
    st.plotly_chart(fig)

with tab2:
    st.header(f"Distribution of Bedrooms Within \${price_range[0]} and \${price_range[1]}")
    price_data = data[(data['Price'] >= price_range[0]) & (data['Price'] <= price_range[1])].copy()
    fig2 = px.histogram(price_data, x= 'Beds',
                        nbins=6,
                        labels = {
                           'Category': 'Number of Beds',
                           'Values': 'Count'
                       })
    st.plotly_chart(fig2)
    st.header('Houses Within Price Range')
    st.dataframe(price_data.drop(columns=['Unnamed: 0']))

with tab3:
    st.header(f"Price by Square Footage for {n_beds} beds")
    sq_data = data[(data['Sq_Footage'] >= square_feet[0]) & (data['Sq_Footage'] <= square_feet[1]) & (data['Beds'] == n_beds)].copy()
    fig3 = px.scatter(sq_data, x='Sq_Footage', y='Price', hover_data = 'City',
                      labels = {
                           'Sq_Footage': 'Square Footage',
                           'Price': 'Price ($)'
                       })
    st.plotly_chart(fig3)


