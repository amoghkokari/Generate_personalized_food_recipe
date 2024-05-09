# Bring in deps
import api_key as apky
from prompts import build_prompt
from PIL import Image
import streamlit as st
import google.generativeai as genai
from firebase_admin import firestore, credentials, initialize_app

# App framework
st.title('🍲 Get Food Recipe')
st.subheader('Get Food Recipe based on Grocery, Time Required, Cuisines and Equipment available (all inputs are optional)')

# get inputs
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

# start process
prompt_enter = st.button("Recipe")

if food_image:
    food_image = Image.open(food_image)

prompt = build_prompt(food, grocery, time, cusine, equipment, meal, allergies, extra, food_image)

# Llms
llm_api_key = api_key if api_key else apky.llm_key
genai.configure(api_key=llm_api_key)
model = genai.GenerativeModel(model_name = "gemini-pro")

st.write("Made with ❤️ by Amogh Mahadev kokari ©️ 2024 _||_ [linkedin](https://www.linkedin.com/in/amoghkokari/) _||_ [Portfolio](https://amoghkokari.github.io/portfolio.pdf) _||_ [Github](https://github.com/amoghkokari)")

@st.experimental_fragment
def get_feedback(prompt, resp):
    rating = st.select_slider(label="likeness", options=["😀","🙂","😐","🙁","😞"], key='rating', label_visibility='hidden')
    feedback = st.text_area(label="Feedback", placeholder=" I like the application, gave good response but I would love to see .....")

    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 5, "🙂": 4, "😐": 3, "🙁": 2, "😞": 1},
    }

    enter_feedback = st.button("Save Feedback")

    if enter_feedback:
        feedback_data = {
            "response": resp,
            "prompt": prompt,
            "feedback": feedback,
            "rating": score_mappings["faces"][rating]
        }
        store_to_db("feedback" ,feedback_data)
    
    st.write("Thank you for your valuable feedback, dont forget to follow on [Github](https://github.com/amoghkokari) !!")

    return

def store_to_db(collection, values):
    try:
        cred = credentials.Certificate("eatoff-cdef5-firebase-adminsdk-xdsbj-95581ba566.json")
        initialize_app(cred)
        db = firestore.client()
        # Store the feedback data in Firestore
        db.collection(collection).add(values)
        return True
    except Exception as error1:
        st.write("Please check your Api key, probable issue", SystemExit(error1))
        return False

# Show stuff to the screen if there's a prompt
try:
    if prompt_enter:
        response = model.generate_content(prompt)
        st.write(response.text)
        get_feedback(prompt, response.text)            

except Exception as error:
    st.write("Please check your Api key, probable issue", SystemExit(error))