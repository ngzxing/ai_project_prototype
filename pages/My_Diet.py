import streamlit as st
import numpy as np
import pandas as pd

if "diet" not in st.session_state:

    st.warning("Please Go To Diet Planner, before go back this page")
else:
    
    st.write("# Your Goals: ")
    st.write("Here is the goals your diet planner try to achieve in one month")
    st.write("- " + "\n- ".join(st.session_state.goals) )
    
    st.write("# Your Diet Planning")
    st.write("*repeat this 7 days routine diet in one month*")
    tabs = st.tabs( [ "###### " + key for key in st.session_state.diet.keys() ] )
    
    for tab, day in zip(tabs, st.session_state.diet):
    
        with tab:
            plan = pd.DataFrame(st.session_state.diet[day]).T
            st.table(plan)
            st.write(f"###### Total Calories of that Day: `{plan['Calories'].sum()}` ")
