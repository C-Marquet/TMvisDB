

import py3Dmol
from stmol import showmol
from urllib.request import urlopen
import requests
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid


## Define  color codes ##
top = ["Helix", "Helix", "Beta-Strand", "Beta-Strand", "inside", "outside", "Signal Peptide"]
abb = ["H", "h", "B", "b", "i", "o", "S"]
ori = ["IN-->OUT", "OUT-->IN", "IN-->OUT", "OUT-->IN", "inside", "outside", "NA"]
col = ["light green", "dark green", "light blue", "dark blue", "light grey", "dark grey", "pink"]
color_code_pred = pd.DataFrame(zip(top, abb, ori, col), columns=["Topology", "Abbreviation", "Orientation", "Color"])
color_code_af = pd.DataFrame(['Very low (pLDDT < 50)', 'Low (70 > pLDDT > 50)', 'Confident (90 > pLDDT > 70)', 'Very high (pLDDT > 90)'], columns=['pLDDT score'])

# Color codes for tables
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

def color_expl_tmbed(s):
    if s == 'pink':
        color = 'pink'
    elif s == 'light green':
        color = 'yellowgreen'
    elif s == 'dark green':
        color = 'darkgreen'
    elif s == 'light blue':
        color = 'lightblue'
    elif s == 'dark blue':
        color = 'darkblue'
    elif s == 'dark grey':
        color = 'darkgrey'
    else:
        color = 'grey'
    return f'background-color: {color}'

def color_expl_af(val):
    if val == 'Very low (pLDDT < 50)':
        color = '#FF0000'
    elif val == 'Low (70 > pLDDT > 50)':
        color = '#FFA500'
    elif val == 'Confident (90 > pLDDT > 70)':
        color = '#00C900'
    elif val == 'Very high (pLDDT > 90)':
        color = '#0000FF'
    return f'background-color: {color}'


## Load TMvis-DB data ##
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

## Load AF structure ##
def get_af_structure(selected_id):
    # Initialize AF DB json file
    afdb_api_path = 'https://www.alphafold.ebi.ac.uk/api/prediction/' + selected_id
    afdb_json = requests.get(afdb_api_path).json()

    # get sequence
    seq = afdb_json[0]["uniprotSequence"]

    # get structure
    afdb_pdb_path = afdb_json[0]['pdbUrl']
    afdb_file = urlopen(afdb_pdb_path).read().decode('utf-8')
    system = "".join([x for x in afdb_file])
    return seq, system

## create color vector for transmembrane topology ##
def tm_color_structure(pred):
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
    return atom_color

## Additional information concerning visualization ##
def annotation(pred, df, seq, color_prot, selected_id):
    st.markdown("---")
    # Show Prediction if available
    if pred != 0:
        st.write('Prediction')
        pred_table = pd.DataFrame(zip(list(seq), list(pred)), columns=["Sequence", "Prediction"]).T.style.apply(color_prediction, axis = 0)
        st.write(pred_table)
        st.caption("Inside/outside annotations are not optimized and must be interpreted with caution.")

        # Show further sequence annotation
        st.write('Sequence Annotation')
        AgGrid(df.drop(columns=['Sequence','Prediction']), height=75, fit_columns_on_grid_load=True)

    # Explain Colors
    st.write('Color code')
    if color_prot == 'Alphafold pLDDT score' or pred == 0:
        st.write(color_code_af.style.applymap(color_expl_af, subset=["pLDDT score"]))
    else:
        st.write(color_code_pred.style.applymap(color_expl_tmbed, subset=["Color"]))

    st.markdown("---")

    # Link other resources
    link_up = f'- UniProt entry: [{selected_id}](https://www.uniprot.org/uniprotkb/{selected_id}/entry)  \n'
    link_lpp = f'- Evaluate protein-specific phenotype predictions: [LambdaPP](https://embed.predictprotein.org/#/interactive/{selected_id})  \n'
    link_fs = f'- Generate structural alignments: [Foldseek](https://search.foldseek.com/search)'

    st.markdown("Resources to evaluate your selection further:  \n")
    st.markdown(link_up)
    st.markdown(link_lpp)
    st.markdown(link_fs)


## Visualize ##
def vis(selected_id, pred, df, style, color_prot, spin):

    # visualize protein structure
    [seq, structure] = get_af_structure(selected_id)

    st.write("Displayed protein: ", selected_id)
    view = py3Dmol.view(js='https://3dmol.org/build/3Dmol.js')
    view.addModelsAsFrames(structure)
    view.setBackgroundColor('#262730')

    # add color
    if color_prot == 'Alphafold pLDDT score' or pred == 0:
        view.setStyle({'model': -1}, {style: {'colorscheme': {'prop': 'b', 'gradient': 'roygb', 'min': 50, 'max': 90}}})
    else:
        tm_color = tm_color_structure(pred)
        view.setStyle({'model': -1}, {style: {'colorscheme': {'prop':'resi', 'map': tm_color}}})
    # add spin
    if spin:
        view.spin(True)
    else:
        view.spin(False)

    #view.addResLabels()
    view.zoomTo()
    showmol(view, height=500, width=800)

    annotation(pred, df, seq, color_prot, selected_id)

