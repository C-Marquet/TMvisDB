import streamlit as st
import py3Dmol
from stmol import showmol

##############
# Header vis #
id = "A0A6J4QGY1"
#seq = "PLRVWMHVPVGASAQPEWRAGVSLSVPLDAGRRAPP"
#pred ="BBBBBBBBBoooooooobbbbbbbbbbiiiiiiiii"

seq = "MSTTSATPDPVVVRSTVPARMDRLPWTRFHWIVVVGLGVSWILDGLEIQIVSLNGPSLTDAAGSMHLSAAEFGALGSIYLAGEVVGALVFGRITDKLGRRKLFIITLAIYLVGSGLGGFAWDFWSLALFRFVAGTGIGGEYTAINSAIDELIPAKYRGRVDIAVNGTYWGGALLGNLVGLYLFSNNVSIDWGWRIGFFIGPVLGLVIIFLRRTIPESPRWLMTHGREEEAKRTVDDIEKRIEARGVELEPVPDSKAITLKETPPLGFAELTKIFFGKYPKRSVLGFTMMVTQAFLYNAIFFSYALVLKTFYGIPAGSIPLYFLPFALGNLLGPLLLGHLFDTIGRRKMILATYGGSGILLFITAFMFNAGILTATTQTILWCVIFFFASAGASSAYLTVSEIFPLELRGQAISYFFAISQGAGGVVAPWLFGKLIGNPDALASTGHAPPTGPLTWGYVIGASIMVIGGLVAWFIGIDAERKSLEDIATPLSAAEQPPGQGEMSEARS"
pred = "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiHHHHHHHHHHHHHHHHHHHHHHHHoooooooooooooooohhhhhhhhhhhhhhhhhhhhhhiiiiiiiHHHHHHHHHHHHHHHHHHHHoohhhhhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiHHHHHHHHHHHHHHHHHHHHHHHooooooooohhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiHHHHHHHHHHHHHHHHHHHHHHHHHooooooooooohhhhhhhhhhhhhhhhhhhhhhiiiiiiiHHHHHHHHHHHHHHHHHHHHHooooooohhhhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiHHHHHHHHHHHHHHHHHHHHHHHooooooooooooooooooohhhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiHHHHHHHHHHHHHHHHHHHHHHHHoooooooooooooooohhhhhhhhhhhhhhhhhhhhhhiiiiiiiHHHHHHHHHHHHHHHHHHHHoohhhhhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiHHHHHHHHHHHHHHHHHHHHHHHooooooooohhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiHHHHHHHHHHHHHHHHHHHHHHHHHooooooooooohhhhhhhhhhhhhhhhhhhhhhiiiiiiiHHHHHHHHHHHHHHHHHHHHHooooooohhhhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiHHHHHHHHHHHHHHHHHHHHHHHooooooooooooooooooohhhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"

pdb_file = open("header_A0A2T0ZVU5.pdb","r")
system = "".join([x for x in pdb_file])


##############


def title():
    st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap='small')
    col1.markdown("  \n")
    col1.markdown("  \n")
    col1.markdown("  \n")
    col1.markdown("# TMvis-DB")

    with col2:
        view = py3Dmol.view(js='https://3dmol.org/build/3Dmol.js', height=200, width=400)
        view.addModelsAsFrames(system)
        view.setBackgroundColor('#0E1117')
        view.spin(True)

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

        view.setStyle({'model': -1}, {'cartoon': {'colorscheme': {'prop': 'resi', 'map': atom_color}}})
        view.zoom(0.15)
        showmol(view, height=200, width=400)

    st.caption("Welcome to TMvis-DB: A database to search and visualize predicted transmembrane proteins.")





