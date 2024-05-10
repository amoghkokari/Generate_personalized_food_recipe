# Bring in deps
import streamlit as st
from prompts import build_prompt
import google.generativeai as genai
from get_inputs import get_food_pref_inputs
from firebase_admin import firestore, credentials, initialize_app, _apps

@st.experimental_fragment
def get_feedback(user_inputs, resp):
    rating = st.select_slider(label="likeness", options=["😞","🙁","😐","🙂","😀"], key='rating', label_visibility='hidden')
    feedback = st.text_area(label="Feedback", placeholder=" I like the application, gave good response but I would love to see .....")

    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 5, "🙂": 4, "😐": 3, "🙁": 2, "😞": 1},
    }

    enter_feedback = st.button("Save Feedback")

    if enter_feedback:
        feedback_data = {
            "response": resp,
            "prompt_inputs": user_inputs,
            "feedback": feedback,
            "rating": score_mappings["faces"][rating]
        }
        store_to_db("feedback" ,feedback_data)
    
        st.write("Thank you for your valuable feedback, dont forget to follow on [Github](https://github.com/amoghkokari) !!")

    return

def store_to_db(collection, values):
    try:
        db = firestore.client()
        # Store the feedback data in Firestore
        db.collection(collection).add(values)
        return True
    except Exception as error1:
        st.write("Please check your Api key, probable issue", SystemExit(error1))
        return False

def build_user_input(food, grocery, time, cusine, equipment, meal, allergies, extra):
    dct_inputs = {
        "food" : food, 
        "grocery" : grocery, 
        "time" : time, 
        "cusine" : cusine, 
        "equipment" : equipment, 
        "meal" : meal, 
        "allergies" : allergies, 
        "extra" : extra
    }
    return dct_inputs

def main():

    cred = credentials.Certificate(dict(st.secrets['profile']))

    if not _apps:
        initialize_app(cred)

    # App framework
    st.title('🍲 Get Food Recipe')
    st.subheader('Get Food Recipe based on Grocery, Time Required, Cuisines and Equipment available (all inputs are optional)')

    api_key =  st.text_input('Enter Google Generative AI API KEY (Required)')
    st.link_button("Click for API KEY (select create api key in new project)", "https://makersuite.google.com/app/apikey", type="secondary")

    food, grocery, time, cusine, equipment, meal, allergies, extra, food_image, prompt_enter = get_food_pref_inputs()
    prompt = build_prompt(food, grocery, time, cusine, equipment, meal, allergies, extra, food_image)

    # Llms
    llm_api_key = api_key if api_key else st.secrets["api_key"]
    genai.configure(api_key=llm_api_key)
    model = genai.GenerativeModel(model_name = "gemini-pro")

    u_inputs = build_user_input(food, grocery, time, cusine, equipment, meal, allergies, extra)

    st.write("Made with ❤️ by Amogh Mahadev kokari ©️ 2024 _||_ [linkedin](https://www.linkedin.com/in/amoghkokari/) _||_ [Portfolio](https://amoghkokari.github.io/portfolio.pdf) _||_ [Github](https://github.com/amoghkokari)")

    # Show stuff to the screen if there's a prompt
    try:
        if prompt_enter:
            response = model.generate_content(prompt)
            st.write(response.text)
            get_feedback(u_inputs, response.text)            

    except Exception as error:
        st.write("Please check your Api key, probable issue", SystemExit(error))

if __name__ == "__main__":
    main()