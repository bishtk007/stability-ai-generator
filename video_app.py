import streamlit as st
import requests
from PIL import Image
import io
import base64
import time
import tempfile
import os

def video_generation_ui():
    st.title("🎥 Generate Videos with AI")
    
    # Container for the main content
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(90deg, #1a1a1a 0%, #2a2a2a 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: #ffffff;'>Transform Images into Videos</h3>
            <p style='margin: 10px 0 0 0; color: #cccccc;'>Upload an image and watch it come to life with AI-powered motion</p>
        </div>
        """, unsafe_allow_html=True)

        # Image Upload
        uploaded_file = st.file_uploader("Upload your image", type=['png', 'jpg', 'jpeg'], key="video_image_upload")
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Motion Style Selection
            st.markdown("<p style='margin-top: 20px; color: #cccccc;'>Select Motion Style</p>", unsafe_allow_html=True)
            motion_styles = {
                "Zoom Out": "A smooth camera zoom-out effect",
                "Zoom In": "A dynamic zoom-in motion",
                "Pan Left to Right": "Horizontal panning from left to right",
                "Pan Right to Left": "Horizontal panning from right to left",
                "Pan Up to Down": "Vertical panning from top to bottom",
                "Pan Down to Up": "Vertical panning from bottom to top",
                "Rotate": "Gentle rotating motion"
            }
            
            # Create two columns for options
            col1, col2 = st.columns(2)
            
            with col1:
                selected_style = st.selectbox(
                    "Motion Style",
                    list(motion_styles.keys()),
                    format_func=lambda x: x,
                    help="Choose how your image will animate"
                )
                
                # Display style description
                st.markdown(f"<p style='color: #888888; font-size: 0.9em;'>{motion_styles[selected_style]}</p>", unsafe_allow_html=True)
            
            with col2:
                # Quality Options
                quality_options = ["Standard", "High Quality"]
                selected_quality = st.selectbox(
                    "Quality",
                    quality_options,
                    help="Higher quality will take longer to generate"
                )
                
                # Duration Slider
                duration = st.slider(
                    "Duration (seconds)",
                    min_value=1,
                    max_value=10,
                    value=5,
                    help="Length of the generated video"
                )

            # Optional Context Prompt
            context_prompt = st.text_input(
                "Optional Context Prompt",
                placeholder="Add additional context to guide the video generation...",
                help="Describe any specific aspects you want to emphasize in the motion"
            )

            # Generate Video Button
            if st.button("Generate Video", type="primary", use_container_width=True):
                try:
                    # Check if user is on free plan and has generations remaining
                    if st.session_state.user_plan == 'free' and st.session_state.images_remaining <= 0:
                        st.warning("⚡ You've used all your free generations for today! Upgrade to Pro for unlimited generations.")
                        return

                    # Save uploaded image to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                        image.save(tmp_file, format='PNG')
                        tmp_file_path = tmp_file.name

                    # Stability AI API endpoint for video generation
                    api_key = st.secrets["STABILITY_API_KEY"]
                    url = "https://api.stability.ai/v1/generation/stable-video-diffusion/text-to-video"
                    
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }

                    # Prepare the request body
                    body = {
                        "motion_style": selected_style,
                        "quality": "high" if selected_quality == "High Quality" else "standard",
                        "duration": duration,
                        "image": base64.b64encode(open(tmp_file_path, 'rb').read()).decode('utf-8')
                    }

                    if context_prompt:
                        body["context_prompt"] = context_prompt

                    # Show generation progress
                    with st.spinner("🎬 Generating your video..."):
                        # Simulate processing time for demo
                        if st.session_state.user_plan == 'free':
                            progress_bar = st.progress(0)
                            for i in range(10):
                                time.sleep(1)
                                progress_bar.progress((i + 1) * 10)
                            progress_bar.empty()

                        # Make the API request
                        response = requests.post(url, headers=headers, json=body)
                        
                        if response.status_code != 200:
                            raise Exception(f"Error: {response.text}")

                        # Process the response
                        result = response.json()
                        video_data = base64.b64decode(result["video"])

                        # Save and display the video
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as video_file:
                            video_file.write(video_data)
                            st.video(video_file.name)
                            
                            # Download button for the video
                            with open(video_file.name, 'rb') as file:
                                st.download_button(
                                    label="Download Video",
                                    data=file,
                                    file_name="generated_video.mp4",
                                    mime="video/mp4"
                                )

                    # Update remaining generations for free users
                    if st.session_state.user_plan == 'free':
                        st.session_state.images_remaining -= 1

                    # Cleanup temporary files
                    os.unlink(tmp_file_path)

                except Exception as e:
                    st.error(f"Error generating video: {str(e)}")
                    if "API key" in str(e):
                        st.info("Please make sure your Stability AI API key is properly configured.")
                    elif "quota" in str(e).lower():
                        st.info("You've reached your API quota limit. Please try again later or upgrade your plan.")

        else:
            # Show placeholder/preview when no image is uploaded
            st.markdown(
                """
                <div style='background: #1a1a1a; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px;'>
                    <p style='color: #888888; margin: 0;'>Upload an image to start creating your video</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Pro Features Preview
        st.markdown("""
        <div style='background: linear-gradient(90deg, #1a1a1a 0%, #2a2a2a 100%); padding: 20px; border-radius: 10px; margin-top: 30px;'>
            <h4 style='margin: 0; color: #ffffff;'>✨ Pro Features</h4>
            <ul style='color: #cccccc; margin: 10px 0;'>
                <li>Unlimited video generations</li>
                <li>Higher quality processing</li>
                <li>Priority rendering</li>
                <li>Advanced motion styles</li>
                <li>Longer video durations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
