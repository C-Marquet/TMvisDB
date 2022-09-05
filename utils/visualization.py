

import py3Dmol
from stmol import showmol
from urllib.request import urlopen
import requests
import streamlit as st


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
    view.setBackgroundColor('white')

    num_atom = 0
    atom_color = dict()
    # get TM colors
    for nr, res_type in enumerate(pred):
        if res_type == '.':
            atom_color[nr] = 'grey'
        elif res_type in ['B', 'H']:
            atom_color[nr] = 'green'
        elif res_type in ['b', 'h']:
            atom_color[nr] = 'blue'
        else:
            atom_color[nr] = 'pink'

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
    st.write(selected_id)
    st.write("sequence length ", len(seq), seq)
    st.write("prediction length", len(pred), pred)


