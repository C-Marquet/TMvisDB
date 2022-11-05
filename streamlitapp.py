import streamlit as st
import pymongo
import pandas as pd
from utils import overview, sidebar, table, visualization, about, header, faq

st.set_page_config(page_title='TMvis-DB', page_icon="⚛️", layout="wide")

with open( ".streamlit\style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

####################################################################
## Initialize connection to DB ##
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["microscope"])


client = init_connection()
db = client.microscope.tmvis

## Initialize session ##
if 'rndm' not in st.session_state:
    st.session_state.rndm = False
if 'filt' not in st.session_state:
    st.session_state.filt = False
if 'tbl' not in st.session_state:
    st.session_state.tbl = pd.DataFrame()
if 'txt' not in st.session_state:
    st.session_state.txt = ''

####################################################################

####################################################################
## Sidebar ##
[selected_organismid, selected_domain, selected_kingdom, selected_type, selected_sp, selected_limit, select_random, selected_length] = sidebar.filters()
[selected_id, style, color_prot, spin] = sidebar.vis()
sidebar.end()
####################################################################

####################################################################
## Header ##
header.title()
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Database", "Visualization", "FAQ", "About"])

####################################################################

####################################################################
## Overview ##

with tab1:
    overview.intro()

####################################################################

####################################################################
## Database ##
with tab2:#
    df = pd.DataFrame()

    if st.session_state.rndm:
        st.session_state.filt = False
        st.session_state.txt = "The table below shows a random selection. To personalize your selection, use the sidebar filters. (Note: Your current random selection will not be saved after reloading.)"
        with st.spinner('Loading your data'):
            df = table.get_random(db, 100)
            st.session_state.tbl = df
        st.session_state.rndm = False
        st.experimental_rerun()

    if st.session_state.filt:
        st.session_state.rndm = False
        query_tbl = table.query(selected_organismid, selected_domain, selected_kingdom, selected_type, selected_sp, selected_length)
        try:
            with st.spinner('Loading your data'):
                df = table.get_data_tbl(db, query_tbl, selected_limit)
                st.session_state.txt = "The table below shows your personalized selection. For a random selection use the sidebar button."
                st.session_state.tbl = df
        except:
            st.error("There are no entries in TMvis-DB for your selection: topology (" + selected_type + ") and taxonomy ("+ selected_organismid+ '/ ' + selected_domain +", "+ selected_kingdom+ "). Please check FAQs if you believe there is something missing.", icon="🚨")
            st.session_state.txt = ''
        st.session_state.filt = False
        st.experimental_rerun()


    if len(st.session_state.txt) == 0:
        st.info("Use the sidebar to access TMvis-DB.")
    else:
        # Print results.
        st.caption(st.session_state.txt)
        table.show_tbl(st.session_state.tbl)
        # Download Button
        st.download_button("Download selection", table.convert_df(st.session_state.tbl), "file.csv", "text/csv", key='download-csv')

        # Visualize from table
        st.markdown("---")
        selected_dfid = st.selectbox("Choose an ID to visualize predicted transmembrane topology below", st.session_state.tbl["UniProt ID"], 0)
        st.caption("Use the visualization tab and side bar to change style and color scheme.")
        pred_tbl = visualization.get_data_vis(db, selected_dfid)
        visualization.vis(selected_dfid, pred_tbl[0], pred_tbl[1], style, color_prot, spin)

####################################################################

####################################################################
## 3D vis ##

with tab3:
    #load_vis_sdbr = st.checkbox('Load selected 3D structure')
    #if load_vis_sdbr:
    try:
        [pred_vis, df_vis] = visualization.get_data_vis(db, selected_id)
        visualization.vis(selected_id, pred_vis, df_vis, style, color_prot, spin)
    except:
        st.error("We are having trouble loading your structure. Please check whether you entered the correct UniProt Identifier.",icon="🚨")
        #st.stop()
    st.markdown("---")

####################################################################

####################################################################
## About ##
with tab4:
    faq.quest()
####################################################################

####################################################################
## About ##
with tab5:
    about.references()
    about.software()
    about.author()
    about.impr()

