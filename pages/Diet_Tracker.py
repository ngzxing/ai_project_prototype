import streamlit as st
import pandas as pd
import numpy as np

if "diet" not in st.session_state:

    st.warning("Please Go To Diet Planner, before go back this page")

else:
    protein = []
    carbonhydrates = []
    fat = []
    
    for day in st.session_state.diet:
        p = 0
        c = 0
        f =0
        for key in st.session_state.diet[day]:
            p = p + st.session_state.diet[day][key]["Protein"] 
            c = p + st.session_state.diet[day][key]["Carbonhydrates"] 
            f = p + st.session_state.diet[day][key]["Fat"]
    
        protein.append(p)
        carbonhydrates.append(c)
        fat.append(f)
    
    protein = np.array(protein*4)
    carbonhydrates = np.array(carbonhydrates*4)
    fat = np.array(fat*4)
    
    st.write("# Diet Tracker")
    st.error("We detect you consumed inappropriate amount of **protein** over last 28 days")
    st.error("We detect you consumed inappropriate amount of **fat** over last 28 days")
    
    def plotter(name, data):
        st.write("## "+ name + " Consumed")
        data = pd.DataFrame({ "expected" : data, "actual" :  data + 10*np.random.randn(data.shape[0])})
        st.area_chart(data)
    
    plotter("Protein", protein)
    plotter("Carbonhydrates", carbonhydrates)
    plotter("Fat", fat)


