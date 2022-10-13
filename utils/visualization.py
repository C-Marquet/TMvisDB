

import py3Dmol
from stmol import showmol
from urllib.request import urlopen
import requests
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

# define color code
top = ["Helix", "Helix", "Beta-Strand", "Beta-Strand", "inside", "outside", "Signal Peptide"]
abb = ["H", "h", "B", "b", "i", "o", "S"]
ori = ["IN-->OUT", "OUT-->IN", "IN-->OUT", "OUT-->IN", "inside", "outside", "NA"]
col = ["light green", "dark green", "light blue", "dark blue", "light grey", "dark grey", "pink"]
color_code = pd.DataFrame(zip(top, abb, ori, col), columns=["Topology", "Abbreviation", "Orientation", "Color"])


def get_data_vis(db, selected_id):
    query = {"_id": selected_id}
    data_form = {'_id': 1,
                 'sequence': 1,
                 'predictions.transmembrane': 1,
                 'annotations.tm_categorical': 1,
                 'seq_length': 1,
                 'organism_name': 1,
                 'organism_id': 1,
                 'uptaxonomy.Lineage_all': 1,
                 'uptaxonomy.Domain': 1,
                 'uptaxonomy.Kingdom': 1}
    item = db.find(query, data_form)
    pred_vis = item[0]['predictions']['transmembrane']
    df_vis = pd.json_normalize(item)

    if len(df_vis.T) == 10:
        df_vis = df_vis[['_id', 'sequence', 'predictions.transmembrane', 'annotations.tm_categorical', 'seq_length', 'organism_name', 'organism_id', 'uptaxonomy.Lineage_all', 'uptaxonomy.Domain', 'uptaxonomy.Kingdom' ]]
        df_vis.columns = ['UniProt ID', 'Sequence', 'Prediction', 'Alpha / Beta / Signal', 'Sequence length', 'Organism name', 'Organism ID', 'Lineage', 'Domain', 'Kingdom']
    else:
        df_vis = df_vis[['_id', 'sequence', 'predictions.transmembrane', 'annotations.tm_categorical', 'seq_length', 'organism_name', 'organism_id']]
        df_vis.columns = ['UniProt ID', 'Sequence', 'Prediction', 'Alpha / Beta / Signal', 'Sequence length', 'Organism name', 'Organism ID']

    return pred_vis, df_vis


def vis(selected_id, pred, df, style, color_prot, spin):

    st.write("Displayed protein: ", selected_id)

    # Initialize AF DB json file
    afdb_api_path = 'https://www.alphafold.ebi.ac.uk/api/prediction/' + selected_id
    afdb_json = requests.get(afdb_api_path).json()

    # get sequence
    seq = afdb_json[0]["uniprotSequence"]

    # get structure
    afdb_pdb_path = afdb_json[0]['pdbUrl']
    afdb_file = urlopen(afdb_pdb_path).read().decode('utf-8')
    system = "".join([x for x in afdb_file])

    # visualize protein structure
    view = py3Dmol.view(js='https://3dmol.org/build/3Dmol.js')
    view.addModelsAsFrames(system)
    view.setBackgroundColor('#262730')

    num_atom = 0
    atom_color = dict()
    # get TM colors
    for nr, res_type in enumerate(pred):
        if res_type == 'S':
            atom_color[nr] = 'pink'
        elif res_type == 'H':
            atom_color[nr] = 'yellowgreen'
        elif res_type == 'h':
            atom_color[nr] = 'darkgreen'
        elif res_type == 'B':
            atom_color[nr] = 'powderblue'
        elif res_type == 'b':
            atom_color[nr] = 'darkblue'
        elif res_type == 'i':
            atom_color[nr] = 'darkgrey'
        else:
            atom_color[nr] = 'grey'

    if color_prot == 'Alphafold pLDDT score':
        view.setStyle({'model': -1}, {style: {'colorscheme': {'prop': 'b', 'gradient': 'roygb', 'min': 50, 'max': 90}}})
    else:
        view.setStyle({'model': -1}, {style: {'colorscheme': {'prop':'resi', 'map': atom_color}}})

    if spin:
        view.spin(True)
    else:
        view.spin(False)

    #view.addResLabels()
    view.zoomTo()
    showmol(view, height=500, width=800)

    # Colorcode sequence
    def color_prediction(s):
        if s.loc['Prediction'] == 'S':
            color = 'pink'
        elif s.loc['Prediction'] == 'H':
            color = 'yellowgreen'
        elif s.loc['Prediction'] == 'h':
            color = 'darkgreen'
        elif s.loc['Prediction'] == 'B':
            color = 'lightblue'
        elif s.loc['Prediction'] == 'b':
            color = 'darkblue'
        elif s.loc['Prediction'] == 'i':
            color = 'darkgrey'
        else:
            color = 'grey'
        return [f'background-color: {color}'] * 2

    def color_tab(s):
        if s['Abbreviation'] == 'S':
            color = 'pink'
        elif s['Abbreviation'] == 'H':
            color = 'yellowgreen'
        elif s['Abbreviation'] == 'h':
            color = 'darkgreen'
        elif s['Abbreviation'] == 'B':
            color = 'lightblue'
        elif s['Abbreviation'] == 'b':
            color = 'darkblue'
        elif s['Abbreviation'] == 'i':
            color = 'darkgrey'
        else:
            color = 'grey'
        return ['background-color: #0E1117','background-color: #0E1117','background-color: #0E1117', f'background-color: {color}']


    color_table = pd.DataFrame(zip(list(seq), list(pred)), columns=["Sequence", "Prediction"]).T.style.apply(color_prediction, axis = 0)

    st.write('Prediction')
    st.write(color_table)
    st.caption("Inside/outside annotations are not optimized and must be interpreted with caution.")

    st.write('Sequence Annotation')
    AgGrid(df.drop(columns=['Sequence','Prediction']), height=75, fit_columns_on_grid_load=True)

    st.write('Color code')
    st.write(color_code.style.apply(color_tab, axis = 1))#, fit_columns_on_grid_load=True)


