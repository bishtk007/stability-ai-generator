import streamlit as st
import requests
from PIL import Image
import io
import os
import base64
import random
import tempfile

def generate_video(image, motion_style, duration, quality, prompt=""):
    try:
        api_key = st.secrets["STABILITY_API_KEY"]
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        url = "https://api.stability.ai/v1/generation/stable-video-diffusion/image-to-video"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Motion style parameters
        motion_params = {
            "Gentle Movement": {"motion_bucket_id": 127, "min_cfg": 1.0},
            "Zoom In": {"motion_bucket_id": 180, "min_cfg": 1.5},
            "Zoom Out": {"motion_bucket_id": 80, "min_cfg": 1.5},
            "Pan Left to Right": {"motion_bucket_id": 150, "min_cfg": 2.0},
            "Pan Right to Left": {"motion_bucket_id": 50, "min_cfg": 2.0},
            "Rotate Clockwise": {"motion_bucket_id": 200, "min_cfg": 2.5},
            "Rotate Counter-clockwise": {"motion_bucket_id": 100, "min_cfg": 2.5}
        }

        # Quality settings
        quality_params = {
            "Standard": {"num_frames": 14, "num_inference_steps": 25},
            "High": {"num_frames": 24, "num_inference_steps": 35},
            "Ultra": {"num_frames": 36, "num_inference_steps": 45}
        }

        motion = motion_params[motion_style]
        quality_settings = quality_params[quality]
        fps = max(8, min(30, int(quality_settings["num_frames"] / duration)))

        body = {
            "image": image_base64,
            "motion_bucket_id": motion["motion_bucket_id"],
            "cfg_scale": motion["min_cfg"],
            "num_frames": quality_settings["num_frames"],
            "num_inference_steps": quality_settings["num_inference_steps"],
            "fps": fps,
            "seed": random.randint(1, 1000000)
        }

        if prompt:
            body["text_prompts"] = [{"text": prompt, "weight": 1}]

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        data = response.json()
        if not data.get("artifacts"):
            raise Exception("No video data received from API")
        
        video_data = base64.b64decode(data["artifacts"][0]["base64"])
        
        # Save video to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_file.write(video_data)
        temp_file.close()
        
        return temp_file.name

    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        return None

def video_generation_ui():
    st.title("Turn Images into Videos")

    uploaded_file = st.file_uploader("Upload an image to animate", type=['png', 'jpg', 'jpeg'], key="video_image")
    
    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Motion options
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
            selected_motion = st.selectbox("Motion Style", motion_styles, key="motion_style")

        with col2:
            quality_options = ["Standard", "High", "Ultra"]
            quality = st.selectbox("Quality", quality_options, key="video_quality")

        # Duration slider
        duration = st.slider("Duration (seconds)", 1, 10, 3, key="video_duration")

        # Optional context prompt
        context_prompt = st.text_input("Add context for video generation (optional)", key="video_prompt")

        # Generate video button
        if st.button("Generate Video", type="primary", key="video_generate"):
            if st.session_state.user_plan == 'free' and st.session_state.images_remaining <= 0:
                st.warning("⚡ You've used all your free generations for today! Upgrade to Pro for unlimited generations.")
                return

            with st.spinner("Generating your video... This may take a few minutes"):
                video_path = generate_video(
                    image=image,
                    motion_style=selected_motion,
                    duration=duration,
                    quality=quality,
                    prompt=context_prompt
                )
                
                if video_path:
                    # Display the video
                    video_file = open(video_path, 'rb')
                    video_bytes = video_file.read()
                    st.video(video_bytes)
                    video_file.close()
                    
                    # Clean up the temporary file
                    os.unlink(video_path)
                    
                    # Update remaining generations for free users
                    if st.session_state.user_plan == 'free':
                        st.session_state.images_remaining -= 1

if __name__ == "__main__":
    # Set page config when running directly
    st.set_page_config(page_title="AI Video Generator", layout="wide")
    
    # Initialize session state
    if 'user_plan' not in st.session_state:
        st.session_state.user_plan = 'free'
        st.session_state.images_remaining = 10
        
    # Run the video generation UI
    video_generation_ui()
