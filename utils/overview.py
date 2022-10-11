import streamlit as st

def intro():
    st.markdown(
        "**TMvis-DB** provides per-residue transmembrane topology annotations for all proteins in [AlphaFold DB](http://example.com) (~ 200 million proteins) "
        "predicted as transmembrane proteins (~ 46 million). "
        "The annotations are predicted with [TMbed](http://example.com), and are visualized by overlaying them with AlphaFold 2 structures.  \n")

    st.markdown(
        "###### :bulb: How to browse TMvis-DB: \n"
        "To browse the 46 million predicted transmembrane proteins in TMvis-DB via a table, you can show a random selection or use the following filters:  \n"
        "- Transmembrane topology (alpha-helix, beta-strand)  \n"
        "- Include/Exclude sequences with predicted signal peptides  \n"
        "- Taxonomy (UniProt Organism Identifier, Domain, Kingdom)  \n"
        "- Protein length  \n")
    st.markdown(
        "###### :bulb: How to visualize predicted transmembrane proteins: \n"
        "Single proteins of TMvis-DB can be selected for 3D-visualization of per-residue transmembrane topology annotation. "
        "You can either select a protein from the table you generated while browsing TMvis-DB, or you can directly enter a UniProt Identifier. "
        "The AlphaFold 2 structures of a protein is then shown with the corresponding color code of the predicted topology. "
        "You may also select the pLDDT score of AlphaFold 2 as a color code.")
