import streamlit as st

def references():
    st.markdown("##### References  \n"
                "- Preprint for TMvisDB: [TMvisDB](https://www.biorxiv.org/)  \n"
                "- Structure predictions: [Alphafold DB](https://alphafold.ebi.ac.uk)  \n"
                "- Transmembrane topology predictions: [TMbed](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-022-04873-x)")

def software():
    st.markdown("##### Software   \n"
                "- Website: [Streamlit](https://streamlit.io), [pandas](https://pandas.pydata.org)   \n"
                "- Database: [MongoDB](https://www.mongodb.com), [pymongo](https://github.com/mongodb/mongo-python-driver)  \n"
                "- 3D Visualization: [py3Dmol](https://3dmol.csb.pitt.edu), [stmol](https://github.com/napoles-uach/stmol)")

def author():
    st.markdown("##### Development & Maintenance")
    st.markdown("- Author: [Céline Marquet](https://github.com/C-Marquet)  \n"
                "- Code Source: [Github](https://github.com/C-Marquet/TMvisDB)  \n"
                "- Resources: [Rostlab](https://rostlab.org)")