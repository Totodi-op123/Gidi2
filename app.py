#import required libraries
import streamlit as st
import json
import requests
import os
from io import StringIO, BytesIO
from dotenv import load_dotenv
import pandas as pd

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

if uploaded_file is not None:
    # Save the uploaded file to the filesystem
    file_path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display a message
    st.success("File uploaded successfully!")

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    payload = {"wait_for_model": True}
    # data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data, params={"wait_for_model": True})
    return json.loads(response.content.decode("utf-8"))


if st.button('Analyze'):
    if uploaded_file is not None:
        # Call the query function
        result = query(file_path)

        # Display results
        st.write(result)
    else:
        st.error("Please upload an audio file first.")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    
    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    # To read file as string:
    string_data = stringio.read()
    
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = st.file_uploader("Upload audio", type=['wav', 'mp3', 'flac'])

uploaded_file = st.session_state['uploaded_file']

if st.button('Analyze', key='analyze_button'):
    if uploaded_file is not None:
        # Save the uploaded audio file to the filesystem
        with open(os.path.join("tempDir", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Call the query function
        result = query(os.path.join("tempDir", uploaded_file.name))
        
        # Display results
        st.write(result)
    else:
        st.error("Please upload an audio file first.")

# This line is outside of the 'if' blocks and will always execute
st.legacy_caching.clear_cache()
