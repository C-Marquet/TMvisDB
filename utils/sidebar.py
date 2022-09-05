
import streamlit as st
sb = st.sidebar
from PIL import Image

####################################################################
# Options: Filter
type_list = ['All', 'Both','Alpha-helix', 'Beta-barrel']
domain_list = ['All', 'Bacteria', 'Eukaryota', 'Archaea', 'unclassified sequences']
kingdom_list = ['All', 'Bacteroidetes', 'Viridiplantae', 'Gemmatimonadetes', 'Thaumarchaeota', 'Proteobacteria', 'Cyanobacteria', 'Actinobacteria', 'Metazoa', 'Rhodophyta', 'environmental samples', 'Firmicutes', 'Fungi', 'Sar', 'metagenomes', 'Planctomycetes', 'Fusobacteria', 'Aquificae', 'Candidatus Saccharibacteria', 'Verrucomicrobia', 'Candidatus Woesebacteria', 'Euryarchaeota', 'Discoba', 'Synergistetes', 'Glaucocystophyceae', 'Cryptophyceae', 'Acidobacteria', 'Tenericutes', 'Fibrobacteres', 'Chlamydiae', 'Deinococcus-Thermus', 'Crenarchaeota', 'unclassified Parcubacteria group', 'Spirochaetes', 'Candidatus Thermoplasmatota', 'Asgard group', 'Chloroflexi', 'Candidatus Gottesmanbacteria', 'Candidatus Moranbacteria', 'Metamonada', 'Candidatus Bipolaricaulota', 'Elusimicrobia', 'Candidatus Stahlbacteria', 'Amoebozoa', 'Haptista', 'Candidatus Poribacteria', 'unclassified candidate division Zixibacteria', 'candidate division GN15', 'Candidatus Aminicenantes', 'Candidatus Rokubacteria', 'Candidatus Giovannonibacteria', 'candidate division WS2', 'Calditrichaeota', 'Thermotogae', 'Nitrospirae', 'Candidatus Marinimicrobia', 'Candidatus Dojkabacteria', 'Candidatus Peregrinibacteria', 'Candidatus Roizmanbacteria', 'candidate division TA06', 'Chlorobi', 'Candidatus Gracilibacteria', 'Candidatus Bathyarchaeota', 'Candidatus Altiarchaeota', 'Candidatus Latescibacteria', 'Lentisphaerae', 'Candidatus Parcubacteria', 'Candidatus Aerophobetes', 'Candidatus Dadabacteria', 'Atribacterota', 'Armatimonadetes', 'candidate division WWE3', 'Candidatus Microgenomates', 'Candidatus Falkowbacteria', 'Candidatus Edwardsbacteria', 'Candidatus Cloacimonetes', 'Candidatus Omnitrophica', 'candidate division KSB1', 'Ignavibacteriae', 'Candidatus Collierbacteria', 'Candidatus Micrarchaeota', 'Candidatus Hydrogenedentes', 'Candidatus Dependentiae', 'Candidatus Kaiserbacteria', 'Candidatus Vecturithrix', 'Candidatus Berkelbacteria', 'Candidatus Fermentibacteria', 'Candidatus Woesearchaeota', 'candidate division WOR-3', 'Balneolaeota', 'Candidatus Magasanikbacteria', 'Candidatus Wolfebacteria', 'Nitrospinae/Tectomicrobia group', 'Chrysiogenetes', 'Candidatus Shapirobacteria', 'Coprothermobacterota', 'Candidatus Pacearchaeota', 'Candidatus Margulisbacteria', 'Candidatus Amesbacteria', 'candidate division CPR1', 'Candidatus Delongbacteria', 'candidate division CPR2', 'Candidatus Korarchaeota', 'candidate division NC10', 'Candidatus Uhrbacteria', 'candidate division Kazan-3B-28', 'Deferribacteres', 'Candidatus Yanofskybacteria', 'Candidatus Eisenbacteria', 'Candidatus Daviesbacteria', 'Candidatus Nomurabacteria', 'Nanoarchaeota', 'Candidatus Kuenenbacteria', 'Candidatus Coatesbacteria', 'Candidatus Adlerbacteria', 'Candidatus Schekmanbacteria', 'Candidatus Levybacteria', 'Candidatus Aenigmarchaeota', 'Dictyoglomi', 'Candidatus Nealsonbacteria', 'Candidatus Melainabacteria', 'Thermodesulfobacteria', 'Candidatus Curtissbacteria', 'Candidatus Saganbacteria', 'Candidatus Beckwithbacteria', 'Candidatus Sumerlaeota', 'Candidatus Handelsmanbacteria', 'Candidatus Huberarchaea', 'Candidatus Azambacteria', 'Candidatus Desantisbacteria', 'Candidatus Dormibacteraeota', 'Candidatus Undinarchaeota', 'Candidatus Diapherotrites', 'Microgenomates group incertae sedis', 'Candidatus Hydrothermarchaeota', 'Candidatus Parvarchaeota', 'Candidatus Pacebacteria', 'Candidatus Jorgensenbacteria']

####################################################################
# Header Image
image = Image.open('img.png')

####################################################################
# Introduction
def intro():
    col1, col2 = sb.columns(2, gap='small')
    col1.text("\n")
    col1.title("TMvisDB")
    col2.image(image, width=100)
    sb.info("Welcome to TMvisDB:  \n"   # note: for newline add two whitespaces before \n
            "A database to search and visualize predicted transmembrane proteins.")
    with sb.expander("Overview TMvisDB"):     # note: when using expander make sure to drop "sidebar"
        st.markdown("**TMvisDB** provides per-residue transmembrane topology annotations for all proteins in [AlphaFold DB](http://example.com) (~ 200 million proteins) "
                    "predicted as transmembrane proteins (~ 40 million). "
                    "The annotations are predicted with [TMbed](http://example.com), and are visualized by overlaying them with AlphaFold 2 structures.")
    with sb.expander("How to browse TMvisDB."):
        st.markdown("To browse the 40 million predicted transmembrane proteins in TMvisDB, you can show a random selection or use the following filters:  \n"
                    "- Transmembrane topology (alpha-helix, beta-strand  \n"
                    "- Include/Exclude sequences with predicted signal peptides  \n"
                    "- Taxonomy (Domain, Kingdom)")
    with sb.expander("How to visualize predicted transmembrane proteins."):
        st.markdown("Single proteins of TMvisDB can be selected for 3D-visualization of per-residue transmembrane topology annotation. "
                    "You can either select a protein from the table you generated while browsing TMvisDB, or you can directly enter a UniProt Identifier. "
                    "The AlphaFold 2 structures of a protein is then shown with the corresponding color code of the predicted topology. "
                    "You may also select the pLDDT score of AlphaFold 2 as a color code.")


def filters():
    sb.markdown("---")
    sb.subheader("Search TMvisDB")
    select_random = sb.checkbox('Show random subset', value=1,
                                help="By default, a random subset of TMvisDB is shown. To apply the filters below, uncheck this box.")
    with sb.expander("Access filters for TMvisDB."):
        # select TMP type
        selected_type = st.selectbox('Filter by Transmembrane Topology ', type_list, help="TMbed predicts per-residue transmembrane topology as either alpha-helical or beta-stand.")
        selected_sp = st.checkbox('Include sequences with signal peptides', value=0, help="TMbed also predicts whether a sequence contains signal peptides.")
        # select Taxonomy
        selected_domain = st.multiselect('Filter by Taxonomy: Domain', domain_list, default='All', help="Select a domain.")
        selected_kingdom = st.multiselect('Filter by Taxonomy: Kingdom', kingdom_list, default='All', help="Select a kingdom.")
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
        style = st.selectbox('Style', ['Cartoon', 'Line', 'Cross', 'Stick', 'Sphere', 'Clicksphere']).lower()
        # select color
        color_prot = st.selectbox('Color Scheme', ['Transmembrane Prediction', 'Alphafold pLDDT score'])
        # select spin
        spin = st.checkbox('Spin', value=False)
    return selected_id, style, color_prot, spin

def end():
    sb.markdown("---")
    st.sidebar.write("Author: [Céline Marquet](https://github.com/C-Marquet)")
    st.sidebar.write("Source: [Github](https://github.com/C-Marquet/TMvisDB)")