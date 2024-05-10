# Bring in deps
import streamlit as st
from prompts import build_prompt
import google.generativeai as genai
from get_inputs import get_food_pref_inputs
from feedback import build_user_input, get_feedback

def main():
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

    st.write("Made with ❤️ by Amogh Mahadev kokari ©️ 2024 _||_ [linkedin](https://www.linkedin.com/in/amoghkokari/) _||_ [Portfolio](https://amoghkokari.github.io/portfolio.pdf) _||_ [Github](https://github.com/amoghkokari)")

    # Show stuff to the screen if there's a prompt
    try:
        if prompt_enter:
            response = model.generate_content(prompt)
            st.write(response.text)
            u_inputs = build_user_input(food, grocery, time, cusine, equipment, meal, allergies, extra)
            get_feedback(u_inputs, response.text)            

    except Exception as error:
        st.write("Please check your Api key, probable issue", SystemExit(error))

if __name__ == "__main__":
    main()