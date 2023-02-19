
from urllib.request import urlopen
import requests
import re
import streamlit as st


## check if ID input format is correct
re_accessionNumber = re.compile("^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2}$")
re_uniprotID = re.compile("^[A-Z0-9]{3,20}_[A-Z0-9]{3,20}$")
def check_input_format(selected_id):
    test_str = selected_id.upper()
    if re_uniprotID.match(test_str):
        type = "uniprot_id"
    elif re_accessionNumber.match(test_str):
        type = "uniprot_acc_num"
    else:
        type = "unknown"
    return type

## Load AF structure ##
def get_af_structure(selected_id):
    # Initialize AF DB json file
    afdb_api_path = 'https://www.alphafold.ebi.ac.uk/api/prediction/' + selected_id
    afdb_json = requests.get(afdb_api_path).json()
    try:
        # get sequence
        seq = afdb_json[0]["uniprotSequence"]
        # get structure
        afdb_pdb_path = afdb_json[0]['pdbUrl']
        afdb_file = urlopen(afdb_pdb_path).read().decode('utf-8')
        system = "".join([x for x in afdb_file])
    except:
        st.warning(
            "We could not find a protein in AlphaFold DB matching your ID: " + selected_id ,
            icon="🚨")
        seq = 0
        system = 0
    return seq, system

## Load uniprot transmembrane annotation ##
def get_uniprot_tmvec(selected_id, input_type):
    # format of accession or ID must be correct for access, so not all in one statement
    if input_type == "uniprot_acc_num":
        url = f"https://rest.uniprot.org/uniprotkb/search?query=accession:{selected_id} AND active:true &fields=id,accession,length,ft_transmem&format=json&size=1"
    elif input_type == "uniprot_id":
        url= f"https://rest.uniprot.org/uniprotkb/search?query=id:{selected_id} AND active:true &fields=id,accession,length,ft_transmem&format=json&size=1"
    elif input_type == "unknown":
        url = f"https://rest.uniprot.org/uniprotkb/search?query={selected_id} AND active:true &fields=id,accession,length,ft_transmem&format=json&size=1"

    body = requests.get(url).json()

    if "results" in body:
        if len(body["results"]) == 0:
            st.warning("We could not find a protein in UniProtKB/TrEMBL matching your ID: "+  selected_id +". This could mean the ID is misspelled or the protein was deleted in a recent release of UniProtKB/TrEMBL.",
                       icon="🚨")
            up_name = selected_id
            up_acc = selected_id
            UP_TM_vec = 0
            seq_length = "unknown"

        else:
            body = body["results"][0]
            up_acc = body["primaryAccession"]
            up_name = body['uniProtkbId']
            seq_length = body['sequence']['length']
            if 'Transmembrane' in body.__str__():
                # initialize array with uniprot transmembrane annotation
                UP_TM_vec = ["*"] * (seq_length)
                # iterate over features in json file, add to vector if transmembrane
                for entry in body['features']:
                    if entry['type'] == 'Transmembrane':
                        if "Beta" in entry['description']:
                            annotation = 'BS'
                        elif "Helical" in entry['description']:
                            annotation = 'AH'
                        else:
                            annotation = 'NaN'
                        pos_start = int(entry['location']['start']['value']) - 1
                        pos_end = int(entry['location']['end']['value'])
                        UP_TM_vec[pos_start:pos_end] = [annotation] * (pos_end - pos_start)
            else:
                UP_TM_vec = 0
    else:
        st.write("Something went wrong contacting Uniprot. Please check your selected ID and/or try again later.")
        up_name = selected_id
        up_acc = selected_id
        UP_TM_vec = 0
        seq_length = "unknown"

    return up_acc, up_name, UP_TM_vec, seq_length


## Load tmalphafold transmembrane annotation ##
def get_tmalphafold(up_name, seq_length):
    url = f"https://tmalphafold.ttk.hu/api/tmdet/{up_name}.json"
    try:
        body = requests.get(url).json()
        if "CHAIN" in body:
            tmaf_tm_vec = ["*"] * (seq_length)
            for entry in body["CHAIN"][0]["REGION"]:
                if entry["_attributes"]["type"] == "M":
                    pos_start = int(entry["_attributes"]['seq_beg']) - 1
                    pos_end = int(entry["_attributes"]['seq_end'])
                    tmaf_tm_vec[pos_start:pos_end] = ["AH"] * (pos_end - pos_start)
        else:
            tmaf_tm_vec = 0
    except:
        tmaf_tm_vec = 0

    return tmaf_tm_vec
