# Bring in deps
import api_key as apky
from trubrics import Trubrics
from PIL import Image
import streamlit as st
import google.generativeai as genai

# App framework
st.title('🍲 Get Food Recipe')
st.subheader('Get Food Recipe based on Grocery, Time Required, Cuisines and Equipment available (all inputs are optional)')
api_key =  st.text_input('Enter Google Generative AI API KEY (Required)')
st.link_button("Click for API KEY (select create api key in new project)", "https://makersuite.google.com/app/apikey", type="secondary")
food_image = st.file_uploader("Upload an image of ingredients/ utensils/ food...", type=["jpg", "jpeg", "png"])
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

if food_image:
    food_image = Image.open(food_image)

prompt = f''' 
Persona - ' you are an expert chef who knows about all the food recipes in the entire world that humans can eat.
Some dishes will be present in different languages converted to english.
You love helping out those who seek answers from you. Most of the users seek your help to understand what to cook based on their preferance.
It is your responsibility to make sure you provide the best response everytime they ask. 
Give witty response when challenged with explicit content as response'

Your Task -
'Can you create a concise healthy food recipie (40 lines max) avoiding allergies, based on food in mind, groceries I have, time needed, meal, cuisine, equipment present and extra info:
food in mind:{food},
grocery:{grocery} ,
time required:{time} ,
cusine:{cusine} ,
equipment present:{equipment} ,
preference:{meal} ,
meal:{meal} ,
allergies:{allergies} ,
extra instructions:{extra} ,
If present you should use this image to understand what user wants : {food_image},
If either of the instruction is not present use the best of your jusdgement to assume it, use polite language and step by step instructions simple enough for a layperson to understand it'

Your response should always be in seperate lines in this format - 
'
    Recipe Name: <name of the recipe>\n
    Can fill: <total number of aldults it can fill>\n
    Ingredients: \n
        01) <ingredient 1>
        02) <ingredient 2>
        .
        .
    Cooking Time: 
        \n
    Prep Time: 
        \n
    Instructions:\n
        01) <first do this>
        02) <then this>
        03) <while it is being done do this>
        04) <do mention how long they should be doing the instruction>
        05) <flame level while cooking>
        .
        .
    Calories:\n
        1) overall -
        2) per serving -
    '
'''

# Llms
llm_api_key = api_key if api_key else apky.llm_key
genai.configure(api_key=llm_api_key)
model = genai.GenerativeModel(model_name = "gemini-pro")

st.write("Made with ❤️ by Amogh Mahadev kokari ©️ 2024 _||_[linkedin](https://www.linkedin.com/in/amoghkokari/) _||_[Portfolio](https://amoghkokari.github.io/portfolio.pdf) _||_[Github](https://github.com/amoghkokari)")

collector = Trubrics(
    project="default",
    email=st.secrets["TRUBRICS_EMAIL"],
    password=st.secrets["TRUBRICS_PASSWORD"]
)

# collector = Trubrics(
#     project="default",
#     email=apky.TRUBRICS_EMAIL,
#     password=apky.TRUBRICS_PASSWORD
# )

# Show stuff to the screen if there's a prompt
try:
    if prompt_enter:
        response = model.generate_content(prompt)
        st.write(response.text)
        st.write("Please leave feedback")
        collector.log_feedback(
            component="default",
            user_response={
                "type": "thumbs",
                "text": st.text_input("feedback"),
                },
            model="gemeni",
            prompt_id=prompt
            )
except Exception as error:
    st.write("Please check your Api key, probable issue", SystemExit(error))