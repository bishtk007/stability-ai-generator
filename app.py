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
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --background-color: #09090B;
        --text-color: #FFFFFF;
        --secondary-text: #A1A1AA;
        --border-color: #27272A;
        --input-bg: #18181B;
        --button-bg: #3F3F46;
        --button-hover: #52525B;
    }

    /* Global dark theme */
    .stApp {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }

    /* Main heading */
    .main-heading {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        text-align: center !important;
        margin: 2rem 0 !important;
        padding: 0 !important;
    }

    /* Prompt input styling */
    .stTextInput > div > div {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-color) !important;
    }

    .stTextInput input {
        color: var(--text-color) !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
    }

    /* Button styling */
    .stButton > button {
        background-color: var(--button-bg) !important;
        color: var(--text-color) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: var(--button-hover) !important;
        transform: translateY(-2px);
    }

    /* Aspect ratio buttons */
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-color) !important;
    }

    /* Settings styling */
    .stSelectbox > div > div {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-color) !important;
    }

    .stSlider > div > div {
        background-color: var(--button-bg) !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Section headings */
    h3 {
        color: var(--text-color) !important;
        font-size: 1.2rem !important;
        margin-top: 2rem !important;
    }

    /* Spinner color */
    .stSpinner > div > div {
        border-top-color: var(--text-color) !important;
    }
</style>
""", unsafe_allow_html=True)

def generate_image(prompt, style="", negative_prompt="", width=1024, height=1024, steps=50):
    api_key = os.getenv('STABILITY_API_KEY')
    if not api_key:
        st.error("Please set your STABILITY_API_KEY in the .env file")
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
    st.markdown('<h1 class="main-heading">AI Image Generator</h1>', unsafe_allow_html=True)

    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []

    col1, col2 = st.columns([2, 1])

    with col1:
        prompt = st.text_input("Enter your prompt", placeholder="Describe the image you want to generate...")
        
        negative_prompt = st.text_input("Negative prompt (Optional)", 
                                      placeholder="What you don't want in the image...",
                                      help="Specify elements you want to exclude from the image")

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
        selected_style = st.selectbox("Select Style", styles)
        style_prompt = "" if selected_style == "None" else selected_style

    with col2:
        st.write("Choose Aspect Ratio")
        aspect_ratios = {
            "1:1 (Square)": (1024, 1024),
            "16:9 (Landscape)": (1024, 576),
            "9:16 (Portrait)": (576, 1024)
        }
        
        ar_cols = st.columns(3)
        selected_ratio = None
        
        for idx, (ratio_name, dimensions) in enumerate(aspect_ratios.items()):
            if ar_cols[idx].button(ratio_name):
                selected_ratio = dimensions

    if st.button("Generate Image", type="primary"):
        if not prompt:
            st.warning("Please enter a prompt first!")
            return

        if not selected_ratio:
            selected_ratio = (1024, 1024)  # Default to square if none selected

        with st.spinner("Generating your image..."):
            image = generate_image(
                prompt=prompt,
                style=style_prompt,
                negative_prompt=negative_prompt,
                width=selected_ratio[0],
                height=selected_ratio[1]
            )
            
            if image:
                st.session_state.generated_images.insert(0, {
                    'image': image,
                    'prompt': prompt,
                    'timestamp': datetime.now()
                })
                st.success("Image generated successfully!")

    if st.session_state.generated_images:
        st.markdown("### Generated Images")
        
        cols = st.columns(3)
        for idx, img_data in enumerate(st.session_state.generated_images):
            with cols[idx % 3]:
                st.image(img_data['image'], use_column_width=True)
                st.caption(f"Prompt: {img_data['prompt']}")
                
                img_byte_arr = io.BytesIO()
                img_data['image'].save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                st.download_button(
                    label="Download",
                    data=img_byte_arr,
                    file_name=f"generated_image_{idx}.png",
                    mime="image/png"
                )

if __name__ == "__main__":
    main()
