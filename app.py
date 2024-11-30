import streamlit as st
import requests
from PIL import Image
import io
import os
import base64
import random
import time
from video_app import video_generation_ui

# Set page config and styling
st.set_page_config(
    page_title="AI Art & Video Creator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS
st.markdown("""
    <style>
    /* Base theme */
    .stApp {
        background-color: #1a1b1e;
    }
    
    /* Hide unnecessary elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .stTabs {
        background-color: #23252a;
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTab {
        color: white !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #2d2f34;
        color: white !important;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff69b4, #ff8c00);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def generate_image(prompt, style="", width=1024, height=1024):
    try:
        api_key = st.secrets["STABILITY_API_KEY"]
        url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        body = {
            "text_prompts": [{"text": f"{prompt} {style}", "weight": 1}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": 30,
        }

        response = requests.post(url, headers=headers, json=body)
        if response.status_code != 200:
            raise Exception(f"Non-200 response: {response.text}")

        data = response.json()
        image_data = base64.b64decode(data["artifacts"][0]["base64"])
        image = Image.open(io.BytesIO(image_data))
        return image

    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def main():
    # Add session state for user plan and current tab
    if 'user_plan' not in st.session_state:
        st.session_state.user_plan = 'free'
        st.session_state.images_remaining = 10
    
    # Create tabs for Image and Video Generation
    tab1, tab2 = st.tabs(["🖼️ Image Generation", "🎥 Video Generation"])

    with tab1:
        st.markdown("""
            <div style='padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <h1 style='color: white; margin: 0; font-size: 2rem;'>AI Image Creator</h1>
                <p style='color: #ff69b4; font-size: 1.2rem; margin-top: 0.5rem;'>
                    Transform Your Ideas into Art
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Image generation UI
        prompt = st.text_input("", 
                             placeholder="Describe what you want to see",
                             key="image_prompt")
        
        col1, col2 = st.columns(2)
        with col1:
            styles = [
                "None",
                "Photorealistic",
                "Digital Art",
                "Cinematic",
                "Anime",
                "Oil Painting",
                "Watercolor",
                "3D Render",
                "Comic Book",
                "Fantasy Art"
            ]
            selected_style = st.selectbox("Style", styles, key="image_style")

        with col2:
            aspect_ratios = {
                "1:1 Square": (1024, 1024),
                "16:9 Landscape": (1024, 576),
                "9:16 Portrait": (576, 1024)
            }
            selected_ratio = st.selectbox("Aspect Ratio", list(aspect_ratios.keys()), key="image_ratio")

        if st.button("Generate", type="primary", key="image_generate", use_container_width=True):
            if prompt:
                if st.session_state.user_plan == 'free' and st.session_state.images_remaining <= 0:
                    st.warning("⚡ You've used all your free images for today! Upgrade to Pro for unlimited generations.")
                    return

                with st.spinner("Creating your masterpiece..."):
                    width, height = aspect_ratios[selected_ratio]
                    style_prompt = "" if selected_style == "None" else selected_style
                    image = generate_image(prompt, style_prompt, width, height)
                    
                    if image:
                        st.image(image, caption="Generated Image", use_column_width=True)
                        
                        # Add download button for the image
                        buffered = io.BytesIO()
                        image.save(buffered, format="PNG")
                        image_bytes = buffered.getvalue()
                        
                        st.download_button(
                            label="Download Image",
                            data=image_bytes,
                            file_name=f"generated_image_{int(time.time())}.png",
                            mime="image/png"
                        )
                        
                        if st.session_state.user_plan == 'free':
                            st.session_state.images_remaining -= 1

        # Display remaining generations for free users
        if st.session_state.user_plan == 'free':
            st.markdown(f"""
                <div style='background: #23252a; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                    <p style='color: #888888; margin: 0;'>
                        ⚡ {st.session_state.images_remaining} generations remaining today
                    </p>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        video_generation_ui()

    # Add upgrade section at the bottom
    st.markdown("""
        <div style='background: #23252a; padding: 2rem; border-radius: 10px; margin-top: 2rem; text-align: center;'>
            <h2 style='color: white; margin: 0;'>⚡ Upgrade to Pro</h2>
            <p style='color: #888888; font-size: 1.2rem; margin: 1rem 0;'>
                Get unlimited generations and premium features
            </p>
            <div style='margin: 1rem;'>
                <h3 style='color: #ff69b4;'>$9.99/month</h3>
                <ul style='color: #888888; list-style: none; padding: 0;'>
                    <li>✨ Unlimited Generations</li>
                    <li>🚀 Instant Generation</li>
                    <li>🎨 Priority Support</li>
                    <li>🎯 Advanced Settings</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
