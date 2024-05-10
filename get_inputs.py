import streamlit as st
from PIL import Image

def get_food_pref_inputs():
    # get inputs
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

    if food_image:
        food_image = Image.open(food_image)
    
    prompt_enter = st.button("Recipe")
    
    return food, grocery, time, cusine, equipment, meal, allergies, extra, food_image, prompt_enter