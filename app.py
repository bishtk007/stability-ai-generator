import streamlit as st
import requests
from PIL import Image
import io
import os
import base64
import time
from video_app import video_generation_ui

# Set page config
st.set_page_config(page_title="AI Art Generator", layout="wide")

# Custom CSS for pricing modal and upgrade button
st.markdown("""
    <style>
    /* Floating upgrade button */
    .upgrade-button {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(45deg, #ff69b4, #ff8c00);
        padding: 10px 20px;
        border-radius: 20px;
        color: white;
        text-decoration: none;
        font-weight: bold;
        z-index: 1000;
        cursor: pointer;
    }
    
    /* Pricing cards */
    .pricing-container {
        display: flex;
        justify-content: space-around;
        padding: 20px;
        gap: 20px;
    }
    
    .pricing-card {
        background: #2d2f34;
        border-radius: 15px;
        padding: 20px;
        width: 300px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .pricing-card.popular {
        border: 2px solid #ff69b4;
        transform: scale(1.05);
    }
    
    .price {
        font-size: 2.5rem;
        color: #ff69b4;
        margin: 20px 0;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 20px 0;
        color: white;
    }
    
    .feature-list li {
        margin: 10px 0;
    }
    
    .buy-button {
        background: linear-gradient(45deg, #ff69b4, #ff8c00);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        text-decoration: none;
        display: inline-block;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def show_pricing_modal():
    st.markdown("""
        <div class="pricing-container">
            <div class="pricing-card">
                <h2>Basic</h2>
                <div class="price">$9.99/mo</div>
                <ul class="feature-list">
                    <li>✨ 100 Generations/month</li>
                    <li>🎨 Standard Quality</li>
                    <li>⚡ Normal Processing Speed</li>
                    <li>📧 Email Support</li>
                </ul>
                <a href="#" class="buy-button">Get Started</a>
            </div>
            
            <div class="pricing-card popular">
                <h2>Pro</h2>
                <div class="price">$19.99/mo</div>
                <ul class="feature-list">
                    <li>✨ 500 Generations/month</li>
                    <li>🎨 HD Quality</li>
                    <li>⚡ Priority Processing</li>
                    <li>🎯 Advanced Settings</li>
                    <li>💬 Priority Support</li>
                </ul>
                <a href="#" class="buy-button">Most Popular</a>
            </div>
            
            <div class="pricing-card">
                <h2>Enterprise</h2>
                <div class="price">$49.99/mo</div>
                <ul class="feature-list">
                    <li>✨ Unlimited Generations</li>
                    <li>🎨 Ultra HD Quality</li>
                    <li>⚡ Instant Processing</li>
                    <li>🎯 Custom API Access</li>
                    <li>🤝 Dedicated Support</li>
                    <li>📊 Analytics Dashboard</li>
                </ul>
                <a href="#" class="buy-button">Contact Sales</a>
            </div>
        </div>
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
        return image, image_data

    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None, None

def main():
    # Add session state for user plan and current tab
    if 'user_plan' not in st.session_state:
        st.session_state.user_plan = 'free'
        st.session_state.images_remaining = 10
        st.session_state.show_pricing = False

    # Add floating upgrade button
    st.markdown("""
        <div class="upgrade-button" onclick="document.getElementById('pricing-section').scrollIntoView();">
            ⚡ Upgrade
        </div>
    """, unsafe_allow_html=True)

    # Create tabs for Image and Video Generation
    tab1, tab2, tab3 = st.tabs(["🖼️ Image Generation", "🎥 Video Generation", "💎 Pricing"])

    with tab1:
        st.title("Generate Images with AI")
        prompt = st.text_input("Describe what you want to see", key="image_prompt")
        
        col1, col2 = st.columns(2)
        with col1:
            styles = ["None", "Photorealistic", "Cinematic", "Anime", "Digital Art", "Fantasy"]
            selected_style = st.selectbox("Style", styles, key="image_style")

        with col2:
            aspect_ratios = {
                "1:1 Square": (1024, 1024),
                "16:9 Landscape": (1024, 576),
                "9:16 Portrait": (576, 1024)
            }
            selected_ratio = st.selectbox("Aspect Ratio", list(aspect_ratios.keys()), key="image_ratio")

        if st.button("Generate", type="primary", key="image_generate"):
            if prompt:
                if st.session_state.user_plan == 'free' and st.session_state.images_remaining <= 0:
                    st.warning("⚡ You've used all your free images for today! Upgrade to Pro for unlimited generations.")
                    st.session_state.show_pricing = True
                    return

                with st.spinner("Creating your masterpiece..."):
                    width, height = aspect_ratios[selected_ratio]
                    style_prompt = "" if selected_style == "None" else selected_style
                    image, image_data = generate_image(prompt, style_prompt, width, height)
                    
                    if image and image_data:
                        st.image(image, caption="Generated Image", use_column_width=True)
                        
                        # Add download button
                        st.download_button(
                            label="Download Image",
                            data=image_data,
                            file_name=f"generated_image_{int(time.time())}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                        
                        if st.session_state.user_plan == 'free':
                            st.session_state.images_remaining -= 1
                            st.info(f"⚡ {st.session_state.images_remaining} generations remaining today")

    with tab2:
        video_generation_ui()

    with tab3:
        st.title("Choose Your Plan")
        show_pricing_modal()

if __name__ == "__main__":
    main()
