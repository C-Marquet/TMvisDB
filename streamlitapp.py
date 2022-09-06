import streamlit as st
import pymongo
import pandas as pd
from utils import overview, sidebar, table, visualization, about, header
#from st_aggrid import AgGrid

st.set_page_config(page_title='TMvisDB', page_icon="⚛️")

####################################################################
## Initialize connection to DB ##
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    # pymongo.MongoClient("mongodb://localhost:27017/")
    return pymongo.MongoClient("mongodb+srv://marquet:testmongo@cluster0.b84qizg.mongodb.net/?retryWrites=true&w=majority")


client = init_connection()
db = client.tmvis
####################################################################

####################################################################
## Sidebar ##
[selected_domain, selected_kingdom, selected_type, selected_sp, selected_limit, select_random] = sidebar.filters()
[selected_id, style, color_prot, spin] = sidebar.vis()
sidebar.end()
####################################################################

####################################################################
## Header ##
header.title()
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Database", "Visualization", "About"])

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

    if select_random:
        st.markdown("The table below shows a random selection. To personalize your selection, use the filters in the sidebar.")
        df = table.get_random(db, selected_limit)
    else:
        st.markdown("The table below shows your personalized selection. To change a random selection, use the checkbox in the sidebar.")
        query_tbl = table.query(selected_domain, selected_kingdom, selected_type, selected_sp)
        try:
            df = table.get_data_tbl(db, query_tbl, int(selected_limit))
        except:
            st.error("You selected: topology (" + selected_type + ") and taxonomy ("+ selected_domain +", "+ selected_kingdom+ "). There are not entries in TMvisDB for this selection. Please contact the authors if you believe there is something missing.", icon="🚨")
            st.stop()

    # Print results.
    st.dataframe(df)
    #grid_response = AgGrid(df)
    #id = grid_response['data']["selected_rows"]
    #st.write(f'Selected ID: {id["UniProt ID"]}')

    st.markdown("---")
    selected_dfid = st.selectbox("Choose an ID to visualize predicted transmembrane topology below", df["UniProt ID"], 0)
    st.write(f'Selected ID: {selected_dfid}')

    load_vis_tbl = st.checkbox('Visualize selected prediction')
    if load_vis_tbl:
        pred_tbl = visualization.get_data_vis(db, selected_dfid)
        visualization.vis(selected_dfid, pred_tbl, 'cartoon', 'Transmembrane Prediction', 0)
        st.caption("Use the visualization tab and side bar to change style and color scheme.")
####################################################################

####################################################################
## 3D vis ##

with tab3:
    #load_vis_sdbr = st.checkbox('Load selected 3D structure')
    #if load_vis_sdbr:
    pred_vis = visualization.get_data_vis(db, selected_id)
    visualization.vis(selected_id, pred_vis, style, color_prot, spin)

    st.markdown("---")

####################################################################

####################################################################
## About ##
with tab4:
    about.references()
    about.software()
    about.author()