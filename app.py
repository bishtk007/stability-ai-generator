import streamlit as st
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv
import base64
from datetime import datetime, timedelta
import time
import video_app

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

    /* Pricing Header */
    .pricing-header {
        background: linear-gradient(90deg, #13111C 0%, #1A1A1A 100%);
        padding: 0.5rem 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }

    .plan-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .plan-badge {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8E53 100%);
        padding: 0.2rem 0.8rem;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .plan-details {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .upgrade-section {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .upgrade-button {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .upgrade-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.2);
    }

    .pricing-popup {
        display: none;
        position: absolute;
        top: 100%;
        right: 0;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 0.5rem;
        width: 300px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .pricing-popup.show {
        display: block;
    }

    .plan-card {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }

    .plan-card h3 {
        margin: 0;
        color: white;
        font-size: 1.1rem;
    }

    .plan-card p {
        margin: 0.5rem 0;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .plan-price {
        font-size: 1.2rem;
        font-weight: 500;
        color: white;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_image(prompt, style="", width=1024, height=1024):
    try:
        # Get API key from environment variable
        api_key = st.secrets["STABILITY_API_KEY"]
        
        # Add artificial delay for free users
        if st.session_state.user_plan == 'free':
            progress_text = "Generating your image... (Free Plan - Standard Speed)"
            progress_bar = st.progress(0)
            
            # Simulate slower generation with progress updates
            for i in range(5):
                time.sleep(1)  # 5 second delay for free users
                progress_bar.progress((i + 1) * 20)
            
            progress_bar.empty()
        else:
            st.info("Generating your image... (Pro Plan - Instant Generation)")

        # Prepare the API request
        url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Add style to prompt if specified
        full_prompt = f"{prompt}, {style}" if style and style != "None" else prompt

        body = {
            "steps": 30,
            "width": width,
            "height": height,
            "seed": 0,
            "cfg_scale": 7,
            "samples": 1,
            "text_prompts": [
                {
                    "text": full_prompt,
                    "weight": 1
                }
            ],
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=body)
        
        if response.status_code != 200:
            raise Exception(f"Non-200 response: {response.text}")

        # Process and return the image
        data = response.json()
        image_data = base64.b64decode(data["artifacts"][0]["base64"])
        image = Image.open(io.BytesIO(image_data))
        
        # Update remaining images for free users
        if st.session_state.user_plan == 'free':
            st.session_state.images_remaining -= 1
        
        return image

    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def create_tabs():
    # Create tabs for Image and Video Generation
    tab1, tab2 = st.tabs(["🖼️ Image Generation", "🎥 Video Generation"])
    return tab1, tab2

def main():
    # Add session state for user plan
    if 'user_plan' not in st.session_state:
        st.session_state.user_plan = 'free'
        st.session_state.images_remaining = 10  # Increased to 10 images
    
    # Pricing Header
    st.markdown(
        f'''
        <div class="pricing-header">
            <div class="plan-info">
                <span class="plan-badge">Free Plan</span>
                <span class="plan-details">{st.session_state.images_remaining} images remaining today</span>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Upgrade Button and Pricing
    st.markdown(
        '''
        <div class="upgrade-section">
            <button class="upgrade-button" onclick="showPricing()">
                ⚡ Upgrade
                <span style="font-size: 0.8rem; opacity: 0.8;">$9.99/mo</span>
            </button>
            <div class="pricing-popup" id="pricingPopup">
                <div class="plan-card">
                    <h3>Free Plan</h3>
                    <p>Perfect for trying out</p>
                    <div class="plan-price">$0/month</div>
                    <p>• 10 images per day<br>• Standard generation (5s)<br>• Basic styles</p>
                </div>
                <div class="plan-card">
                    <h3>Pro Plan</h3>
                    <p>For serious creators</p>
                    <div class="plan-price">$9.99/month</div>
                    <p>• Unlimited images<br>• Instant generation<br>• All premium styles<br>• Priority support</p>
                </div>
            </div>
        </div>
        <script>
        function showPricing() {
            const popup = document.getElementById('pricingPopup');
            popup.classList.toggle('show');
        }
        </script>
        ''',
        unsafe_allow_html=True
    )

    # Create tabs
    image_tab, video_tab = create_tabs()

    # Image Generation Tab
    with image_tab:
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

        # Handle image generation
        if generate_button and prompt:
            if st.session_state.user_plan == 'free' and st.session_state.images_remaining <= 0:
                st.warning("⚡ You've used all your free images for today! Upgrade to Pro for unlimited generations.")
                return
                
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

    # Video Generation Tab
    with video_tab:
        video_app.video_generation_ui()

if __name__ == "__main__":
    main()
