import streamlit as st

st.markdown(
    """
    <style>
       
        div[data-testid="column"]:nth-of-type(2)
        {
            
            text-align: end;
        } 

        div [data-testid=stImage]
        {
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            object-position: left top;
            
        }
    </style>
    """,unsafe_allow_html=True
)
st.image("./images/pantrypal.png",width = 500)
with st.form("Login"):

    st.write("# Login")
    st.text_input("Username")
    st.text_input("Password", type="password")
    columns = st.columns(2)
    columns[0].markdown("[Forget Password]()")
    columns[1].markdown("[Sign Up]()")
    st.form_submit_button("Log In")
