import streamlit as st
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv
import base64
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Custom CSS for modern theme
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Modern Light Theme Colors */
    :root {
        --text-color: #1E1E1E;
        --background-color: #FFFFFF;
        --primary-color: #000000;
        --accent-color: #333333;
        --hover-color: #666666;
    }

    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
        background-color: var(--background-color);
    }

    /* Header Styles */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: var(--text-color);
    }

    .header-subtitle {
        font-size: 1.1rem;
        color: var(--accent-color);
        margin-bottom: 1rem;
    }

    /* Upgrade Banner */
    .upgrade-banner {
        background: linear-gradient(135deg, #000000, #333333);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .upgrade-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .upgrade-text {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    .upgrade-button {
        background-color: white !important;
        color: black !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: 500 !important;
        margin-top: 0.5rem !important;
        transition: all 0.3s ease !important;
    }

    .upgrade-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Button Styles */
    .stButton > button {
        background-color: white !important;
        color: black !important;
        border: 1px solid #E0E0E0 !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #F5F5F5 !important;
        border-color: #D0D0D0 !important;
    }

    /* Input Styles */
    .stTextInput > div > div > input {
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }

    /* Generated Image Container */
    .generated-image-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-top: 2rem;
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
</style>
""", unsafe_allow_html=True)

def generate_image(prompt, style="", negative_prompt="", width=1024, height=1024, steps=50):
    # Try to get API key from Streamlit secrets
    api_key = None
    if hasattr(st, 'secrets'):
        api_key = st.secrets.get("API_KEY")
    
    # Fallback to environment variable if not in secrets
    if not api_key:
        api_key = os.getenv('API_KEY')
        
    if not api_key:
        st.error("⚠️ API key not found! Please check your Streamlit secrets configuration.")
        return None

    api_host = 'https://api.stability.ai'
    engine_id = 'stable-diffusion-v1-6'

    # Combine style with prompt if style is selected
    full_prompt = f"{style} {prompt}".strip() if style else prompt

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": full_prompt,
                    "weight": 1
                }
            ],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "steps": steps,
            "samples": 1,
        },
    )

    if response.status_code != 200:
        st.error(f"Failed to generate image: {response.text}")
        return None

    data = response.json()
    
    if "artifacts" not in data:
        st.error(f"No image data in response: {data}")
        return None
        
    # Get the base64 string
    image_b64 = data["artifacts"][0]["base64"]
    
    # Convert to PIL Image
    image_data = base64.b64decode(image_b64)
    image = Image.open(io.BytesIO(image_data))
    
    return image

def main():
    # Header Section
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-title">AI Art Creator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Transform your ideas into stunning digital art with AI</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Upgrade Banner
    st.markdown("""
        <div class="upgrade-banner">
            <div class="upgrade-title">🌟 Unlock Premium Features</div>
            <div class="upgrade-text">Get unlimited generations, priority processing, and exclusive styles</div>
            <button class="upgrade-button">Upgrade Now - 50% OFF</button>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Tabs
    tab1, tab2, tab3 = st.tabs(["Create", "My Gallery", "Explore"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### What will you create?")
            prompt = st.text_input(
                "",
                placeholder="Describe your artistic vision in detail...",
                key="prompt_input",
                label_visibility="collapsed"
            )

            st.markdown("### Choose Your Style")
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
            selected_style = st.selectbox("", styles, label_visibility="collapsed")

        with col2:
            st.markdown("### Canvas Size")
            aspect_ratios = {
                "1:1 Square": (1024, 1024),
                "16:9 Landscape": (1024, 576),
                "9:16 Portrait": (576, 1024)
            }
            
            selected_ratio = None
            for ratio_name, dimensions in aspect_ratios.items():
                if st.button(ratio_name, key=f"ratio_{ratio_name}"):
                    selected_ratio = dimensions

        # Generate Button with enhanced styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_button = st.button("✨ Create Artwork", type="primary", use_container_width=True)

        if generate_button:
            if not prompt:
                st.warning("Please describe what you'd like to create!")
                return

            if not selected_ratio:
                selected_ratio = (1024, 1024)  # Default to square

            with st.spinner("Creating your masterpiece... 🎨"):
                clean_prompt = prompt.strip()
                if not clean_prompt:
                    st.warning("Please enter a valid prompt!")
                    return
                    
                style_prompt = selected_style if selected_style and selected_style != "None" else ""
                
                image = generate_image(
                    prompt=clean_prompt,
                    style=style_prompt,
                    negative_prompt="",
                    width=selected_ratio[0],
                    height=selected_ratio[1]
                )
                
                if image:
                    # Display the generated image in a container
                    st.markdown('<div class="generated-image-container animate-fade-in">', unsafe_allow_html=True)
                    st.image(image, caption="Your Generated Artwork", use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add to gallery
                    if 'generated_images' not in st.session_state:
                        st.session_state.generated_images = []
                    
                    st.session_state.generated_images.insert(0, {
                        'image': image,
                        'prompt': clean_prompt,
                        'style': selected_style,
                        'timestamp': datetime.now()
                    })

    with tab2:
        if 'generated_images' not in st.session_state:
            st.session_state.generated_images = []

        if st.session_state.generated_images:
            st.markdown("### Your Creative Gallery")
            
            cols = st.columns(3)
            for idx, img_data in enumerate(st.session_state.generated_images):
                with cols[idx % 3]:
                    st.markdown('<div class="generated-image-container animate-fade-in">', unsafe_allow_html=True)
                    st.image(img_data['image'], caption="Your Generated Artwork", use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Your gallery is empty. Start creating some amazing artwork! ✨")

    with tab3:
        st.markdown("### Trending Creations")
        st.info("Coming soon! Explore and get inspired by the community's artwork. 🎨")

    # Enhanced Footer
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown("Crafted with ❤️ by AI Art Creator")
    st.markdown("""
        <div class="social-icons">
            <a href="#" target="_blank">📘 Facebook</a>
            <a href="#" target="_blank">🐦 Twitter</a>
            <a href="#" target="_blank">📸 Instagram</a>
            <a href="#" target="_blank">💻 GitHub</a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
