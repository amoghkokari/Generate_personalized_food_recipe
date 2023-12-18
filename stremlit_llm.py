# Bring in deps
from api_key import llm_key
from trubrics.integrations.streamlit import FeedbackCollector

import streamlit as st
import google.generativeai as genai

# App framework
st.title('🍲 Get Food Recipe')
st.subheader('Get Food Recipe based on Grocery, Time Required, Cuisines and Equipment available (all inputs are optional)')
api_key =  st.text_input('Enter Google Generative AI API KEY (Required)')
st.link_button("Click for API KEY (select create api key in new project)", "https://makersuite.google.com/app/apikey", type="secondary")
food = st.text_input('Particular Food in Mind (Dal Tadka, cake)')
grocery = st.text_input('Grocery (onion, garam masala)')
time = st.text_input('Cooking Time (1 hr, 30 mins)')
cusine = st.text_input('Cuisine (Italian, South-Indian)')
equipment = st.text_input('Equipment used (frying pan, spatula)')
meal = st.text_input('Meal (breakfast, brunch)')
preference = st.text_input('Preference (vegan, no meat)')
allergies = st.text_input('Allergies')
extra = st.text_input('Additional information/requests')

# Prompt templates
prompt_enter = st.button("Recipe") 

prompt = f''' Can you create a concise healthy food recipie (40 lines max) avoiding allergies, based on food in mind, groceries I have, time needed, meal, cuisine, equipment present and extra info:
food in mind:{food},
grocery:{grocery} ,
time required:{time} ,
cusine:{cusine} ,
equipment present:{equipment} ,
preference:{meal} ,
meal:{meal} ,
allergies:{allergies} ,
extra instructions:{extra} ,
If either of the instruction is not present use the best of your jusdgement to assume it, use polite language and step by step instructions simple enough for a layperson to understand it
use the following format in seperate lines
    Recipe Name:<name of the recipe>
    Ingredients:
        <ingredient 1>
        <ingredient 2>
        .
        .
    Cooking Time:
        \n
    Prep Time:
        \n
    Instructions:
        <first do this>
        <then this>
        <while it is being done do this>
        <do mention how long they should be doing the instruction>
        <flame level while cooking>
        .
        .
'''

# Llms
llm_api_key = api_key if api_key else llm_key
genai.configure(api_key=llm_api_key)
model = genai.GenerativeModel(model_name = "gemini-pro")

st.write("Made with ❤️ by [Amogh Mahadev kokari](https://padlet.com/amoghkokari/my-portfolio-pmedtgib3l3qk1ma/wish/2605601586) ©️ 2024 _||_[linkedin](https://www.linkedin.com/in/amoghkokari/) _||_[Portfolio](https://padlet.com/amoghkokari/my-portfolio-pmedtgib3l3qk1ma) _||_[Github](https://github.com/amoghkokari)")

collector = FeedbackCollector(
    project="food recipe",
    email=st.secrets["TRUBRICS_EMAIL"],
    password=st.secrets["TRUBRICS_PASSWORD"],
)

# Show stuff to the screen if there's a prompt
try:
    if prompt_enter:
        response = model.generate_content(prompt)
        st.write(response.text)
        collector.st_feedback(
            component="food recipe",
            feedback_type="thumbs",
            open_feedback_label="[Optional] Provide additional feedback",
            model="gemeni",
            prompt_id=prompt,)
        st.write("Please leave feedback")
except Exception as error:
    st.write("Please check your Api key, probable issue", SystemExit(error))
