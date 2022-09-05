

import py3Dmol
from stmol import showmol
from urllib.request import urlopen
import requests
import streamlit as st
import pandas as pd

# define color code
top = ["Helix", "Helix", "Beta-Strand", "Beta-Strand", "inside", "outside", "Signal Peptide"]
abb = ["H", "h", "B", "b", "i", "o", "S"]
ori = ["IN-->OUT", "OUT-->IN", "IN-->OUT", "OUT-->IN", "inside", "outside", "NA"]
col = ["light green", "dark green", "light blue", "dark blue", "grey", "grey", "pink"]
color_code = pd.DataFrame(zip(top, abb, ori, col), columns=["Topology", "Abbreviation", "Orientation", "Color"])


def get_data_vis(db, selected_id):
    query = {"tmvis_id": selected_id}
    data_form = {"tmvis_pred": 1,
                 "_id": 0}
    prediction_vis = db.chunk0.find(query, data_form)[0]['tmvis_pred']
    return prediction_vis


def vis(selected_id, pred, style, color_prot, spin):

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
        else:
            color = 'grey'

        return [f'background-color: {color}'] * 2

    color_table = pd.DataFrame(zip(list(seq), list(pred)), columns=["Sequence", "Prediction"]).T.style.apply(color_prediction, axis = 0)

    st.write("Displayed protein ID: ", selected_id)
    st.write(color_table)
    st.write(color_code)

    st.caption("The inside/outside annotation is not optimized and must be interpreted with caution.")

