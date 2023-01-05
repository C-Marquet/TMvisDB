
import streamlit as st

def quest():

    st.markdown("##### FAQs  \n")

    with st.expander("Why can't I find this protein I am interested in?"):
        st.markdown(
        "(1) If the protein you are looking for is not part of AlphaFold DB, it is also not included in TMvisDB. For example, viral proteins are not included, and we follow followed general length restrictions of AlphaFold DB: minimum 16 amino acids and maximum 1,280 amino acids for all organisms except SwissProt (2,700 amino acids) and human (none).  \n"
        "(2) The protein you are looking for might be membrane associated. TMvisDB only contains proteins predicted to fully span a membrane.  \n"
        "(3) While TMbed has a low false negative rate, some proteins are likely missing from the database.  \n"
        )

    st.info("Please submit any further questions or suggestions here: [Github Issues](https://github.com/marquetce/TMvisDB/issues)")
