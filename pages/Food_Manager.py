import streamlit as st
import numpy as np

st.write("# Food Manager")

tab1, tab2 = st.tabs(["#### Ingredients List", "#### Order List"])

with tab1:
    st.error("There are some **food expired**, kinldy check the following list")
    with st.expander("See Details"):
        st.markdown("""
        
        The list is showing the details of ingredients inside the refrigerator:

        > `ingredient` is the name of ingredient
        
        > `status` is showing whether the food is expired
        
        > `target_weight` is showing the expected ingredients amount should have in refrigerator
        
        > `weight` is the actual weight of ingredients inside the refrigerator

        > `Expired Date` is the expired date of the ingredients
        
                    """)
        
    st.table(st.session_state["ingredients"][["Ingredient", "Target Weight", "Weight", "Status", "Expired Date"]])
        

with tab2:

    def replace(i, order_status):
        st.session_state.ingredients.loc[i, "Order Status"] = order_status

    def show_container(i):
    
        if st.session_state.ingredients.loc[i, "Order Status"] == "Sufficient":
            return
            
        with st.container():
            
            columns = st.columns(3)
            columns[0].write( f":red[{st.session_state.ingredients.loc[i, 'Ingredient']}]")
            columns[0].divider()
            columns[1].write( st.session_state.ingredients.loc[i, "Order Status"])
            columns[1].divider()

            
            if st.session_state.ingredients.loc[i, "Order Status"] == "Ordering":
                
                columns[2].button(f"Cancel Order", key = f"Cancel Order{i}", 
                                  on_click = lambda : replace(i, "Not Ordering"), type = "primary", use_container_width=True )
                    
            elif st.session_state.ingredients.loc[i, "Order Status"] == "Not Ordering":
                columns[2].button(f"Order", key = f"Order{i}", 
                                  on_click = lambda : replace(i, "Ordering"), type = "secondary", use_container_width=True )


                
            

    columns = st.columns(3)
    columns[0].write("### Ingredient")
    columns[1].write("### Status")
    
    for i in range( st.session_state.ingredients.shape[0] ):    
        show_container(i)