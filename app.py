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
    /* Modern Dark Theme Colors */
    :root {
        --background-color: #0D1117;
        --secondary-bg: #161B22;
        --text-color: #F0F6FC;
        --accent-color: #7C3AED;
        --accent-hover: #9F67FF;
        --card-bg: #21262D;
        --border-color: #30363D;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Header Styling */
    .header-container {
        background: linear-gradient(180deg, var(--secondary-bg) 0%, var(--background-color) 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Navigation Tabs */
    .stTabs {
        background: var(--secondary-bg);
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7C3AED 0%, #9F67FF 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #9F67FF 0%, #7C3AED 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }

    /* Input Fields */
    .stTextInput > div > div {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        color: var(--text-color);
    }

    /* Cards */
    .gallery-card {
        background: var(--card-bg);
        border-radius: 1rem;
        padding: 1rem;
        margin: 0.5rem;
        transition: transform 0.3s ease;
    }

    .gallery-card:hover {
        transform: translateY(-5px);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        color: var(--text-color);
    }

    /* Sidebar */
    .css-1d391kg {
        background: var(--secondary-bg);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
    }

    /* Social Icons */
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    }

    .social-icons a {
        color: var(--text-color);
        text-decoration: none;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
</style>
""", unsafe_allow_html=True)

def generate_image(prompt, style="", negative_prompt="", width=1024, height=1024, steps=50):
    api_key = os.getenv('STABILITY_API_KEY')
    if not api_key:
        st.error("Please set your STABILITY_API_KEY in the environment variables")
        return None

    api_host = 'https://api.stability.ai'
    engine_id = 'realistic-vision-v6'

    if style:
        prompt = f"{prompt}, {style}"

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
                    "text": prompt,
                    "weight": 1
                },
                {
                    "text": negative_prompt,
                    "weight": -1
                }
            ],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps,
        },
    )

    if response.status_code != 200:
        st.error(f"Failed to generate image: {response.text}")
        return None

    data = response.json()
    image_data = base64.b64decode(data["artifacts"][0]["base64"])
    return Image.open(io.BytesIO(image_data))

def main():
    # Header Section
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.title("AI Art Creator")
    st.markdown("Transform your ideas into stunning digital art with AI")
    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation Tabs
    tab1, tab2, tab3 = st.tabs(["Create", "My Gallery", "Explore"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            prompt = st.text_input(
                "What will you create today?",
                placeholder="Describe your artistic vision...",
                key="prompt_input"
            )

            # Style Selection
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
            selected_style = st.selectbox("Choose Your Style", styles)
            
            # Negative Prompt
            negative_prompt = st.text_input(
                "Negative Prompt",
                placeholder="Elements to avoid in your creation...",
                help="Specify what you don't want in the image"
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

        # Generate Button
        if st.button("✨ Generate Art", type="primary"):
            if not prompt:
                st.warning("Please describe what you'd like to create!")
                return

            if not selected_ratio:
                selected_ratio = (1024, 1024)  # Default to square

            with st.spinner("Creating your masterpiece... 🎨"):
                image = generate_image(
                    prompt=prompt,
                    style=selected_style if selected_style != "None" else "",
                    negative_prompt=negative_prompt,
                    width=selected_ratio[0],
                    height=selected_ratio[1]
                )
                
                if image:
                    st.session_state.generated_images.insert(0, {
                        'image': image,
                        'prompt': prompt,
                        'style': selected_style,
                        'timestamp': datetime.now()
                    })
                    st.success("Your artwork is ready! ✨")

    with tab2:
        if 'generated_images' not in st.session_state:
            st.session_state.generated_images = []

        if st.session_state.generated_images:
            st.markdown("### Your Creative Gallery")
            
            # Create a grid layout for images
            cols = st.columns(3)
            for idx, img_data in enumerate(st.session_state.generated_images):
                with cols[idx % 3]:
                    st.markdown('<div class="gallery-card fade-in">', unsafe_allow_html=True)
                    st.image(img_data['image'], use_column_width=True)
                    st.caption(f"Prompt: {img_data['prompt']}")
                    if img_data['style'] != "None":
                        st.caption(f"Style: {img_data['style']}")
                    
                    # Convert image for download
                    img_byte_arr = io.BytesIO()
                    img_data['image'].save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    st.download_button(
                        "↓ Download",
                        data=img_byte_arr,
                        file_name=f"ai_artwork_{idx}.png",
                        mime="image/png"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Your gallery is empty. Start creating some art! ✨")

    with tab3:
        st.markdown("### Trending Creations")
        st.info("Coming soon! Explore and get inspired by the community's artwork.")

    # Footer
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown("Made with ❤️ by AI Art Creator")
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
