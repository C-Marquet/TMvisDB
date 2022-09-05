import pandas as pd


def get_random(db, selected_limit):
    data_form = {"tmvis_id": 1,
                 "topology_flags": 1,
                 "organism.lineage": 1,
                 "_id": 0}

    items = db.chunk0.aggregate([{ "$sample" : { "size": selected_limit }}, { "$project" : data_form}])

    df = pd.json_normalize(items)
    df['Domain'] = df['organism.lineage'].str[0]
    df['Kingdom'] = df['organism.lineage'].str[1]
    df = df[['tmvis_id', 'topology_flags', 'Domain', 'Kingdom', 'organism.lineage']]
    df.columns = ['UniProt ID', 'Predicted: Alpha / Beta / Signal', 'Domain', 'Kingdom', 'Organism']

    return df


def query(selected_domain, selected_kingdom, selected_type, selected_sp):
    sp = int(selected_sp)

    selection = dict()
    # add topology filter if selected_type not "All"
    if 'Both' in selected_type:
        selection["topology_flags"] = [1, 1, sp]
    elif 'Alpha-helix' in selected_type:
        selection["topology_flags"] = [1, 0, sp]
    elif 'Beta-barrel' in selected_type:
        selection["topology_flags"] = [0, 1, sp]

    # add filter for domain and kingdom
    if 'All' not in selected_kingdom:
        selection["organism.lineage.1"] = selected_kingdom

    if 'All' not in selected_domain:
        selection["organism.lineage.0"] = selected_domain

    return selection


def get_data_tbl(db, query, selected_limit):
    data_form = {"tmvis_id": 1,
                 "topology_flags": 1,
                 "organism.lineage": 1,
                 "_id": 0}

    items = db.chunk0.find(query, data_form).limit(selected_limit)

    df = pd.json_normalize(items)
    df['Domain'] = df['organism.lineage'].str[0]
    df['Kingdom'] = df['organism.lineage'].str[1]
    df = df[['tmvis_id', 'topology_flags', 'Domain', 'Kingdom', 'organism.lineage']]
    df.columns = ['UniProt ID', 'Predicted: Alpha / Beta / Signal', 'Domain', 'Kingdom', 'Organism']

    return df

