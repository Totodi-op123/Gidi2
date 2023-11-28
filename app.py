#import required libraries
import streamlit as st
import json
import requests
import os
from io import StringIO, BytesIO
from dotenv import load_dotenv
import pandas as pd
import hashlib

#load .env file variables
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Set page config
st.set_page_config(page_title='Gidi Audio Scanner', layout='wide')

# Define the page header
st.markdown("<h1 style='text-align: center; color: white;'>GIDI AUDIO</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'>SCAN.DETECT.PROTECT</h4>", unsafe_allow_html=True)

#The API URL and headers
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/HyperMoon/wav2vec2-base-960h-finetuned-deepfake"

# File uploader allows the user to add their own audio
uploaded_file = st.file_uploader("Upload audio", type=['wav', 'mp3', 'flac'], key='file_uploader')

# Temporary directory for uploaded files
TEMP_DIR = "tempDir"
os.makedirs(TEMP_DIR, exist_ok=True)

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    payload = {"wait_for_model": True}
    response = requests.request("POST", API_URL, headers=headers, data=data, params=payload)
    return json.loads(response.content.decode("utf-8"))

# Handle file upload and save to the filesystem
if uploaded_file is not None:
    file_path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

# Single 'Analyze' button event
if st.button('Analyze'):
    if uploaded_file is not None:
        # Call the query function
        result = query(file_path)
        
        # Format and display results
        if result:
            for index, item in enumerate(result):
                score = item['score'] * 100  # Convert to percentage
                label = "Fake" if item['label'] == "spoof" else "Real"
                st.write(f"Result {index}: {label} ({score:.2f}%)")
        else:
            st.error("Analysis failed. Please try again.")
    else:
        st.error("Please upload an audio file first.")


