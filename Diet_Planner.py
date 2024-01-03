import streamlit as st
import google.generativeai as genai
import re
import json
import pandas as pd
import numpy as np

class DietPlanner():

    def __init__(self):
        genai.configure(api_key = "AIzaSyAgvoJ9J3PwJZuvP6gNAid8YCQRMDf9ktU" )
        self.model = genai.GenerativeModel("gemini-pro",
                                          generation_config=genai.types.GenerationConfig(
                                              candidate_count=1,
                                              max_output_tokens=6000,
                                              temperature  = 1.0)
                                          )

    def inputting(self):

        st.write("# Diet Planner")
        self.target = st.text_input("**Tell us your target**", "I want to reduce 10 kg...")
        self.age = st.slider("**How old are you**", 3, 100, 1)
        self.weight = st.slider("**Tell us your weight(KG)**", 0.0, 200.0, 0.1)
        self.height = st.slider("**Tell us your height(CM)**", 0.0, 200.0, 0.1)
        self.preference = st.text_input("**Tell us your food preference**", "I don't like sweet")


    def generate_goals(self):

       
            
        response = self.model.generate_content(f"""You are a expert diet planner, the goal of you is to 
        generate 3 sub-goals for this a one month diet planning based on the user target and body data as simple as possible, don't too long.
    
        user targets:
        {self.target}
    
        user body data:
            age : {self.age}
            weight: {self.weight}
            height: {self.height}

        user preference:
            {self.preference}
    
        example output format:
            1. everyday decrease 100 calotries consumed
            2. eat more vegtables
            3. reduce sugar
        
        output:
        """)
    
        self.goals = re.findall( r"\d+\. (.+)", response.text, re.M)
        st.session_state["goals"] = self.goals
            

    def planning(self):


        if st.button("Generate"):
            with st.spinner('Generating...'):
    
                self.generate_goals()
    
                st.write("# Your Goals: ")
                st.write("Here is the goals your diet planner try to achieve in one month")
                st.write("- " + "\n- ".join(self.goals) )
    
                try:
                    self.__planner()
                except:
                    self.__planner()
    
                self.__show_planning()
    
                try:
                    self.__ingredients()
                except:
                    self.__ingredients()

            st.success('Done!')

            return self.diet

    def __planner(self):
        
        response = self.model.generate_content(f"""You are a expert diet planner, the goal of you is to 
            generate one week diet planning based on the user target, body data, preference and goals. 

            what your output should be:
                - Output it in json
                - include Breakfast, Lunch and Dinner and take it as key name
                - include a specific food names with key name "Food"
                - include calories with key name "Calories" 
                - include protein with key name "Protein"
                - include carbornhydrates with key name "Carbonhydrates"
                - include fat with key name "Fat"
                - The key for this json should be "Day1", "Day2" etc.

            what your output should not be:
                - include snacks
                - include specific diet ingredients
        
            user targets:
                {self.target}
        
            user body data:
                age : {self.age}
                weight: {self.weight}
                height: {self.height}
    
            user preference:
                {self.preference}
    
            goals:
                {self.goals}
        
            output:
            """)

        response = re.sub( r"(\d+)[ ]*g", r"\1", response.text.replace("json", "").replace("```","").strip() ) 

        self.diet = json.loads(response)
        st.session_state["diet"] = self.diet
        
    
    def __show_planning(self):

        st.write("# Your Diet Planning")
        st.write("*repeat this 7 days routine diet in one month*")
        tabs = st.tabs( self.diet.keys() )

        for tab, day in zip(tabs, self.diet):

            with tab:
                plan = pd.DataFrame(self.diet[day]).T
                st.dataframe(plan)
                st.write(f"Total Calories of that Day: {plan['Calories'].sum()} ")

        

    def __ingredients(self):

        foods = []
        
        for day in self.diet:
            diet = self.diet[day]
            
            for i in ["Breakfast", "Lunch", "Dinner"]:
                foods.append(diet[i]["Food"])

        response = self.model.generate_content(f"""

        You as an expert cooker, please suggest and list all the required ingredients for all the following food

        your output should be:
            - list the ingredients directly
            - seperate the ingredients with comma
            - write it in plain text instead of markdown

        your output should not be:
            - include the food name:
            - list them in number or seperate by '-'
        
        food:
        {foods}

        ingredients:
        """)

        ingredients = re.sub( r"\d+\.", "", response.text.replace("\n", ",").replace("-","")).split(",")
        ingredients = pd.DataFrame([ {"Ingredient" : ingredient, "Target Weight": np.abs(np.random.normal()) } 
                                    for ingredient in ingredients])
        
        ingredients["Weight"] =  np.random.uniform([0]*ingredients.shape[0], ingredients["Target Weight"]) 
        ingredients["Order Status"] = np.where( np.abs(ingredients["Target Weight"] - ingredients["Weight"]) > 0.1, 
                                               "Ordering", "Sufficient") 

        expired = np.random.randint(-50,200, ingredients.shape[0])
        status = np.where( expired >= 0, "good", "expired" )
        expired = expired.astype("str")
        
        
        ingredients["Expired Date"] = pd.to_datetime("today") + pd.to_timedelta( np.char.add(expired, " days") )
        ingredients["Status"] = status
        
        st.session_state["ingredients"] = ingredients
        
        return ingredients
        
        
        

planner = DietPlanner()
planner.inputting()
planner.planning()


        

        
        
