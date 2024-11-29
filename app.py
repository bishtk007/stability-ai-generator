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

# Page config
st.set_page_config(
    page_title="AI Art Creator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme dashboard
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Modern Dark Theme Colors */
    :root {
        --background-color: #000000;
        --card-bg: #1a1a1a;
        --text-color: #ffffff;
        --border-color: #333333;
        --accent-color: #ff0080;
        --button-color: #ffffff;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }

    /* Header and Navigation */
    .stHeader {
        background-color: transparent !important;
        border-bottom: none !important;
    }

    /* Main Search Bar */
    .main-prompt-container {
        max-width: 900px;
        margin: 2rem auto;
        padding: 0 1rem;
    }

    .main-title {
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
        color: var(--text-color);
    }

    /* Custom Search Input */
    .search-container {
        display: flex;
        gap: 0.5rem;
        background: var(--card-bg);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }

    .stTextInput > div > div > input {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: none !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
    }

    /* Generate Button */
    .generate-button {
        background-color: var(--button-color) !important;
        color: var(--background-color) !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    .generate-button:hover {
        opacity: 0.9;
    }

    /* Navigation Tabs */
    .nav-container {
        display: flex;
        gap: 2rem;
        margin: 1rem 0;
        padding: 0 1rem;
    }

    .nav-item {
        color: var(--text-color);
        text-decoration: none;
        font-weight: 500;
        opacity: 0.7;
        transition: opacity 0.2s ease;
    }

    .nav-item:hover, .nav-item.active {
        opacity: 1;
    }

    /* Image Grid */
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
        padding: 1rem;
    }

    .image-card {
        background: var(--card-bg);
        border-radius: 12px;
        overflow: hidden;
        transition: transform 0.2s ease;
    }

    .image-card:hover {
        transform: translateY(-4px);
    }

    .image-card img {
        width: 100%;
        height: auto;
        object-fit: cover;
    }

    /* Upgrade Button */
    .upgrade-button {
        position: fixed;
        top: 1rem;
        right: 1rem;
        background: linear-gradient(45deg, #ff0080, #7928ca);
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 20px !important;
        font-weight: 500 !important;
        border: none !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Advanced Options */
    .options-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        padding: 0.5rem;
        background: var(--card-bg);
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }

    .option-group {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .option-label {
        color: var(--text-color);
        font-size: 0.9rem;
        opacity: 0.8;
    }

    /* Style and Ratio Buttons */
    .style-button, .ratio-button {
        background: transparent !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        padding: 0.3rem 0.8rem !important;
        border-radius: 16px !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }

    .style-button:hover, .ratio-button:hover,
    .style-button.active, .ratio-button.active {
        background: var(--accent-color) !important;
        border-color: var(--accent-color) !important;
    }

    /* Options Row */
    .options-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        align-items: center;
    }

    .option-group {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .option-label {
        color: var(--text-color);
        font-size: 0.9rem;
        opacity: 0.8;
        margin-right: 0.5rem;
    }

    /* Style the select boxes */
    .stSelectbox > div > div {
        background-color: var(--card-bg) !important;
        border-color: var(--border-color) !important;
    }

    .stSelectbox > div > div:hover {
        border-color: var(--accent-color) !important;
    }

    /* Section Divider */
    .section-divider {
        margin: 2rem 0;
        border-top: 1px solid var(--border-color);
        opacity: 0.2;
    }

    /* Hide Streamlit Components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
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
    # Upgrade Button
    st.markdown(
        '<button class="upgrade-button">⚡ Upgrade</button>',
        unsafe_allow_html=True
    )

    # Main Search Container
    st.markdown(
        '<div class="main-prompt-container">'
        '<h1 class="main-title">What will you create?</h1>'
        '</div>',
        unsafe_allow_html=True
    )

    # Create two columns for search and button
    col1, col2 = st.columns([5, 1])
    
    with col1:
        prompt = st.text_input(
            "",
            placeholder="Describe what you want to see",
            label_visibility="collapsed"
        )
    
    with col2:
        generate_button = st.button("Generate", type="primary", use_container_width=True)

    # Style and Aspect Ratio Options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="option-label">Style</p>', unsafe_allow_html=True)
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
        st.markdown('<p class="option-label">Aspect Ratio</p>', unsafe_allow_html=True)
        aspect_ratios = {
            "1:1 Square": (1024, 1024),
            "16:9 Landscape": (1024, 576),
            "9:16 Portrait": (576, 1024)
        }
        selected_ratio = st.selectbox(
            "",
            list(aspect_ratios.keys()),
            label_visibility="collapsed"
        )

    # Section Divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Navigation moved down
    st.markdown(
        '<div class="nav-container">'
        '<a href="#" class="nav-item active">🔍 Explore</a>'
        '<a href="#" class="nav-item">👥 Following</a>'
        '<a href="#" class="nav-item">🔥 Top</a>'
        '</div>',
        unsafe_allow_html=True
    )

    # Handle image generation
    if generate_button and prompt:
        with st.spinner("Creating your masterpiece... 🎨"):
            # Get the selected ratio dimensions
            width, height = aspect_ratios[selected_ratio]
            
            # Clean the prompt and add style
            clean_prompt = prompt.strip()
            if not clean_prompt:
                st.warning("Please enter a valid prompt!")
                return
                
            style_prompt = selected_style if selected_style and selected_style != "None" else ""
            
            image = generate_image(
                prompt=clean_prompt,
                style=style_prompt,
                width=width,
                height=height
            )
            
            if image:
                if 'generated_images' not in st.session_state:
                    st.session_state.generated_images = []
                st.session_state.generated_images.insert(0, {
                    'image': image,
                    'prompt': clean_prompt,
                    'style': selected_style,
                    'timestamp': datetime.now()
                })

    # Display Image Grid
    if 'generated_images' in st.session_state and st.session_state.generated_images:
        st.markdown('<div class="image-grid">', unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, img_data in enumerate(st.session_state.generated_images):
            with cols[idx % 3]:
                st.image(img_data['image'], use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="image-grid">'
            '<div class="image-card">Sample images will appear here</div>'
            '</div>',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
