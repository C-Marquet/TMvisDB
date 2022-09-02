import streamlit as st
import pymongo
import pandas as pd

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient("mongodb://localhost:27017/")

client = init_connection()


# FILTER OPTIONS
type_list = ['Alpha-helix', 'Beta-barrel']
domain_list = ['Bacteria','Eukaryota','Archaea', 'unclassified sequences']
kingdom_list = ['Bacteroidetes', 'Viridiplantae', 'Gemmatimonadetes', 'Thaumarchaeota', 'Proteobacteria', 'Cyanobacteria', 'Actinobacteria', 'Metazoa', 'Rhodophyta', 'environmental samples', 'Firmicutes', 'Fungi', 'Sar', 'metagenomes', 'Planctomycetes', 'Fusobacteria', 'Aquificae', 'Candidatus Saccharibacteria', 'Verrucomicrobia', 'Candidatus Woesebacteria', 'Euryarchaeota', 'Discoba', 'Synergistetes', 'Glaucocystophyceae', 'Cryptophyceae', 'Acidobacteria', 'Tenericutes', 'Fibrobacteres', 'Chlamydiae', 'Deinococcus-Thermus', 'Crenarchaeota', 'unclassified Parcubacteria group', 'Spirochaetes', 'Candidatus Thermoplasmatota', 'Asgard group', 'Chloroflexi', 'Candidatus Gottesmanbacteria', 'Candidatus Moranbacteria', 'Metamonada', 'Candidatus Bipolaricaulota', 'Elusimicrobia', 'Candidatus Stahlbacteria', 'Amoebozoa', 'Haptista', 'Candidatus Poribacteria', 'unclassified candidate division Zixibacteria', 'candidate division GN15', 'Candidatus Aminicenantes', 'Candidatus Rokubacteria', 'Candidatus Giovannonibacteria', 'candidate division WS2', 'Calditrichaeota', 'Thermotogae', 'Nitrospirae', 'Candidatus Marinimicrobia', 'Candidatus Dojkabacteria', 'Candidatus Peregrinibacteria', 'Candidatus Roizmanbacteria', 'candidate division TA06', 'Chlorobi', 'Candidatus Gracilibacteria', 'Candidatus Bathyarchaeota', 'Candidatus Altiarchaeota', 'Candidatus Latescibacteria', 'Lentisphaerae', 'Candidatus Parcubacteria', 'Candidatus Aerophobetes', 'Candidatus Dadabacteria', 'Atribacterota', 'Armatimonadetes', 'candidate division WWE3', 'Candidatus Microgenomates', 'Candidatus Falkowbacteria', 'Candidatus Edwardsbacteria', 'Candidatus Cloacimonetes', 'Candidatus Omnitrophica', 'candidate division KSB1', 'Ignavibacteriae', 'Candidatus Collierbacteria', 'Candidatus Micrarchaeota', 'Candidatus Hydrogenedentes', 'Candidatus Dependentiae', 'Candidatus Kaiserbacteria', 'Candidatus Vecturithrix', 'Candidatus Berkelbacteria', 'Candidatus Fermentibacteria', 'Candidatus Woesearchaeota', 'candidate division WOR-3', 'Balneolaeota', 'Candidatus Magasanikbacteria', 'Candidatus Wolfebacteria', 'Nitrospinae/Tectomicrobia group', 'Chrysiogenetes', 'Candidatus Shapirobacteria', 'Coprothermobacterota', 'Candidatus Pacearchaeota', 'Candidatus Margulisbacteria', 'Candidatus Amesbacteria', 'candidate division CPR1', 'Candidatus Delongbacteria', 'candidate division CPR2', 'Candidatus Korarchaeota', 'candidate division NC10', 'Candidatus Uhrbacteria', 'candidate division Kazan-3B-28', 'Deferribacteres', 'Candidatus Yanofskybacteria', 'Candidatus Eisenbacteria', 'Candidatus Daviesbacteria', 'Candidatus Nomurabacteria', 'Nanoarchaeota', 'Candidatus Kuenenbacteria', 'Candidatus Coatesbacteria', 'Candidatus Adlerbacteria', 'Candidatus Schekmanbacteria', 'Candidatus Levybacteria', 'Candidatus Aenigmarchaeota', 'Dictyoglomi', 'Candidatus Nealsonbacteria', 'Candidatus Melainabacteria', 'Thermodesulfobacteria', 'Candidatus Curtissbacteria', 'Candidatus Saganbacteria', 'Candidatus Beckwithbacteria', 'Candidatus Sumerlaeota', 'Candidatus Handelsmanbacteria', 'Candidatus Huberarchaea', 'Candidatus Azambacteria', 'Candidatus Desantisbacteria', 'Candidatus Dormibacteraeota', 'Candidatus Undinarchaeota', 'Candidatus Diapherotrites', 'Microgenomates group incertae sedis', 'Candidatus Hydrothermarchaeota', 'Candidatus Parvarchaeota', 'Candidatus Pacebacteria', 'Candidatus Jorgensenbacteria']

### Sidebar
st.sidebar.title("TMvis")
# select Proteome
#selected_org = st.sidebar.selectbox('Filter by organism', organism_list)
# select TMP type
st.sidebar.subheader('Select by Transmembrane Topology')
selected_type = st.sidebar.multiselect('Transmembrane topology ', type_list)
selected_sp = st.sidebar.checkbox('Include sequences with signal peptides', value=0)
# select Taxonomy
st.sidebar.subheader('Select by Taxonomy')
selected_domain = st.sidebar.selectbox('Domain', domain_list)
selected_kingdom = st.sidebar.selectbox('Kingdom', kingdom_list)
# select style
#style = st.sidebar.selectbox('Style', ['Cartoon','Line','Cross','Stick','Sphere','Clicksphere']).lower()
# select color
#color_prot = st.sidebar.selectbox('Color Scheme', ['Transmembrane Prediction', 'Alphafold pLDDT score'])
# select spin
#spin = st.sidebar.checkbox('Spin', value = False)

load = st.button('Load selected data')
if load:
    # summarize filter
    if 'Alpha-helix' in selected_type:
        ah_flag = 1
    else:
        ah_flag = 0
    if 'Beta-barrel' in selected_type:
        bb_flag = 1
    else:
        bb_flag = 0
    if selected_sp:
        sp_flag = 1
    else:
        sp_flag = 0

    # Pull data from the collection.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    #@st.experimental_memo(ttl=6000)
    def get_data():
        db = client.tmvis
        items = db.chunk0.find({"topology_flags.0": ah_flag, "topology_flags.1": bb_flag, "topology_flags.2": sp_flag},
                               {"tmvis_id": 1,
                                "topology_flags": 1,
                                #"uniprot_id": 1,
                                "organism.lineage": 1,
                                #"organism.lineage.1": 1,
                                #"organism.scientificName": 1,
                                "_id": 0
                                }).limit(50)
        df = pd.json_normalize(items)
        df['Domain'] = df['organism.lineage'].str[0]
        df['Kingdom'] = df['organism.lineage'].str[1]
        df = df[['tmvis_id', 'topology_flags', 'Domain', 'Kingdom', 'organism.lineage']]
        df.columns = ['Uniprot ID', 'Predicted: Alpha / Beta / Signal', 'Domain', 'Kingdom', 'Organism']

        #items = pd.DataFrame(items)  # make hashable for st.experimental_memo
        #items.columns = ['Uniprot ID', 'Predicted: Alpha / Beta / Signal', 'Domain', 'Kingdom', 'Organism']
        return df

    df = get_data()

    # Print results.
    st.write(df)

    #st.write(top_flags)
