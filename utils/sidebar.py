
import streamlit as st
import re
sb = st.sidebar

####################################################################
# Options: Filter
type_list = ['All', 'Both', 'Alpha-helix', 'Beta-strand']
domain_list = ['All', 'Bacteria', 'Eukaryota', 'Archaea', 'unclassified sequences']
kingdom_dict = dict()
kingdom_dict['Archaea'] = \
    ["All Archaea",
     "Asgard group",
    "Candidatus Hydrothermarchaeota",
    "Candidatus Thermoplasmatota",
    "DPANN group",
    "Euryarchaeota",
    "TACK group",
    "Archaea incertae sedis"
    "unclassified Archaea",
    "environmental samples"]
kingdom_dict['Eukaryota'] = \
    ["All Eukaryota",
    "Amoebozoa",
    "Ancyromonadida",
    "Apusozoa",
    "Breviatea",
    "CRuMs",
    "Cryptophyceae (cryptomonads)",
    "Discoba",
    "Glaucocystophyceae",
    "Haptista",
    "Hemimastigophora",
    "Malawimonadida",
    "Metamonada",
    "Opisthokonta",
    "Rhodelphea",
    "Rhodophyta (red algae)",
    "Sar",
    "Viridiplantae",
    "Eukaryota incertae sedis",
    "unclassified eukaryotes",
    "environmental samples"]
kingdom_dict["Bacteria"] = \
    ["All Bacteria",
    "Acidobacteria",
    "Aquificae",
    "Atribacterota",
    "Caldiserica/Cryosericota group",
    "Calditrichaeota",
    "Candidatus Krumholzibacteriota",
    "Candidatus Tharpellota",
    "Chrysiogenetes",
    "Coleospermum",
    "Coprothermobacterota",
    "Deferribacteres",
    "Desulfobacterota",
    "Dictyoglomi",
    "Elusimicrobia",
    "FCB group",
    "Fusobacteria",
    "Myxococcota",
    "Nitrospinae/Tectomicrobia group",
    "Nitrospirae",
    "Proteobacteria",
    "PVC group",
    "Spirochaetes",
    "Synergistetes",
    "Terrabacteria group",
    "Thermodesulfobacteria",
    "Thermotogae",
    "Bacteria incertae sedis",
    "unclassified Bacteria",
    "environmental samples"]

kingdom_dict['All'] = ["All"] + kingdom_dict['Archaea'] + kingdom_dict['Bacteria'] + kingdom_dict['Eukaryota']

####################################################################

def filters():
    sb.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    sb.markdown("---")
    sb.subheader("Search TMvisDB")
    sb.caption("Please open the 'Database' tab to see results.")

    emp = sb.empty()
    rand = emp.button('Show random selection', help='Click here to show 100 random proteins of TMvisDB.', disabled=st.session_state.rndm, key='1')

    if rand:
        st.session_state.rndm = True
        rand = emp.button('Show random selection', help='Click here to show 100 random proteins of TMvisDB.',
                          disabled=st.session_state.rndm, key='2')
        select_random = 1
        selected_type = 'All'
        selected_sp = '0'
        selected_organismid = '0'
        selected_domain = 'All'
        selected_kingdom = 'All'
        selected_limit = 100

    with sb.expander("Access filters for TMvisDB."):
        select_random = 0
        st.caption("Once you picked your filters, click the submit button below and open the 'Database' tab.")

        # select TMP type
        selected_type = st.selectbox('Filter by Transmembrane Topology ', type_list, help="TMbed predicts per-residue transmembrane topology as either alpha-helical or beta-stand.")
        selected_sp = st.checkbox('Show sequences with signal peptides', value=0, help="TMbed predicts whether a sequence contains signal peptides.")

        tax = st.radio("Select Taxonomy via", ('Organism ID', 'Domain/Kingdom'))
        if tax == 'Organism ID':
            dis_bx = True
            dis_org = False
            val = ''
        else:
            dis_bx = False
            dis_org = True
            val = '0'

        # select Taxonomy: Organism ID
        selected_organismid = st.text_input('Enter Organism ID', help="Type in UniProt Organism ID.", placeholder='9606', disabled=dis_org, value = val)
        # select Taxonomy: Domain
        selected_domain = st.selectbox('Select Domain', domain_list, help="Tyoe domain or select from list.", disabled=dis_bx)
        # select Taxonomy: Kingdom
        if selected_domain == "Bacteria":
            kingdom_list = kingdom_dict["Bacteria"]
        elif selected_domain == "Eukaryota":
            kingdom_list = kingdom_dict["Eukaryota"]
        elif selected_domain == "Archaea":
            kingdom_list = kingdom_dict["Archaea"]
        else:
            kingdom_list = kingdom_dict['All']
        selected_kingdom = st.selectbox('Select Kingdom', kingdom_list, help="Type kingdom or select from list.", disabled=dis_bx)

        # Sequence length range
        selected_length = st.slider('Select sequence length', 16, 1200, [16, 1200], help= "Select a minimum and maximum value for sequence length.")

        # Number of shown sequences
        selected_limit = st.number_input('Select limit of shown sequences', 1, 10000, value=100, help="As TMvis-DB is a large database, you may want to set a limit for your table.")

        # Submit results
        emp2 = st.empty()
        subm = emp2.button('Submit filters', help='Click here to show your selection.', disabled=st.session_state.filt, key='3')

        if subm:
            st.session_state.filt = True
            subm = emp2.button('Submit filters', help='Click here to show your selection.', disabled=st.session_state.filt, key='4')

    return selected_organismid, selected_domain, selected_kingdom, selected_type, selected_sp, selected_limit, select_random, selected_length


def vis():
    sb.markdown("---")
    st.sidebar.subheader("Visualize predicted transmembrane proteins")
    sb.caption("Please open the 'Visualization' tab to see results.")

    with sb.expander("Access 3D visualization of a protein."):
        # select ID
        selected_id = st.text_input('Insert Uniprot ID', placeholder ="Q9NVH1")
        selected_id = re.sub(r'[^a-zA-Z0-9]','', selected_id).upper()
        # select style
        style = st.selectbox('Style', ['Cartoon', 'Line', 'Cross', 'Stick', 'Sphere']).lower()
        # select color
        color_prot = st.selectbox('Color Scheme', ['Transmembrane Prediction', 'Alphafold pLDDT score'])
        # select spin
        spin = st.checkbox('Spin', value=False)
        if selected_id == '':
            selected_id="Q9NVH1"
    return selected_id, style, color_prot, spin

def end():
    sb.markdown("---")
    st.sidebar.write("Author: [Céline Marquet](https://github.com/C-Marquet)")
    st.sidebar.write("Source: [Github](https://github.com/marquetce/TMvisDB)")
