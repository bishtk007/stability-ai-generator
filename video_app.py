import streamlit as st
import requests
from PIL import Image
import io
import os
import base64
import tempfile
import time
from moviepy.editor import VideoFileClip

def video_generation_ui():
    # Custom CSS for modern dark theme
    st.markdown("""
        <style>
        /* Modern Dark Theme */
        .stApp {
            background-color: #1a1b1e;
        }
        
        .tab-container {
            background: #23252a;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .main-title {
            color: white;
            font-size: 24px;
            margin-bottom: 5px;
            font-weight: 600;
        }
        
        .subtitle {
            color: #ff69b4;
            font-size: 16px;
            margin-bottom: 20px;
        }
        
        .stTabs {
            background-color: #23252a;
            border-radius: 10px;
            padding: 10px;
        }
        
        .stTextInput > div > div > input {
            background-color: #2d2f34;
            color: white;
            border: 1px solid #3a3c42;
        }
        
        .upload-section {
            border: 2px dashed #3a3c42;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }
        
        /* Custom button styling */
        .stButton>button {
            background: linear-gradient(45deg, #ff69b4, #ff8c00);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title Section
    st.markdown('<p class="main-title">Reimagine Video Creation</p>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["Text to Video", "Image to Video"])

    with tab2:  # Image to Video tab
        st.markdown('<p class="subtitle">Transform Your Images into Videos</p>', unsafe_allow_html=True)
        
        # Upload section with modern styling
        uploaded_file = st.file_uploader(
            "Upload your image",
            type=['png', 'jpg', 'jpeg'],
            key="video_image"
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)

            # Options in columns
            col1, col2 = st.columns(2)
            with col1:
                motion_styles = [
                    "Gentle Movement",
                    "Zoom In",
                    "Zoom Out",
                    "Pan Left to Right",
                    "Pan Right to Left",
                    "Rotate Clockwise",
                    "Rotate Counter-clockwise"
                ]
                selected_motion = st.selectbox("Motion Style", motion_styles)

            with col2:
                quality_options = ["Standard", "High", "Ultra"]
                quality = st.selectbox("Quality", quality_options)

            # Duration with modern slider
            duration = st.slider("Duration (seconds)", 1, 30, 4)

            # Generate button
            if st.button("Generate Video", type="primary", use_container_width=True):
                with st.spinner("Creating your video..."):
                    # Your existing video generation code here
                    pass

        else:
            # Placeholder when no image is uploaded
            st.markdown(
                """
                <div class="upload-section">
                    <p style='color: #888888;'>Drop your image here or click to upload</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab1:  # Text to Video tab (placeholder for future implementation)
        st.markdown('<p class="subtitle">Create Videos from Text Description</p>', unsafe_allow_html=True)
        st.text_area("Describe your video", placeholder="Enter a detailed description of the video you want to create...")
        st.info("Text to Video feature coming soon!")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Video Creation",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    video_generation_ui()
