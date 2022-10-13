
import streamlit as st

def quest():

    st.markdown("##### FAQs  \n")

    with st.expander("Why can't I find this protein I am interested in?"):
        st.markdown(
        "(1) If the protein you are looking for is not part of AFDB, f.e. due to length restrictions, it is also not included in TMvis-DB.  \n"
        "(2) The protein you are looking for might only be membrane associated, TMvis-DB only contains proteins predicted to fully span a membrane.  \n"
        "(3) While TMbed has a low false negative rate, some proteins are likely missing in the databse.  \n"
        )

    st.info("Please submit any further questions or suggestions here: [Github Issues](https://github.com/marquetce/TMvisDB/issues)")