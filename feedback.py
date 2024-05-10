import streamlit as st
from firebase_admin import firestore, credentials, initialize_app, _apps

if not _apps:
    cred = credentials.Certificate(dict(st.secrets['profile']))
    initialize_app(cred)

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

def store_to_db(collection, values):
    try:
        db = firestore.client()
        # Store the feedback data in Firestore
        db.collection(collection).add(values)
        return True
    except Exception as error1:
        st.write("Please check your Api key, probable issue", SystemExit(error1))
        return False

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