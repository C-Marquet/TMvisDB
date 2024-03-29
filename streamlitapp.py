import streamlit as st
import pymongo
from pymongo.errors import ConnectionFailure
import pandas as pd
from app import faq, table, overview, visualization, about, sidebar, header

st.set_page_config(page_title='TMvisDB', page_icon="⚛️", layout="wide")


####################################################################
## Usage statistics
if 'usg_stats' not in st.session_state:
    st.session_state.usg_stats = False

if not st.session_state.usg_stats:
    warn = st.warning(
        "Welcome to TMvisDB. The authors of TMvisDB opted out of gathering any usage summary statistics.  \n"
        "However, this web application is implemented with Streamlit. "
        "Please familiarize yourself with [Streamlit's privacy policy](https://streamlit.io/privacy-policy) before proceeding. "
        "The authors of TMvisDB have no insight into or control over Streamlit's data collection process and, thus, cannot accept any liability for said process.", icon="🚨")
    placeholder_button = st.empty()
    user_stats = placeholder_button.button('Click here to continue to TMvisDB.')
    if user_stats:
        st.session_state.usg_stats = True
        placeholder_button.empty()
        warn.empty()
####################################################################

if st.session_state.usg_stats:
####################################################################
## Initialize connection to DB ##
# Uses st.experimental_singleton to only run once.
    @st.experimental_singleton
    def init_connection():
        return pymongo.MongoClient(**st.secrets["microscope"])

    client = init_connection()
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        db = client.microscope.tmvis
    except ConnectionFailure:
        st.error("Error establishing a connection to TMvisDB! Please try again later, and/or contact us here: tmvisdb@rostlab.org", icon="🚨")
        db = 0

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

        if db == 0:
            st.error(
                "Error establishing a connection to TMvisDB! Please try again later, and/or contact us here: tmvisdb@rostlab.org",
                icon="🚨")
        else:
            df = pd.DataFrame()

            if st.session_state.rndm:
                st.session_state.filt = False
                st.session_state.txt = "The table below shows a random selection. To personalize your selection, use the sidebar filters. (Note: Your current random selection will not be saved after reloading.)"
                with st.spinner('Loading your data'):
                    df = table.get_random(db, 50)
                    st.session_state.tbl = df
                st.session_state.rndm = False
                st.experimental_rerun()

            if st.session_state.filt:
                st.session_state.rndm = False
                query_tbl = table.query(selected_organismid, selected_domain, selected_kingdom, selected_type, selected_sp, selected_length)

                with st.spinner('Loading your data'):
                    df = table.get_data_tbl(db, query_tbl, selected_limit)

                    st.session_state.txt = "The table below shows your personalized selection: " \
                                           "topology (" + selected_type + "), " \
                                            "taxonomy (Organism ID: "+ selected_organismid+ ', Domain: ' + selected_domain +", Kingdom: "+ selected_kingdom+ "), length "+ str(selected_length) +"." \
                                            " For a random selection use the sidebar button."
                    st.session_state.tbl = df
                    #st.session_state.txt = ''
                st.session_state.filt = False
                st.experimental_rerun()

            if len(st.session_state.txt) == 0:
                st.info("Use the sidebar to access TMvisDB.")
            else:
                # Print results
                #st.write(table.query(selected_organismid, selected_domain, selected_kingdom, selected_type, selected_sp, selected_length))
                if st.session_state.tbl.empty:
                    st.error("There are no entries in TMvisDB for your selection: topology (" + selected_type + ") and taxonomy (Organism ID: "+ selected_organismid+ ', Domain: ' + selected_domain +", Kingdom: "+ selected_kingdom+ "). Please alter your search and try again, or check FAQs if you believe there is something missing.", icon="🚨")
                else:
                    if not selected_organismid.isnumeric() and len(selected_organismid)>0:
                        print(selected_organismid)
                        st.warning(
                            "The organism ID you entered is not numeric: " + selected_organismid + ". It is not included in your database query. Please check UniProt for the organism ID you are looking for.")

                    st.caption(st.session_state.txt)
                    table.show_tbl(st.session_state.tbl)
                    # Download Button
                    st.download_button("Download selection", table.convert_df(st.session_state.tbl), "file.csv", "text/csv", key='download-csv')

                    # Visualize from table
                    st.markdown("---")
                    selected_dfid = st.selectbox("Choose an ID to visualize predicted transmembrane topology below", st.session_state.tbl["UniProt ID"], 0)
                    visualization.vis(db, selected_dfid, style, color_prot, spin)

####################################################################

####################################################################
## 3D vis ##
    with tab3:
        if db == 0:
            st.error(
                "Error establishing a connection to TMvisDB! Please try again later, and/or contact us here: tmvisdb@rostlab.org",
                icon="🚨")
        else:
            try:
                visualization.vis(db, selected_id, style, color_prot, spin)
            except:
                st.error("Sorry, we could not visualize your selected protein. Please contact us, so we can help you with your search.",icon="🚨")
            st.markdown("---")

####################################################################

####################################################################
## FAQ ##
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

