import streamlit as st

def references():
    st.markdown("##### References  \n"
                "- Preprint for TMvis-DB: [TMvis-DB](https://www.biorxiv.org/)  \n"
                "- Structure predictions: [Alphafold DB](https://alphafold.ebi.ac.uk)  \n"
                "- Transmembrane topology predictions: [TMbed](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-022-04873-x)  \n"
                "- Visualization: [TMvis](https://github.com/Rostlab/TMvis)  \n"
                "- Protein-specific phenotype predictions: [LambdaPP](https://embed.predictprotein.org)  \n"
                "- Structural aligments: [Foldseek](https://search.foldseek.com/search)")


def software():
    st.markdown("##### Software   \n"
                "- Website: [Streamlit](https://streamlit.io), [pandas](https://pandas.pydata.org)   \n"
                "- Database: [MongoDB](https://www.mongodb.com), [pymongo](https://github.com/mongodb/mongo-python-driver)  \n"
                "- 3D Visualization: [py3Dmol](https://3dmol.csb.pitt.edu), [stmol](https://github.com/napoles-uach/stmol)")

def author():
    st.markdown("##### Development & Maintenance   \n"
                "- Author: [Céline Marquet](https://github.com/C-Marquet)  \n"
                "- Code Source: [Github](https://github.com/marquetce/TMvisDB)  \n"
                "- License: [License](https://license.com/)  \n"
                "- Resources & Maintenance: [Rostlab](https://rostlab.org)")

def impr():
    st.markdown("---")
    st.markdown("<small>The following information (Impressum) is required under German law:<small>  \n"
                
                "<sub>Adress:</sub>  \n"
                "> <small>I12 - Department for Bioinformatics and Computational Biology</small>  \n"
                "> <small>School of Computation, Information and Technology</small>  \n"
                "> <small>Boltzmannstraße 3</small>  \n"
                "> <small>85748 Garching</small>  \n"
                "> <small>Germany</small>  \n"
                
                "<small>Authorized representative:</small>  \n"
                "> <small>Technical University of Munich is a statutory body under public law (Art. 11 Abs. 1 BayHSchG). It is legally represented by the President, Prof. Dr. Thomas F. Hofmann.</small>  \n"
                
                "<small>Supervisory Authority: </small>  \n"
                "> <small>Bavarian State Ministry of Science and the Arts (Bayerisches Staatsministerium für Wissenschaft und Kunst)</small>  \n"
                
                "<small>VAT ID: </small>  \n"
                "> <small>DE811193231 (§27a UStG)</small>  \n"
                
                "<small>Responsible for Content:  </small>  \n"
                "> <small>Prof. Dr. Burkhard Rost</small>  \n"
                "> <small>Boltzmannstraße 3</small>  \n"
                "> <small>85748 Garching</small>  \n"
                "> <small>assistant. (at) .rostlab.org</small>  \n" 
                "> <small>Tel: +49 (89) 289-17811</small>  \n"
                "> <small>Fax: +49 (89) 289-19414</small>  \n"
                
                "<small>Implementation: </small>  \n"
                "> <small>TMvis-DB was implemented by Rostlab using the resources named above. Technical details, assistance, and open issues can be found on [Github](https://github.com/marquetce/TMvisDB)</small>  \n"

                "<small>Legal disclaimer: </small>  \n"
                "> <small> In spite of regularily monitoring the linked resources with great care, we do not accept any responsibility for the content of external links. The operators of these websites are solely responsible for their content. </small>  \n", unsafe_allow_html=True)

