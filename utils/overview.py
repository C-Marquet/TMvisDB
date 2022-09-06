import streamlit as st

def intro():
    st.markdown(
        "**TMvisDB** provides per-residue transmembrane topology annotations for all proteins in [AlphaFold DB](http://example.com) (~ 200 million proteins) "
        "predicted as transmembrane proteins (~ 40 million). "
        "The annotations are predicted with [TMbed](http://example.com), and are visualized by overlaying them with AlphaFold 2 structures.  \n")

    st.markdown(
        "###### :bulb: How to browse TMvisDB: \n"
        "To browse the 40 million predicted transmembrane proteins in TMvisDB, you can show a random selection or use the following filters:  \n"
        "- Transmembrane topology (alpha-helix, beta-strand  \n"
        "- Include/Exclude sequences with predicted signal peptides  \n"
        "- Taxonomy (Domain, Kingdom)  \n")
    st.markdown(
        "###### :bulb: How to visualize predicted transmembrane proteins: \n"
        "Single proteins of TMvisDB can be selected for 3D-visualization of per-residue transmembrane topology annotation. "
        "You can either select a protein from the table you generated while browsing TMvisDB, or you can directly enter a UniProt Identifier. "
        "The AlphaFold 2 structures of a protein is then shown with the corresponding color code of the predicted topology. "
        "You may also select the pLDDT score of AlphaFold 2 as a color code.")