import streamlit as st
import pandas as pd
import hashlib
import os
from dotenv import load_dotenv
import requests
import json

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load existing user data
def load_user_data():
    try:
        users = pd.read_csv('users.csv')
    except FileNotFoundError:
        users = pd.DataFrame(columns=['username', 'password'])
    return users

# Save new user data
def save_user_data(users):
    users.to_csv('users.csv', index=False)

# User registration
def register_user():
    with st.container():
        st.subheader("Register")
        new_username = st.text_input("Email address", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        
        if st.button("Register"):
            if new_username and new_password:
                users = load_user_data()
                if new_username in users['username'].values:
                    st.error("This email is already registered.")
                else:
                    hashed_password = hash_password(new_password)
                    users = users.append({'username': new_username, 'password': hashed_password}, ignore_index=True)
                    save_user_data(users)
                    st.session_state['authenticated'] = True
                    st.success("You have successfully registered.")
            else:
                st.error("Please enter a valid email and password.")

# User login
def login_user():
    with st.container():
        st.subheader("Login")
        username = st.text_input("Email address", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            users = load_user_data()
            hashed_password = hash_password(password)
            if (users['username'] == username).any() and (users['password'] == hashed_password).any():
                st.session_state['authenticated'] = True
                st.success("You are logged in.")
            else:
                st.error("Invalid username or password.")

# Audio analysis page
def audio_analysis_page():
    st.markdown("<h1 style='text-align: center; color: black;'>GIDI AUDIO</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: black;'>SCAN.DETECT.PROTECT</h4>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload audio", type=['wav', 'mp3', 'flac'])
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        # Proceed with your file processing and audio analysis logic
        
        if st.button('Analyze'):
            # Your audio analysis code here
            st.write("This is where the audio analysis results will be displayed.")
            # Placeholder for demonstration. Replace with your analysis code.
            st.write({"label": "fake", "score": 0.999})

# Main app flow
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if st.session_state['authenticated']:
    audio_analysis_page()
else:
    login_user()
    register_user()

# Environment setup
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Page configuration
st.set_page_config(page_title='Gidi Audio Scanner', layout='wide')

# The API URL and headers for audio analysis
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
            print(result) 
            for index, item in enumerate(result):
                score = item['score'] * 100  # Convert to percentage
                label = "Fake" if item['label'] == "spoof" else "Real"
                st.write(f"Result {index}: {label} ({score:.2f}%)")
        else:
            st.error("Analysis failed. Please try again.")
    else:
        st.error("Please upload an audio file first.")


