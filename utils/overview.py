import streamlit as st

def intro():
    st.markdown(
        "**TMvisDB** provides per-residue transmembrane topology annotations for all proteins in [AlphaFold DB](https://doi.org/10.1093/nar/gkab1061) (~ 200 million proteins, September '22) "
        "predicted as transmembrane proteins (~ 46 million). "
        "The annotations are predicted with [TMbed](https://doi.org/10.1186/s12859-022-04873-x), and are visualized by overlaying them with AlphaFold 2 structures.  \n")

    st.markdown(
        "###### :bulb: How to browse TMvisDB: \n"
        "To browse the 46 million predicted transmembrane proteins in TMvisDB via a table, you can show a random selection or use the following filters:  \n"
        "- Transmembrane topology (alpha-helix, beta-strand)  \n"
        "- Include/Exclude sequences with predicted signal peptides  \n"
        "- Taxonomy (UniProt Organism Identifier, Domain, Kingdom)  \n"
        "- Protein length  \n"
        "Note: We follow followed general length restrictions of AlphaFold DB: minimum 16 amino acids and maximum 1,280 amino acids for all organisms except SwissProt (2,700 amino acids) and human (none).  \n")
    st.markdown(
        "###### :bulb: How to visualize predicted transmembrane proteins: \n"
        "Single proteins of TMvisDB can be selected for 3D-visualization of per-residue transmembrane topology annotation. "
        "You can either select a protein from the table you generated while browsing TMvisDB, or you can directly enter a UniProt Identifier. "
        "The AlphaFold 2 structures of a protein is then shown with the corresponding color code of the predicted topology. "
        "You may also select the pLDDT score of AlphaFold 2 as a color code.")
