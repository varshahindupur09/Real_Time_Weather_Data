## Library Imports
import pandas as pd
import numpy as mp
import streamlit as st
import datetime

import streamlit as st

def nexrad_ui():

    # Check if 'key' already exists in session_state
    # If not, then initialize it
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'

    # Session State also supports the attribute based syntax
    if 'key' not in st.session_state:
        st.session_state.key = 'value'

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    # st.title('This is a title')
    st.title('Search By _File_ : :blue[NEXRAD] Data')
    st.sidebar.markdown("# NexRad Map")
    st.subheader("Please select your Search Criteria")

    ## Data for the dropdown
    data = [10,20,21,22,15,60]
    
    # Create the pandas DataFrame with column name is provided explicitly
    df = pd.DataFrame(data, columns=['Numbers'])
    list_df = df['Numbers'].tolist()

    #----------------------------------------------------------
    # df = pd.read_csv('data.csv')
    # col_one_list = df['one'].tolist()
    # selectbox_01 = st.selectbox('Select', col_one_list)
    #----------------------------------------------------------

    d = st.date_input(
        "Select the date",
        datetime.date(2022, 7, 6))
    st.write('Your Selection is:', d)


    station = st.selectbox(
        'Select the required Station',
        list_df)

    st.write('You selected:', station)

    ## Button code :

    if st.button('Generate the link'):
        st.write(' ')
    else:
        st.write('Look at me :::)) ')




    ##############################################################
    st.title('Search your NEXRAD file : :NEXRAD Data')
    st.subheader("Please input your File Name")
    # Text input :

    file_input = st.text_input('File Name','' )


    if file_input:
            st.write("File name entered: ", file_input)
    else:
            st.write('')

    ## Button code :

    if st.button('Search'):
        st.write(' ')
    else:
        st.write('Enter your file name again')

