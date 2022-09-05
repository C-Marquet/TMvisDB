import streamlit as st
import pymongo
import pandas as pd
from utils import sidebar, table, visualization

st.set_page_config(page_title='TMvisDB', page_icon='🧬')

####################################################################
## Initialize connection to DB ##
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
[selected_domain, selected_kingdom, selected_type, selected_sp, selected_limit, select_random] = sidebar.filters()
[selected_id, style, color_prot, spin] = sidebar.vis()
sidebar.end()
####################################################################

####################################################################
## Table ##
st.title("Database")
df = pd.DataFrame()

if select_random:
    df = table.get_random(db, selected_limit)
else:
    query_tbl = table.query(selected_domain, selected_kingdom, selected_type, selected_sp)
    df = table.get_data_tbl(db, query_tbl, selected_limit)

# Hide Index column
# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

# Print results.
st.dataframe(df)
selected_dfid = st.selectbox("Choose an ID to visualize predicted transmembrane topology", df["UniProt ID"], 0)
st.write(f'Selected ID: {selected_dfid}')

st.markdown("---")
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

st.markdown("---")

####################################################################