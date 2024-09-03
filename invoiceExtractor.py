from dotenv import load_dotenv
load_dotenv() ## To import the environment variables

import streamlit as st
import google.generativeai as genai ## main library to access gemini models
import os
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) ## To use the API key and establish acess to the Google Gemini studio

##Code for selecting the LLM Model
model = genai.GenerativeModel("gemini-pro-vision") ##Variable storing the model to be used

##Function for the response to-from Gemini
def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt]) ## input --> context , image, prompt --> query from user
    return response.text

##Function for converting the image into bytes
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue() ## Read the file into bytes
        image_parts = [
            {
                "mime_type": uploaded_file.type, ## Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


##Streamlit UI Code
st.set_page_config(page_title="Shikhar's Multi-Language Invoice Extractor")

st.header("Shikhar's Multi-Language Invoice Extractor")
input = st.text_input("Input Prompty: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg","jpeg","png"])

image_file=""
if uploaded_file is not None:
    image_file = Image.open(uploaded_file)
    st.image(image_file, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding Invoices. I will provide you an image of an invoice and you will have to answer any questions based on the information available in the uploaded iamge.
If you think that particular information is not there, please write "Requested Information was not found in the Invoice. Please try manual searching."
"""

##If the submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is: ")
    st.write(response)
