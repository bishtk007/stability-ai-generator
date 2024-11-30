import streamlit as st
import requests
from PIL import Image
import io
import os
import base64
import tempfile
import time

def video_generation_ui():
    # Title Section with custom styling
    st.markdown("""
        <div style='padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <h1 style='color: white; margin: 0; font-size: 2rem;'>Reimagine Video Creation</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["Text to Video", "Image to Video"])

    with tab2:  # Image to Video tab
        st.markdown("""
            <p style='color: #ff69b4; font-size: 1.2rem; margin-bottom: 1rem;'>
                Transform Your Images into Videos
            </p>
        """, unsafe_allow_html=True)
        
        # Upload section
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
                if st.session_state.user_plan == 'free' and st.session_state.images_remaining <= 0:
                    st.warning("⚡ You've used all your free generations today! Upgrade to Pro for unlimited generations.")
                    return

                with st.spinner("Creating your video..."):
                    try:
                        # Convert image to base64
                        buffered = io.BytesIO()
                        image.save(buffered, format="PNG")
                        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                        # Get API key
                        api_key = st.secrets["STABILITY_API_KEY"]
                        
                        url = "https://api.stability.ai/v1/generation/stable-video-diffusion/image-to-video"
                        
                        headers = {
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        }

                        body = {
                            "image": image_base64,
                            "seed": 0,
                            "cfg_scale": 2.5,
                            "motion_bucket_id": 127
                        }

                        response = requests.post(url, headers=headers, json=body)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Save and display the video
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                                video_data = base64.b64decode(result['videos'][0])
                                tmp_file.write(video_data)
                                st.video(tmp_file.name)
                                
                                # Download button
                                st.download_button(
                                    label="Download Video",
                                    data=video_data,
                                    file_name="generated_video.mp4",
                                    mime="video/mp4"
                                )
                                
                            # Update remaining generations for free users
                            if st.session_state.user_plan == 'free':
                                st.session_state.images_remaining -= 1
                        else:
                            st.error(f"Error: {response.text}")

                    except Exception as e:
                        st.error(f"Error generating video: {str(e)}")

        else:
            # Placeholder when no image is uploaded
            st.markdown(
                """
                <div style='background: #23252a; padding: 2rem; border-radius: 10px; text-align: center; margin: 1rem 0;'>
                    <p style='color: #888888; margin: 0;'>Drop your image here or click to upload</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab1:  # Text to Video tab
        st.markdown("""
            <p style='color: #ff69b4; font-size: 1.2rem; margin-bottom: 1rem;'>
                Create Videos from Text Description
            </p>
        """, unsafe_allow_html=True)
        st.text_area("Describe your video", placeholder="Enter a detailed description of the video you want to create...")
        st.info("Text to Video feature coming soon!")

if __name__ == "__main__":
    if 'user_plan' not in st.session_state:
        st.session_state.user_plan = 'free'
        st.session_state.images_remaining = 10
    video_generation_ui()
