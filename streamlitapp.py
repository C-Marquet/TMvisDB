import streamlit as st
import pymongo
import pandas as pd
from utils import sidebar, table, visualization

st.set_page_config(page_title='TMvisDB', page_icon='🧬')

####################################################################
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient("mongodb://localhost:27017/")

client = init_connection()
db = client.tmvis
####################################################################

####################################################################
## Sidebar ##
sidebar.intro()
[selected_domain, selected_kingdom, selected_type, selected_sp, selected_limit] = sidebar.filters()
[selected_id, style, color_prot, spin] = sidebar.vis()
sidebar.end()
####################################################################

####################################################################
## Table ##
st.title("Database")
load_tbl = st.checkbox('Load selected data')
df = pd.DataFrame()
if load_tbl:
    query_tbl = table.query(selected_domain, selected_kingdom, selected_type, selected_sp)
    df = table.get_data_tbl(db, query_tbl, selected_limit)
    # Print results.
    st.write(df)
    selected_dfid = st.selectbox("Choose an ID to visualize predicted transmembrane topology", df["UniProt ID"], 0)
    st.write(f'Selected ID: {selected_dfid}')
####################################################################

####################################################################
## 3D vis ##
st.title("Visualization")
load_vis = st.checkbox('Load selected 3D structure')
if load_vis:
    if selected_dfid:
        pred = visualization.get_data_vis(db, selected_dfid)
        st.info("ID selected from table")
    else:
        pred = visualization.get_data_vis(db, selected_id)
        st.info("ID selected from sidebar")
    visualization.vis(selected_id, pred, style, color_prot, spin)