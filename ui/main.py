import streamlit as st
import goes_ui as gu
import nexrad_ui as nu
import nexrad_map as nm
import datetime
import re
from datetime import date
from awscloud.s3 import main as s3
from awscloud.s3 import nexrad_main as nexs3
from utils.logger import Log

## Library Imports
import pandas as pd
import numpy as mp
import streamlit as st
import datetime
from datetime import date
import streamlit as st

def day_of_year(month, day):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        total_days = 0
        for i in range(month - 1):
            total_days += days_in_month[i]
        total_days += day
        if(len(str(total_days))==1):
            total_days = '00'+str(total_days)
        elif(len(str(total_days))==2):
            total_days = '0'+ str(total_days)
        return total_days
hours_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
sd = pd.read_fwf('https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt')
sd = sd.drop(index = 0,axis = 0)
station_id = sd['ICAO'].astype(str).to_list()
# print(sd)
# print(station_id)
# print(type(station_id))

def goes_ui():
   
    # # Check if 'key' already exists in session_state
    # # If not, then initialize it
    # if 'key' not in st.session_state:
    #     st.session_state['key'] = 'value'

    # # Session State also supports the attribute based syntax
    # if 'key' not in st.session_state:
    #     st.session_state.key = 'value'

    # # Store the initial value of widgets in session state
    # if "visibility" not in st.session_state:
    #     st.session_state.visibility = "visible"
    #     st.session_state.disabled = False

    # st.title('This is a title')
    st.title('Search By _File_ : :blue[GOES] Data')
    st.sidebar.markdown("# :blue[GOES] Search")
    st.subheader("Please select your Search Criteria")



    
    # Create the pandas DataFrame with column name is provided explicitly

    #----------------------------------------------------------
    # df = pd.read_csv('data.csv')
    # col_one_list = df['one'].tolist()
    # selectbox_01 = st.selectbox('Select', col_one_list)
    #----------------------------------------------------------
    # station = st.selectbox(
    #     'Select the required Station',
    #     list_df)

    
    station = 'ABI-L1b-RadC'
    st.write('You selected:', station)
    d = st.date_input(
        "Select the date",
        # value = datetime.date(2022, 7, 28),
        min_value= datetime.date(2022, 7, 28), max_value=date.today())
    st.write('Your Selection is:', d)
    day_goes = d.day
    month_goes = d.month
    year_goes = d.year
    Log().i(day_goes)
    Log().i(month_goes)
    Log().i(year_goes)

    # print('day' + ':'+ str(day_goes))
    # print('month' + ':'+ str(month_goes))
    ## Creating date of the year:

    doy = day_of_year(month_goes,day_goes)
    # print('day of year' + ':'+ str(doy))
    hour = st.selectbox(
        'Select the required Hour',
        hours_list)

    st.write('You selected:', hour)
    output_files = s3.get_all_geos_file_name_by_filter(station, str(year_goes),str(doy), str(hour))
    # print(output_files)



    if not output_files:
        st.markdown('**:red[data NOT available for given Inputs]**')
    else:
        st.write('')
    
    sl_file = st.selectbox('Select the required file for Link',output_files)
    Log().i(sl_file)
    ## Button code :

    # if st.button('Search',key = 'goes_file_output'):
    #     fo1 = s3.get_all_geos_file_name_by_filter(station, str(year_goes),str(doy), str(hour))
    #     print(fo1)
        
    # sl_file = st.selectbox('Select the required file for Link',fo1)
    if st.button('Generate Link', key ='goes_filed_search'):
        team_link, goes_link = s3.get_geos_aws_link(station,str(year_goes),str(doy), str(hour),str(sl_file))
        st.write('Our Link')
        st.write(team_link)
        st.write('GOES Link')
        st.write(goes_link)
        # o_df = pd.DataFrame(data = file_output, columns = ['File Name'])
        # l = []
        # for f in file_output:
        #     temp = s3.get_aws_link_by_filename(f)
        #     l.append(temp)
        # print(l)
        # l_df = pd.DataFrame(data = l,columns = ['File Link'])
        # fdf = o_df.join(l_df)
        # print(fdf)
        # st.write(fdf)
    else:
        st.write(' ')

    ##############################################################
    st.title('Search By _FileName_ : :blue[GOES] Data')
    st.subheader("Please input your File Name")
    # Text input :

    file_input = st.text_input('File Name','' )
    Log().i(file_input)

    ## Button code :
    regex = re.compile(r'(OR)_(ABI)-(L\d+b)-(Rad[A-Z]?)-([A-Z]\dC\d{2})_(G\d+)_(s\d{14})_(e\d{14})_(c\d{14}).nc')
    match = regex.match(file_input)
    if st.button('Generate the link',key = 'goes_file_search'):
        if match:
            # print("yes checked")
            file_name = s3.get_aws_link_by_filename(file_input)
            # print(file_name)
            if(file_name == None):
                st.markdown('**:red[File do not exists in Bucker]**')
            else:
                st.write(file_name)
        else:
           st.markdown('**:red[Input file not supported]**') 
    else:
        st.write(' ')

## Library Imports
import pandas as pd
import numpy as mp
import streamlit as st
import datetime

import streamlit as st


def nexrad_ui():

    # Check if 'key' already exists in session_state
    # If not, then initialize it
    # if 'key' not in st.session_state:
    #     st.session_state['key'] = 'value'

    # # Session State also supports the attribute based syntax
    # if 'key' not in st.session_state:
    #     st.session_state.key = 'value'

    # # Store the initial value of widgets in session state
    # if "visibility" not in st.session_state:
    #     st.session_state.visibility = "visible"
    #     st.session_state.disabled = False

    # st.title('This is a title')
    st.title('Search By _File_ : :blue[NEXRAD] Data')
    st.sidebar.markdown("# :blue[NexRad] Search")
    st.subheader("Please select your Search Criteria")
    

    #----------------------------------------------------------
    # df = pd.read_csv('data.csv')
    # col_one_list = df['one'].tolist()
    # selectbox_01 = st.selectbox('Select', col_one_list)
    #----------------------------------------------------------

    d = st.date_input(
        "Select the date",
        value = datetime.date(2023, 2, 4),
        min_value= datetime.date(2022, 1, 1), max_value=date.today())
    st.write('Your Selection is:', d)
    day_nexrad = d.day
    if(len(str(day_nexrad))==1):
        day_nexrad = '0'+str(day_nexrad)
    month_nexrad = d.month
    if(len(str(month_nexrad))==1):
        month_nexrad = '0'+str(month_nexrad)
    year_nexrad = d.year
    # print('day' + ':'+ str(day_nexrad))
    # print('month' + ':'+ str(month_nexrad))
    # print('year'+str(year_nexrad))
    Log().i(day_nexrad)
    Log().i(month_nexrad)
    Log().i(year_nexrad)

    station = st.selectbox(
        'Select the required Station',
        station_id)
    Log().i(station)

    st.write('You selected:', station)
    # print(str(station))
    output_files = nexs3.get_all_nexrad_file_name_by_filter(str(year_nexrad),str(month_nexrad), str(day_nexrad),str(station))
    # output_files = nexs3.get_all_nexrad_file_name_by_filter('2023', '02', '04', 'KABR')
    if not output_files:
        st.markdown('**:red[data NOT available for given Inputs]**')
    else:
        st.write('')
    # print(output_files)
    sl_file = st.selectbox('Select the required file for Link',output_files)
    Log().i(sl_file)
    ## Button code :

    if st.button('Generate Link', key ='nexrad_filed_search'):
        team_link, goes_link = nexs3.get_nexrad_aws_link(str(year_nexrad),str(month_nexrad), str(day_nexrad),str(station),str(sl_file))
        st.write('Our Link')
        st.write(team_link)
        st.write('NexRad Link')
        st.write(goes_link)
    else:
        st.write(' ')




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
    regex = re.compile(r'K[A-Z]{3}[0-9]{8}_[0-9]{6}(_V06_MDM)?')
    match = regex.match(file_input)
    if st.button('Generate the link',key = 'nexrad_file_search'):
        if match:
            Log().i("yes checked")
            file_name = nexs3.get_nexrad_aws_link_by_filename(file_input)
            if file_name == None:
                st.markdown('**:red[File not found in Database]**')
            else:
                st.write(file_name)
        else:
           st.markdown('**:red[Input file not supported]**')
    else:
        st.write(' ')


## Imports
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from data import Map_data_table_creation as ck
# st.title('This is a title')

def nexrad_map():
    st.markdown("# NexRad Map")
    st.sidebar.markdown("# NexRad Map")
    ### Call the function to pull Map data : 
    conn, cursor = ck.map_data_tbl()

    df = pd.read_sql_query("SELECT * from Mapdata", conn) 
    data = df
    st.subheader("Req data :")
    st.write(df) 

    st.subheader("Graph")
    fig = go.Figure(data=go.Scattergeo(
            locationmode = 'USA-states',
            lon = df['lon'],
            lat = df['lat'],
            text = df['name']+ ',' + df['county'],
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                symbol = 'square',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = 'Blues',
                cmin = 0,
                color = df['elev'].astype(int),
                cmax = df['elev'].astype(int).max(),
                colorbar_title="Elevation"
            )))

    fig.update_layout(
            title = 'NexRad Location Across USA',
            geo = dict(
                scope='usa',
                projection_type='albers usa',
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            ),
        )
    # Plot!
    st.plotly_chart(fig, use_container_width=False)


page_names_to_funcs = {
    "GOES Search": goes_ui,
    "NexRad Search": nexrad_ui,
    "NexRad Map": nexrad_map,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()