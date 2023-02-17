import pandas as pd

## Define  color codes ##
import streamlit

top = ["Helix", "Helix", "Beta-Strand", "Beta-Strand", "inside", "outside", "Signal Peptide"]
abb = ["H", "h", "B", "b", "i", "o", "S"]
ori = ["IN-->OUT", "OUT-->IN", "IN-->OUT", "OUT-->IN", "inside", "outside", "NA"]
col = ["light green", "dark green", "light blue", "dark blue", "light grey", "dark grey", "pink"]
color_code_pred = pd.DataFrame(zip(top, abb, ori, col), columns=["Topology", "Abbreviation", "Orientation", "Color"])
color_code_af = pd.DataFrame(['Very low (pLDDT < 50)', 'Low (70 > pLDDT > 50)', 'Confident (90 > pLDDT > 70)', 'Very high (pLDDT > 90)'], columns=['pLDDT score'])

# Color codes for tables
def color_prediction(s):
    if s.loc['TMbed Prediction'] == 'S':
        color = 'pink'
    elif s.loc['TMbed Prediction'] == 'H':
        color = 'yellowgreen'
    elif s.loc['TMbed Prediction'] == 'h':
        color = 'darkgreen'
    elif s.loc['TMbed Prediction'] == 'B':
        color = 'lightblue'
    elif s.loc['TMbed Prediction'] == 'b':
        color = 'darkblue'
    elif s.loc['TMbed Prediction'] == 'i':
        color = 'darkgrey'
    else:
        color = 'grey'
    return [f'background-color: {color}']*len(s.index)

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

# colors for 3D transmembrane topology
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
