import py3Dmol
from stmol import showmol
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from utils.apis import check_input_format, get_tmalphafold, get_uniprot_tmvec, get_af_structure
from utils.coloring import color_prediction, color_code_af, color_code_pred, color_expl_af, color_expl_tmbed, tm_color_structure


## Load TMvisDB data ##
def get_data_vis(db, selected_id):
    query = {"_id": selected_id}
    data_form = {'_id': 1,
                 'sequence': 1,
                 'predictions.transmembrane': 1,
                 'annotations.tm_categorical': 1,
                 'seq_length': 1,
                 'organism_name': 1,
                 'organism_id': 1,
                 'uptaxonomy.Lineage_all': 1,
                 'uptaxonomy.Domain': 1,
                 'uptaxonomy.Kingdom': 1,
                 'topdb.TopDB_Entry':1,
                 'membranomedb.tm_seq_start':1,
                 'membranomedb.tm_seq_end':1}
    try:
        item = db.find(query, data_form)
        # TMbed prediction
        pred_vis = item[0]['predictions']['transmembrane']
        # TopDB and Membranome annotation
        drop_cols=list()
        if 'topdb' in item[0]:
            topdb = str(item[0]['topdb']['TopDB_Entry'])
            drop_cols.append('topdb.TopDB_Entry')
        else:
            topdb = 0
        if 'membranomedb' in item[0]:
            membdb = ["*"] * (int(item[0]['seq_length'])-1)
            pos_start = int(item[0]['membranomedb']['tm_seq_start']) - 1
            pos_end = int(item[0]['membranomedb']['tm_seq_end']) - 1
            membdb[pos_start:pos_end] = ['AH'] * (pos_end - pos_start + 1)
            drop_cols.extend(['membranomedb.tm_seq_start','membranomedb.tm_seq_end'])
        else:
            membdb = 0

        df_vis = pd.json_normalize(item)
        df_vis.drop(drop_cols, axis=1, inplace=True)

        if len(list(df_vis.columns)) <10:
            df_vis = df_vis[['_id', 'sequence', 'predictions.transmembrane', 'annotations.tm_categorical', 'seq_length', 'organism_name', 'organism_id']]
            df_vis.columns = ['UniProt ID', 'Sequence', 'Prediction', 'Alpha / Beta / Signal', 'Sequence length', 'Organism name', 'Organism ID']
        elif len(list(df_vis.columns)) == 10:
            df_vis = df_vis[['_id', 'sequence', 'predictions.transmembrane', 'annotations.tm_categorical', 'seq_length', 'organism_name', 'organism_id', 'uptaxonomy.Lineage_all', 'uptaxonomy.Domain', 'uptaxonomy.Kingdom' ]]
            df_vis.columns = ['UniProt ID', 'Sequence', 'Prediction', 'Alpha / Beta / Signal', 'Sequence length', 'Organism name', 'Organism ID', 'Lineage', 'Domain', 'Kingdom']
    except:
        pred_vis = 0
        df_vis = 0
        st.warning("We are having trouble finding the predicted transmembrane topology of your protein in TMvisDB. "
                   "This could mean, e.g., (1) your protein is outside the length restrictions of TMvisDB (see FAQ), (2) your protein is not predicted as a transmembrane protein, or (3) the UniProt ID is misspelled. "
                   "If an AlphaFold structure is displayed below, it is without transmembrane topology annotation.",
                   icon="🚨")

    return pred_vis, df_vis, topdb, membdb

## Visualizing 3D structure ##
def vis_window(structure, pred, color_prot, spin, style):
    view = py3Dmol.view(js='https://3dmol.org/build/3Dmol.js')
    view.addModelsAsFrames(structure)
    view.setBackgroundColor('#262730')

    # add color
    if color_prot == 'Alphafold pLDDT score' or pred == 0:
        view.setStyle({'model': -1}, {style: {'colorscheme': {'prop': 'b', 'gradient': 'roygb', 'min': 50, 'max': 90}}})
    else:
        tm_color = tm_color_structure(pred)
        view.setStyle({'model': -1}, {style: {'colorscheme': {'prop':'resi', 'map': tm_color}}})
    # add spin
    if spin:
        view.spin(True)
    else:
        view.spin(False)

    #view.addResLabels()
    view.zoomTo()
    showmol(view, height=500, width=800)


## Descriptive information and additional annotation concerning visualization ##
def annotation(pred, df, seq, color_prot, selected_id, up_tm_vec, tmaf_tm_vec, topdb, membdb):
    st.markdown("---")
    # Show Prediction if available
    if pred != 0:
        st.write('Prediction')
        st.write(len(str(topdb)))

        pred_table = pd.DataFrame(zip(list(seq), list(pred)), columns=["Sequence", "TMbed Prediction"])
        # table if no uniprot or tmalphafold
        colnames = ["UniProt Annotation", "TmAlphaFold Annotation", "TopDB Annotation", "Membranome Annotation"]
        cap = "Inside/outside annotations of TMbed are not optimized and must be interpreted with caution. The color code is described below."
        found = False
        not_found = str()
        for idx, x in enumerate([up_tm_vec, tmaf_tm_vec, topdb, membdb]):
            if x != 0 and len(pred_table) == len(list(x)):
                pred_table[colnames[idx]] = list(x)
                found = True
            else:
                not_found = not_found + colnames[idx].split(' ')[0] + ', '
        if found:
            cap = cap + " If entries are '*', there are no annotations for these residues. 'M' means transmembrane-residue, 'AH' means alpha-helix, 'BS' means beta-strand."
        if len(not_found) > 0:
            cap = " We could not find transmembrane annotation in: " + not_found[:-2] +' (Note: there may be entries with deviating sequence length). ' + cap

        pred_table = pred_table.T.style.apply(color_prediction, axis = 0)
        st.write(pred_table)
        st.caption(cap)

        # Show further sequence annotation
        st.write('Protein Annotation')

        #st.write(df.drop(columns=['Sequence','Prediction']))
        AgGrid(df.drop(columns=['Sequence','Prediction']), height=75, fit_columns_on_grid_load=True)

    # if no TMbed annotation, check other databases
    else:
        # no entry in UniProt or TmAlphaFold
        if up_tm_vec == 0 and tmaf_tm_vec == 0:
            st.caption("We could not find UniProt or TmAlphaFold transmembrane annotation for this protein.")
        # table if uniprot but no tmalphafold
        elif up_tm_vec != 0 and tmaf_tm_vec == 0:
            pred_table = pd.DataFrame(zip(list(seq), list(up_tm_vec)), columns=["Sequence", "UniProt Annotation"]).T.style.apply(color_prediction, axis = 0)
            st.write(pred_table)
            st.caption(
                "If entries in the row 'UniProt annotation' are '*', there are no annotations for these residues in UniProt. 'AH' means alpha-helix, 'BS' means beta-strand.")
            st.caption("We could not find TmAlphaFold transmembrane annotation for this protein.")
        # table if tmalphafold but no uniprot
        elif tmaf_tm_vec != 0 and up_tm_vec == 0:
            pred_table = pd.DataFrame(zip(list(seq), list(tmaf_tm_vec)), columns=["Sequence", "TmAlphaFold Annotation"]).T.style.apply(color_prediction, axis = 0)
            st.write(pred_table)
            st.caption(
                "If entries in the row 'TmAlphaFold annotation' are '*', there are no annotations for these residues in TmAlphaFold. 'AH' means alpha-helix.")
            st.caption("We could not find UniProt transmembrane annotation for this protein.")


    # Explain Colors
    st.write('Color code')
    if color_prot == 'Alphafold pLDDT score' or pred == 0:
        st.write(color_code_af.style.applymap(color_expl_af, subset=["pLDDT score"]))
    else:
        st.write(color_code_pred.style.applymap(color_expl_tmbed, subset=["Color"]))
        st.caption("Inside/outside annotations of TMbed are not optimized and must be interpreted with caution.")

    st.markdown("---")

    # Link other resources
    link_up = f'- UniProt entry: [{selected_id}](https://www.uniprot.org/uniprotkb/{selected_id}/entry)  \n'
    link_lpp = f'- Evaluate protein-specific phenotype predictions: [LambdaPP](https://embed.predictprotein.org/i/{selected_id})  \n'
    link_fs = f'- Generate structural alignments: [Foldseek](https://search.foldseek.com/search)  \n'
    link_tdb = f'- Experimentally derived topology information: [Topology Data Bank of Transmembrane Proteins](http://topdb.enzim.hu/)  \n'
    link_memb = f'- Membranome database for single-helix transmembrane proteins: [Membranome](https://membranome.org/)  \n'
    link_tmaf = f'- Alpha-helical transmembrane proteins: [TmAlphaFold database](https://tmalphafold.ttk.hu/entry/{selected_id})'

    st.markdown("Resources to evaluate your selection further:  \n")
    st.markdown(link_up + link_lpp + link_fs + link_tdb + link_memb + link_tmaf)

## Visualize from database ##
def vis(db, selected_id, style, color_prot, spin):

    input_type = check_input_format(selected_id)

    if input_type != "unknown":
        # get uniprot annotation
        up_accnum, up_name, up_tm_vec, seq_length = get_uniprot_tmvec(selected_id, input_type)

        # get data from tmvisdb
        [pred, df, topdb, membdb] = get_data_vis(db, up_accnum)

        # if helical, get TMDET from TmAlphaFold database
        if "H" or "h" in pred or pred == 0:
            tmaf_tm_vec = get_tmalphafold(up_name, seq_length)
        else:
            tmaf_tm_vec = 0

        if pred == 0 and up_tm_vec == 0 and tmaf_tm_vec == 0:
            st.warning("We also found no transmembrane annotation in UniProt or TmAlphaFold.",icon="🚨")

        # get and protein structure
        [seq, structure] = get_af_structure(up_accnum)

        if up_accnum != up_name:
            st.write("Displaying protein with UniProt accession number: ", up_accnum, " and UniProt entry name:", up_name)
        else:
            st.write("Displaying protein with ID: ", up_accnum)
        vis_window(structure, pred, color_prot, spin, style)
        st.caption("Use the visualization tab and side bar to change style and color scheme.")
        annotation(pred, df, seq, color_prot, up_accnum, up_tm_vec, tmaf_tm_vec, topdb, membdb)
    else:
        st.error("The input format of your selected ID ** "+ selected_id+ " ** is not correct.",icon="🚨")
        # get uniprot annotation
        up_accnum, up_name, up_tm_vec, seq_length = get_uniprot_tmvec(selected_id, input_type)
        #st.write("Searching UniProt, we found the following protein with accession number: ", up_accnum, " and UniProt entry name:", up_name)
        #st.write("Below are results for this protein. If this is not what you are looking for, please check UniProt for the accession number of your protein.")

        [pred, df, topdb, membdb] = get_data_vis(db, up_accnum)

        try:
            # get and protein structure
            [seq, structure] = get_af_structure(up_accnum)
            vis_window(structure, pred, color_prot, spin, style)
            st.caption("Use the visualization tab and side bar to change style and color scheme.")
            annotation(pred, df, seq, color_prot, up_accnum, up_tm_vec, tmaf_tm_vec, topdb, membdb)

        except:
            st.warning("We are having trouble finding your protein structure in AlphaFold DB. This could mean that it is not part of AlphaFold DB, or the UniProt ID is misspelled.",
                icon="🚨")

