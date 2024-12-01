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
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        padding: 10px 20px;
        border-radius: 20px;
        color: white;
        text-decoration: none;
        font-weight: bold;
        z-index: 1000;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Pricing cards */
    .pricing-container {
        display: flex;
        justify-content: space-around;
        padding: 20px;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .pricing-card {
        background: linear-gradient(145deg, #1a1c23, #2d2f34);
        border-radius: 20px;
        padding: 30px;
        width: 320px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        border: 1px solid #3f3f46;
    }
    
    .pricing-card:hover {
        transform: translateY(-5px);
    }
    
    .pricing-card.popular {
        border: 2px solid #6366f1;
        position: relative;
        overflow: hidden;
    }
    
    .popular-badge {
        position: absolute;
        top: 20px;
        right: -35px;
        background: #6366f1;
        color: white;
        padding: 8px 40px;
        transform: rotate(45deg);
        font-size: 14px;
    }
    
    .plan-name {
        color: #e4e4e7;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .price {
        font-size: 36px;
        color: #6366f1;
        margin: 20px 0;
        font-weight: bold;
    }
    
    .price span {
        font-size: 16px;
        color: #a1a1aa;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 20px 0;
        color: #e4e4e7;
        text-align: left;
    }
    
    .feature-list li {
        margin: 15px 0;
        padding-left: 25px;
        position: relative;
    }
    
    .feature-list li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #6366f1;
    }
    
    .buy-button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        padding: 12px 30px;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        margin-top: 20px;
        font-weight: bold;
        transition: transform 0.2s ease;
        border: none;
        cursor: pointer;
    }
    
    .buy-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }

    .generation-type {
        color: #8b5cf6;
        font-size: 14px;
        margin-top: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def show_pricing_modal():
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            padding: 20px;
        }
        .price-card {
            background: linear-gradient(145deg, #1a1c23, #2d2f34);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            color: white;
            position: relative;
            border: 1px solid #3f3f46;
        }
        .price-card.popular {
            border: 2px solid #6366f1;
        }
        .popular-badge {
            background: #6366f1;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            position: absolute;
            top: -12px;
            right: 20px;
            font-size: 12px;
        }
        .plan-name {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
        }
        .price {
            font-size: 36px;
            color: #6366f1;
            margin: 15px 0;
        }
        .price span {
            font-size: 16px;
            color: #a1a1aa;
        }
        .features {
            text-align: left;
            margin: 20px 0;
            list-style-type: none;
            padding: 0;
        }
        .features li {
            margin: 10px 0;
            padding-left: 25px;
            position: relative;
        }
        .features li:before {
            content: "✓";
            color: #6366f1;
            position: absolute;
            left: 0;
        }
        .generation-type {
            color: #8b5cf6;
            font-size: 14px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Pricing Grid
    st.markdown("""
        <div class="pricing-grid">
            <!-- Basic Plan -->
            <div class="price-card">
                <div class="plan-name">Basic</div>
                <div class="price">$9.99<span>/mo</span></div>
                <div class="generation-type">Image & Video Generation</div>
                <ul class="features">
                    <li>100 Image Generations/month</li>
                    <li>50 Video Generations/month</li>
                    <li>Standard Quality Output</li>
                    <li>Basic Image Styles</li>
                    <li>1080p Video Resolution</li>
                    <li>Email Support</li>
                </ul>
            </div>

            <!-- Pro Plan -->
            <div class="price-card popular">
                <div class="popular-badge">MOST POPULAR</div>
                <div class="plan-name">Pro</div>
                <div class="price">$19.99<span>/mo</span></div>
                <div class="generation-type">Advanced Creation Suite</div>
                <ul class="features">
                    <li>500 Image Generations/month</li>
                    <li>200 Video Generations/month</li>
                    <li>HD Quality Output</li>
                    <li>All Image Styles</li>
                    <li>4K Video Resolution</li>
                    <li>Priority Processing</li>
                    <li>Advanced Motion Controls</li>
                    <li>Priority Support</li>
                </ul>
            </div>

            <!-- Business Plan -->
            <div class="price-card">
                <div class="plan-name">Business</div>
                <div class="price">$49.99<span>/mo</span></div>
                <div class="generation-type">Professional Solution</div>
                <ul class="features">
                    <li>2000 Image Generations/month</li>
                    <li>1000 Video Generations/month</li>
                    <li>Ultra HD Quality</li>
                    <li>Custom Style Training</li>
                    <li>8K Video Resolution</li>
                    <li>Instant Processing</li>
                    <li>API Access</li>
                    <li>Custom Branding</li>
                    <li>Dedicated Support</li>
                </ul>
            </div>

            <!-- Enterprise Plan -->
            <div class="price-card">
                <div class="plan-name">Enterprise</div>
                <div class="price">$199.99<span>/mo</span></div>
                <div class="generation-type">Enterprise Solution</div>
                <ul class="features">
                    <li>Unlimited Generations</li>
                    <li>Maximum Quality Settings</li>
                    <li>White-label Solution</li>
                    <li>Custom API Integration</li>
                    <li>Custom Model Training</li>
                    <li>24/7 Premium Support</li>
                    <li>SLA Guarantee</li>
                    <li>Custom Features</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add buttons below each plan using Streamlit columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("Get Started", key="basic_btn", use_container_width=True)
    with col2:
        st.button("Upgrade Now", key="pro_btn", type="primary", use_container_width=True)
    with col3:
        st.button("Get Business", key="business_btn", use_container_width=True)
    with col4:
        st.button("Contact Sales", key="enterprise_btn", use_container_width=True)
        
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
