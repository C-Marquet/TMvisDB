import pandas as pd
import streamlit as st
import pymongo

def get_random(db, selected_limit):
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

    items = db.aggregate([{ "$sample" : { "size": selected_limit }}, { "$project" : data_form}])
    df = pd.json_normalize(items)
    df = df[['_id', 'sequence', 'predictions.transmembrane', 'annotations.tm_categorical', 'seq_length', 'organism_name', 'organism_id', 'uptaxonomy.Lineage_all', 'uptaxonomy.Domain', 'uptaxonomy.Kingdom' ]]
    df.columns = ['UniProt ID', 'Sequence', 'Prediction', 'Alpha / Beta / Signal', 'Sequence length', 'Organism name', 'Organism ID', 'Lineage', 'Domain', 'Kingdom']

    return df


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


def query(selected_organismid, selected_domain, selected_kingdom, selected_type, selected_sp):
    sp = int(selected_sp)

    selection = dict()
    # add topology filter if selected_type not "All"
    if 'Both' in selected_type:
        selection["annotations.tm_categorical"] = [1, 1, sp]
    elif 'Alpha-helix' in selected_type:
        selection["annotations.tm_categorical"] = [1, 0, sp]
    elif 'Beta-strand' in selected_type:
        selection["annotations.tm_categorical"] = [0, 1, sp]

    if selected_organismid != '' and selected_organismid != '0':
        selection["organism_id"] = int(selected_organismid)

    # add filter for domain and kingdom
    if 'All' not in selected_domain:
        selection["uptaxonomy.Domain"] = selected_domain

    if 'All' not in selected_kingdom:
        selection["uptaxonomy.Kingdom"] = selected_kingdom

    return selection


def get_data_tbl(db, query, selected_limit):
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

    items = db.find(query, data_form).limit(selected_limit)

    df = pd.json_normalize(items)
    if len(df.T) == 10:
        df = df[['_id', 'sequence', 'predictions.transmembrane', 'annotations.tm_categorical', 'seq_length', 'organism_name', 'organism_id', 'uptaxonomy.Lineage_all', 'uptaxonomy.Domain', 'uptaxonomy.Kingdom' ]]
        df.columns = ['UniProt ID', 'Sequence', 'Prediction', 'Alpha / Beta / Signal', 'Sequence length', 'Organism name', 'Organism ID', 'Lineage', 'Domain', 'Kingdom']
    else:
        df = df[['_id', 'sequence', 'predictions.transmembrane', 'annotations.tm_categorical', 'seq_length', 'organism_name', 'organism_id']]
        df.columns = ['UniProt ID', 'Sequence', 'Prediction', 'Alpha / Beta / Signal', 'Sequence length', 'Organism name', 'Organism ID']
        df = df.reindex(columns=['UniProt ID', 'Sequence', 'Prediction', 'Alpha / Beta / Signal', 'Sequence length', 'Organism name', 'Organism ID', 'Lineage', 'Domain', 'Kingdom'])

    return df

