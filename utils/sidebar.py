
import streamlit as st
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
    #select_random = sb.checkbox('Show random subset', value=1,
    #                            help="By default, a random subset of TMvisDB is shown. To apply the filters below, uncheck this box.")
    select_random = sb.radio(
        "How to select data",
        ('Random', 'Personalized'), help="Click 'Personalized' to select filters.")

    if select_random == 'Random':
        select_random = 1
        selected_type = 'All'
        selected_sp = '0'
        selected_domain = 'All'
        selected_kingdom = 'All'
        selected_limit = 100
    else:
        with sb.expander("Access filters for TMvisDB."):
            select_random = 0
            # select TMP type
            selected_type = st.selectbox('Filter by Transmembrane Topology ', type_list, help="TMbed predicts per-residue transmembrane topology as either alpha-helical or beta-stand.")
            selected_sp = st.checkbox('Show sequences with signal peptides', value=0, help="TMbed also predicts whether a sequence contains signal peptides.")
            # select Taxonomy: Domain
            selected_domain = st.selectbox('Filter by Taxonomy: Domain', domain_list, help="Select a domain.")
            # select Taxonomy: Kingdom
            if selected_domain == "Bacteria":
                kingdom_list = kingdom_dict["Bacteria"]
            elif selected_domain == "Eukaryota":
                kingdom_list = kingdom_dict["Eukaryota"]
            elif selected_domain == "Archaea":
                kingdom_list = kingdom_dict["Archaea"]
            else:
                kingdom_list = kingdom_dict['All']
            selected_kingdom = st.selectbox('Filter by Taxonomy: Kingdom', kingdom_list, help="Select a kingdom.")
            # Number of shown sequences
            selected_limit = st.number_input('Select limit of shown sequences', 1, 1000, value=100, help="As TMvisDB is a large database, you may want to set a limit for your table.")

    return selected_domain, selected_kingdom, selected_type, selected_sp, selected_limit, select_random


def vis():
    sb.markdown("---")
    st.sidebar.subheader("Visualize predicted transmembrane proteins")

    with sb.expander("Access 3D visualization of a protein."):
        # select ID
        selected_id = st.text_input('Insert Uniprot ID', value ="A3Z0C4")
        # select style
        style = st.selectbox('Style', ['Cartoon', 'Line', 'Cross', 'Stick', 'Sphere']).lower()
        # select color
        color_prot = st.selectbox('Color Scheme', ['Transmembrane Prediction', 'Alphafold pLDDT score'])
        # select spin
        spin = st.checkbox('Spin', value=False)
    return selected_id, style, color_prot, spin

def end():
    sb.markdown("---")
    st.sidebar.write("Author: [Céline Marquet](https://github.com/C-Marquet)")
    st.sidebar.write("Source: [Github](https://github.com/C-Marquet/TMvisDB)")