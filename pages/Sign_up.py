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
st.image("./images/pantrypal.png")
with st.form("Login"):

    st.write("# Sign Up")
    columns = st.columns(2)
    columns[0].text_input("First name")
    columns[1].text_input("Last name")
    st.text_input("E-mail")
    st.text_input("Password", type="password")
    st.text_input("Confirm Password", type = "password")
    st.checkbox('Check this box if you agree with [our terms and policy]()')
    st.form_submit_button("Log In", use_container_width= True)
    st.markdown("[Account Exists]()")
