import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def get_api_key():
    # Try getting from Streamlit secrets first
    try:
        return st.secrets["STABILITY_API_KEY"]
    except:
        # If not in secrets, try environment variables
        api_key = os.getenv("STABILITY_API_KEY")
        if api_key:
            return api_key
        else:
            st.error("API key not found. Please set STABILITY_API_KEY in secrets.toml or .env file")
            return None

def generate_video(image_data, motion_bucket_id=32, seed=0):
    try:
        api_key = get_api_key()
        if not api_key:
            return None

        url = "https://api.stability.ai/v1/generation/stable-video-diffusion/text-to-video"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        body = {
            "image": image_data,
            "motion_bucket_id": motion_bucket_id,
            "seed": seed
        }

        response = requests.post(url, headers=headers, json=body)
        
        if response.status_code != 200:
            raise Exception(f"Non-200 response: {response.text}")

        return response.json()

    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        return None

def video_generation_ui():
    st.title("Generate Videos with AI")
    
    # Upload image
    uploaded_file = st.file_uploader("Upload an image to animate", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            motion_strength = st.slider("Motion Strength", min_value=1, max_value=64, value=32)
        with col2:
            seed = st.number_input("Seed (optional)", value=0)
            
        if st.button("Generate Video", type="primary"):
            with st.spinner("Generating video..."):
                # Convert image to base64
                image_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                
                # Generate video
                result = generate_video(image_data, motion_strength, seed)
                
                if result:
                    st.video(result['video_url'])
                    st.success("Video generated successfully!")
                    st.markdown(f"[Download Video]({result['video_url']})")
