
import streamlit as st
sb = st.sidebar
from PIL import Image

####################################################################
# FILTER OPTIONS

type_list = ['All', 'Both','Alpha-helix', 'Beta-barrel']
domain_list = ['All', 'Bacteria', 'Eukaryota', 'Archaea', 'unclassified sequences']
kingdom_list = ['All', 'Bacteroidetes', 'Viridiplantae', 'Gemmatimonadetes', 'Thaumarchaeota', 'Proteobacteria', 'Cyanobacteria', 'Actinobacteria', 'Metazoa', 'Rhodophyta', 'environmental samples', 'Firmicutes', 'Fungi', 'Sar', 'metagenomes', 'Planctomycetes', 'Fusobacteria', 'Aquificae', 'Candidatus Saccharibacteria', 'Verrucomicrobia', 'Candidatus Woesebacteria', 'Euryarchaeota', 'Discoba', 'Synergistetes', 'Glaucocystophyceae', 'Cryptophyceae', 'Acidobacteria', 'Tenericutes', 'Fibrobacteres', 'Chlamydiae', 'Deinococcus-Thermus', 'Crenarchaeota', 'unclassified Parcubacteria group', 'Spirochaetes', 'Candidatus Thermoplasmatota', 'Asgard group', 'Chloroflexi', 'Candidatus Gottesmanbacteria', 'Candidatus Moranbacteria', 'Metamonada', 'Candidatus Bipolaricaulota', 'Elusimicrobia', 'Candidatus Stahlbacteria', 'Amoebozoa', 'Haptista', 'Candidatus Poribacteria', 'unclassified candidate division Zixibacteria', 'candidate division GN15', 'Candidatus Aminicenantes', 'Candidatus Rokubacteria', 'Candidatus Giovannonibacteria', 'candidate division WS2', 'Calditrichaeota', 'Thermotogae', 'Nitrospirae', 'Candidatus Marinimicrobia', 'Candidatus Dojkabacteria', 'Candidatus Peregrinibacteria', 'Candidatus Roizmanbacteria', 'candidate division TA06', 'Chlorobi', 'Candidatus Gracilibacteria', 'Candidatus Bathyarchaeota', 'Candidatus Altiarchaeota', 'Candidatus Latescibacteria', 'Lentisphaerae', 'Candidatus Parcubacteria', 'Candidatus Aerophobetes', 'Candidatus Dadabacteria', 'Atribacterota', 'Armatimonadetes', 'candidate division WWE3', 'Candidatus Microgenomates', 'Candidatus Falkowbacteria', 'Candidatus Edwardsbacteria', 'Candidatus Cloacimonetes', 'Candidatus Omnitrophica', 'candidate division KSB1', 'Ignavibacteriae', 'Candidatus Collierbacteria', 'Candidatus Micrarchaeota', 'Candidatus Hydrogenedentes', 'Candidatus Dependentiae', 'Candidatus Kaiserbacteria', 'Candidatus Vecturithrix', 'Candidatus Berkelbacteria', 'Candidatus Fermentibacteria', 'Candidatus Woesearchaeota', 'candidate division WOR-3', 'Balneolaeota', 'Candidatus Magasanikbacteria', 'Candidatus Wolfebacteria', 'Nitrospinae/Tectomicrobia group', 'Chrysiogenetes', 'Candidatus Shapirobacteria', 'Coprothermobacterota', 'Candidatus Pacearchaeota', 'Candidatus Margulisbacteria', 'Candidatus Amesbacteria', 'candidate division CPR1', 'Candidatus Delongbacteria', 'candidate division CPR2', 'Candidatus Korarchaeota', 'candidate division NC10', 'Candidatus Uhrbacteria', 'candidate division Kazan-3B-28', 'Deferribacteres', 'Candidatus Yanofskybacteria', 'Candidatus Eisenbacteria', 'Candidatus Daviesbacteria', 'Candidatus Nomurabacteria', 'Nanoarchaeota', 'Candidatus Kuenenbacteria', 'Candidatus Coatesbacteria', 'Candidatus Adlerbacteria', 'Candidatus Schekmanbacteria', 'Candidatus Levybacteria', 'Candidatus Aenigmarchaeota', 'Dictyoglomi', 'Candidatus Nealsonbacteria', 'Candidatus Melainabacteria', 'Thermodesulfobacteria', 'Candidatus Curtissbacteria', 'Candidatus Saganbacteria', 'Candidatus Beckwithbacteria', 'Candidatus Sumerlaeota', 'Candidatus Handelsmanbacteria', 'Candidatus Huberarchaea', 'Candidatus Azambacteria', 'Candidatus Desantisbacteria', 'Candidatus Dormibacteraeota', 'Candidatus Undinarchaeota', 'Candidatus Diapherotrites', 'Microgenomates group incertae sedis', 'Candidatus Hydrothermarchaeota', 'Candidatus Parvarchaeota', 'Candidatus Pacebacteria', 'Candidatus Jorgensenbacteria']
####################################################################
image = Image.open('img.png')


def intro():
    col1, col2 = sb.columns([0.8, 0.2])
    col1.title("TMvisDB")
    col2.image(image, width=150)

    sb.info(
        """
    Welcome to TMvisDB! We provide a comprehensive overview of predicted transmembrane proteins for all protein sequences available in Alphafold DB.
    
    -> To access the TMvisDB, please apply one or more of the filters below.
    
    -> To directly show the 3D visualization of a protein, type in a Uniprot identifier.
    
    -> You may also select a row of the table you generated.
    """
    )


def filters():
    st.sidebar.subheader("Filter by Topology and/or Taxonomy")
    # select TMP type
    selected_type = st.sidebar.selectbox('Select by Transmembrane Topology ', type_list)
    selected_sp = st.sidebar.checkbox('Include sequences with signal peptides', value=0)
    # select Taxonomy
    selected_domain = st.sidebar.multiselect('Select by Taxonomy: Domain', domain_list, default='All')
    selected_kingdom = st.sidebar.multiselect('Select by Taxonomy: Kingdom', kingdom_list, default='All')
    # Number of shown sequences
    selected_limit = st.sidebar.number_input('Insert number of shown sequences', 1, 1000, value=100)
    return selected_domain, selected_kingdom, selected_type, selected_sp, selected_limit

def vis():
    # select ID
    selected_id = st.sidebar._text_input('Select protein', value ="A3Z0C4")
    # select style
    style = st.sidebar.selectbox('Style', ['Cartoon', 'Line', 'Cross', 'Stick', 'Sphere', 'Clicksphere']).lower()
    # select color
    color_prot = st.sidebar.selectbox('Color Scheme', ['Transmembrane Prediction', 'Alphafold pLDDT score'])
    # select spin
    spin = st.sidebar.checkbox('Spin', value=False)
    return selected_id, style, color_prot, spin

def end():
    st.sidebar.write("Author: [Céline Marquet](https://github.com/C-Marquet)")
    st.sidebar.write("Source: [Github](https://github.com/C-Marquet/TMvisDB)")