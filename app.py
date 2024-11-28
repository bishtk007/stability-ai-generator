import streamlit as st
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv
import base64

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

# Constants
API_KEY = os.getenv("STABILITY_API_KEY")
API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

def generate_image(prompt, style="", negative_prompt="", width=1024, height=1024, steps=50):
    """Generate an image using Stability AI API"""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Combine style with prompt if style is selected
    full_prompt = f"{prompt}, {style}" if style else prompt

    body = {
        "steps": steps,  # Maximum allowed by API is 50
        "width": width,
        "height": height,
        "seed": 0,  # Random seed
        "cfg_scale": 9,  # Increased for better prompt adherence
        "samples": 1,
        "text_prompts": [
            {
                "text": full_prompt,
                "weight": 1.0
            }
        ]
    }

    # Add negative prompt if provided
    if negative_prompt:
        body["text_prompts"].append({
            "text": negative_prompt,
            "weight": -1.0
        })

    try:
        response = requests.post(API_URL, headers=headers, json=body)
        
        if response.status_code != 200:
            st.error(f"Error: {response.status_code}")
            st.error(f"Response: {response.text}")
            return None
            
        data = response.json()
        if "artifacts" in data and len(data["artifacts"]) > 0:
            image_data = data["artifacts"][0]["base64"]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            return image
        else:
            st.error("No image data in response")
            return None
            
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP Error: {http_err}")
        return None
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        st.error(f"Error type: {type(e)}")
        return None

def main():
    # Main heading
    st.markdown('<h1 class="main-heading">Bring your imagination to life</h1>', unsafe_allow_html=True)

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Top prompt bar
    col1, col2 = st.columns([4, 1])
    
    with col1:
        prompt = st.text_input(
            "",
            placeholder="Describe the image you want to create...",
            label_visibility="collapsed"
        )
    
    with col2:
        generate_btn = st.button("Generate", use_container_width=True)

    # Aspect ratio selection
    st.markdown("### Choose Aspect Ratio")
    aspect_ratios = {
        "1:1 Square": (1024, 1024),
        "16:9 Landscape": (1344, 768),
        "9:16 Portrait": (768, 1344)
    }
    
    # Initialize selected ratio in session state if not present
    if 'selected_ratio' not in st.session_state:
        st.session_state.selected_ratio = (1024, 1024)  # Default to 1:1
    
    # Create columns for aspect ratio buttons
    ratio_cols = st.columns(3)
    
    # Display aspect ratio buttons
    for idx, (ratio_name, dimensions) in enumerate(aspect_ratios.items()):
        with ratio_cols[idx]:
            # Check if this ratio is currently selected
            is_selected = st.session_state.selected_ratio == dimensions
            button_type = "primary" if is_selected else "secondary"
            
            if st.button(
                ratio_name, 
                key=f"ratio_{ratio_name}", 
                use_container_width=True,
                type=button_type
            ):
                st.session_state.selected_ratio = dimensions

    # Style and quality settings
    st.markdown("### Image Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        style = st.selectbox(
            "Style",
            ["Auto (Best Quality)", "Photorealistic", "Digital Art", "Cinematic", "Anime", "Oil Painting", "None"],
            index=0
        )
        
    with col2:
        negative_prompt = st.text_input("Negative Prompt", placeholder="Things to avoid...")

    # Style prompt mappings
    style_prompts = {
        "Auto (Best Quality)": "masterpiece, professional photography, highly detailed, 8k uhd, cinematic lighting, sharp focus, best quality, ultra realistic",
        "Photorealistic": "photorealistic, highly detailed, professional photography, 8k uhd",
        "Digital Art": "digital art, highly detailed, trending on artstation, 8k",
        "Cinematic": "cinematic, dramatic lighting, movie scene quality, 8k",
        "Anime": "anime style, high quality, detailed anime art, studio quality",
        "Oil Painting": "oil painting masterpiece, classical art style, museum quality",
        "None": ""
    }

    # Create columns for generated images
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []

    # Generate image when button is clicked
    if generate_btn:
        if not prompt:
            st.error("Please enter a prompt first!")
        else:
            with st.spinner("Creating your masterpiece..."):
                # Use selected ratio or default to 1:1
                width, height = st.session_state.get('selected_ratio', (1024, 1024))
                
                image = generate_image(
                    prompt=prompt,
                    style=style_prompts[style],
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    steps=50  # Set to maximum allowed by API
                )
                
                if image:
                    # Save image
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    # Add to session state
                    st.session_state.generated_images.insert(0, {
                        'image': image,
                        'bytes': byte_im,
                        'prompt': prompt
                    })

    # Display generated images in a grid
    if st.session_state.generated_images:
        st.markdown("### Generated Images")
        
        # Create rows of 4 images each
        for i in range(0, len(st.session_state.generated_images), 4):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                if i + j < len(st.session_state.generated_images):
                    img_data = st.session_state.generated_images[i + j]
                    with col:
                        # Container for image and buttons
                        with st.container():
                            # Display image with fixed size
                            st.image(img_data['image'], caption=img_data['prompt'][:50] + "..." if len(img_data['prompt']) > 50 else img_data['prompt'], 
                                   width=250)  # Fixed width for consistent sizing
                            
                            # Download button below image
                            st.download_button(
                                "Download",
                                img_data['bytes'],
                                f"generated_image_{i+j}.png",
                                "image/png",
                                use_container_width=True
                            )

if __name__ == "__main__":
    main()
