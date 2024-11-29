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
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark theme
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Modern Dark Theme Colors */
    :root {
        --background-color: #0D1117;
        --secondary-bg: #161B22;
        --text-color: #F0F6FC;
        --accent-color: #7C3AED;
        --accent-hover: #9F67FF;
        --card-bg: #21262D;
        --border-color: #30363D;
        --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: var(--font-family);
    }

    /* Typography */
    h1 {
        font-family: var(--font-family);
        font-weight: 600;
        font-size: 28px !important;
        letter-spacing: -0.02em;
        margin-bottom: 24px !important;
    }

    h2 {
        font-family: var(--font-family);
        font-weight: 500;
        font-size: 24px !important;
        letter-spacing: -0.01em;
        margin: 20px 0 16px !important;
    }

    h3 {
        font-family: var(--font-family);
        font-weight: 500;
        font-size: 20px !important;
        letter-spacing: -0.01em;
        margin: 16px 0 12px !important;
    }

    p, .stMarkdown {
        font-family: var(--font-family);
        font-weight: 400;
        font-size: 16px !important;
        line-height: 1.6;
        margin-bottom: 16px;
    }

    /* Header Styling */
    .header-container {
        background: linear-gradient(180deg, var(--secondary-bg) 0%, var(--background-color) 100%);
        padding: 32px;
        border-radius: 16px;
        margin-bottom: 32px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .header-title {
        font-size: 32px !important;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 12px;
    }

    .header-subtitle {
        font-size: 18px !important;
        font-weight: 400;
        color: rgba(240, 246, 252, 0.8);
    }

    /* Navigation Tabs */
    .stTabs {
        background: var(--secondary-bg);
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 24px;
    }

    /* Input Fields */
    .stTextInput > div > div {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 8px 16px;
        font-family: var(--font-family);
        font-size: 16px !important;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div:focus-within {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
    }

    /* Buttons */
    .stButton > button {
        font-family: var(--font-family);
        font-weight: 500;
        font-size: 16px !important;
        background: linear-gradient(135deg, #7C3AED 0%, #9F67FF 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        transition: all 0.3s ease;
        text-transform: none;
        letter-spacing: 0;
        height: auto;
        margin: 8px 0;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #9F67FF 0%, #7C3AED 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }

    /* Select Box */
    .stSelectbox > div > div {
        font-family: var(--font-family);
        font-size: 16px !important;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-color);
        padding: 8px 16px;
    }

    /* Cards */
    .gallery-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 16px;
        margin: 12px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid var(--border-color);
    }

    .gallery-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
    }

    .gallery-card img {
        border-radius: 12px;
        margin-bottom: 12px;
    }

    .gallery-card .caption {
        font-size: 14px !important;
        color: rgba(240, 246, 252, 0.8);
        margin-bottom: 8px;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 32px;
        margin-top: 48px;
        border-top: 1px solid var(--border-color);
        font-size: 14px !important;
    }

    .social-icons {
        display: flex;
        justify-content: center;
        gap: 24px;
        margin-top: 16px;
    }

    .social-icons a {
        color: var(--text-color);
        text-decoration: none;
        font-size: 14px !important;
        opacity: 0.8;
        transition: opacity 0.2s ease;
    }

    .social-icons a:hover {
        opacity: 1;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

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
    # Header Section with enhanced typography
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-title">AI Art Creator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Transform your ideas into stunning digital art with AI</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
            
            st.markdown("### Refine Your Creation")
            negative_prompt = st.text_input(
                "",
                placeholder="Specify elements you'd like to avoid in your artwork...",
                help="Use this to exclude unwanted elements from your creation",
                label_visibility="collapsed"
            )

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
                # Ensure prompt is not empty and properly formatted
                clean_prompt = prompt.strip()
                if not clean_prompt:
                    st.warning("Please enter a valid prompt!")
                    return
                    
                # Only add style if it's selected and not "None"
                style_prompt = selected_style if selected_style and selected_style != "None" else ""
                
                image = generate_image(
                    prompt=clean_prompt,
                    style=style_prompt,
                    negative_prompt=negative_prompt.strip() if negative_prompt else "",
                    width=selected_ratio[0],
                    height=selected_ratio[1]
                )
                
                if image:
                    st.session_state.generated_images.insert(0, {
                        'image': image,
                        'prompt': clean_prompt,
                        'style': selected_style,
                        'timestamp': datetime.now()
                    })
                    st.success("✨ Your artwork is ready!")

    with tab2:
        if 'generated_images' not in st.session_state:
            st.session_state.generated_images = []

        if st.session_state.generated_images:
            st.markdown("### Your Creative Gallery")
            
            cols = st.columns(3)
            for idx, img_data in enumerate(st.session_state.generated_images):
                with cols[idx % 3]:
                    st.markdown('<div class="gallery-card fade-in">', unsafe_allow_html=True)
                    st.image(img_data['image'], use_column_width=True)
                    st.markdown(f'<p class="caption">Prompt: {img_data["prompt"]}</p>', unsafe_allow_html=True)
                    if img_data['style'] != "None":
                        st.markdown(f'<p class="caption">Style: {img_data["style"]}</p>', unsafe_allow_html=True)
                    
                    img_byte_arr = io.BytesIO()
                    img_data['image'].save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    st.download_button(
                        "↓ Download Artwork",
                        data=img_byte_arr,
                        file_name=f"ai_artwork_{idx}.png",
                        mime="image/png"
                    )
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
