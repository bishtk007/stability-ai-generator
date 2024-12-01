import streamlit as st
import requests
from PIL import Image
import io
import os
import base64
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    </style>
""", unsafe_allow_html=True)

def get_api_key():
    try:
        return st.secrets["STABILITY_API_KEY"]
    except:
        api_key = os.getenv("STABILITY_API_KEY")
        if api_key:
            return api_key
        else:
            st.error("API key not found. Please set STABILITY_API_KEY in secrets.toml or .env file")
            return None

def generate_image(prompt, style="", width=1024, height=1024):
    try:
        api_key = get_api_key()
        if not api_key:
            return None, None

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

def show_pricing_modal():
    # Create columns for the pricing cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="color: white;">Basic</h2>
                <h1 style="color: #8B5CF6; margin: 20px 0;">$9.99<span style="font-size: 16px; color: #A1A1AA;">/mo</span></h1>
                <p style="color: #8B5CF6; font-size: 14px;">Image & Video Generation</p>
                <ul style="list-style: none; padding: 0; text-align: left; color: white;">
                    <li style="margin: 10px 0;">✓ 100 Image Generations/month</li>
                    <li style="margin: 10px 0;">✓ 50 Video Generations/month</li>
                    <li style="margin: 10px 0;">✓ Standard Quality Output</li>
                    <li style="margin: 10px 0;">✓ Basic Image Styles</li>
                    <li style="margin: 10px 0;">✓ 1080p Video Resolution</li>
                    <li style="margin: 10px 0;">✓ Email Support</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("Get Started", key="basic_btn", use_container_width=True)

    with col2:
        st.markdown("""
            <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #8B5CF6;">
                <div style="background: #8B5CF6; color: white; padding: 5px 10px; border-radius: 15px; position: absolute; top: -10px; right: 10px; font-size: 12px;">MOST POPULAR</div>
                <h2 style="color: white;">Pro</h2>
                <h1 style="color: #8B5CF6; margin: 20px 0;">$19.99<span style="font-size: 16px; color: #A1A1AA;">/mo</span></h1>
                <p style="color: #8B5CF6; font-size: 14px;">Advanced Creation Suite</p>
                <ul style="list-style: none; padding: 0; text-align: left; color: white;">
                    <li style="margin: 10px 0;">✓ 500 Image Generations/month</li>
                    <li style="margin: 10px 0;">✓ 200 Video Generations/month</li>
                    <li style="margin: 10px 0;">✓ HD Quality Output</li>
                    <li style="margin: 10px 0;">✓ All Image Styles</li>
                    <li style="margin: 10px 0;">✓ 4K Video Resolution</li>
                    <li style="margin: 10px 0;">✓ Priority Processing</li>
                    <li style="margin: 10px 0;">✓ Advanced Motion Controls</li>
                    <li style="margin: 10px 0;">✓ Priority Support</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("Upgrade Now", key="pro_btn", type="primary", use_container_width=True)

    with col3:
        st.markdown("""
            <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="color: white;">Business</h2>
                <h1 style="color: #8B5CF6; margin: 20px 0;">$49.99<span style="font-size: 16px; color: #A1A1AA;">/mo</span></h1>
                <p style="color: #8B5CF6; font-size: 14px;">Professional Solution</p>
                <ul style="list-style: none; padding: 0; text-align: left; color: white;">
                    <li style="margin: 10px 0;">✓ 2000 Image Generations/month</li>
                    <li style="margin: 10px 0;">✓ 1000 Video Generations/month</li>
                    <li style="margin: 10px 0;">✓ Ultra HD Quality</li>
                    <li style="margin: 10px 0;">✓ Custom Style Training</li>
                    <li style="margin: 10px 0;">✓ 8K Video Resolution</li>
                    <li style="margin: 10px 0;">✓ Instant Processing</li>
                    <li style="margin: 10px 0;">✓ API Access</li>
                    <li style="margin: 10px 0;">✓ Custom Branding</li>
                    <li style="margin: 10px 0;">✓ Dedicated Support</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("Get Business", key="business_btn", use_container_width=True)

    with col4:
        st.markdown("""
            <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="color: white;">Enterprise</h2>
                <h1 style="color: #8B5CF6; margin: 20px 0;">$199.99<span style="font-size: 16px; color: #A1A1AA;">/mo</span></h1>
                <p style="color: #8B5CF6; font-size: 14px;">Enterprise Solution</p>
                <ul style="list-style: none; padding: 0; text-align: left; color: white;">
                    <li style="margin: 10px 0;">✓ Unlimited Generations</li>
                    <li style="margin: 10px 0;">✓ Maximum Quality Settings</li>
                    <li style="margin: 10px 0;">✓ White-label Solution</li>
                    <li style="margin: 10px 0;">✓ Custom API Integration</li>
                    <li style="margin: 10px 0;">✓ Custom Model Training</li>
                    <li style="margin: 10px 0;">✓ 24/7 Premium Support</li>
                    <li style="margin: 10px 0;">✓ SLA Guarantee</li>
                    <li style="margin: 10px 0;">✓ Custom Features</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.button("Contact Sales", key="enterprise_btn", use_container_width=True)

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
        st.title("Generate Videos with AI")
        
        # Upload image
        uploaded_file = st.file_uploader("Upload an image to animate", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            # Add prompt input with placeholder text
            prompt = st.text_area(
                "Describe the motion you want (Optional)",
                placeholder="Example: 'Make the person walk forward', 'Make the flower bloom', 'Make the water flow'",
                help="Describe how you want the image to animate. Be specific about the motion you want to see."
            )
            
            # Create two columns for controls
            col1, col2 = st.columns(2)
            
            with col1:
                motion_strength = st.slider(
                    "Motion Strength",
                    min_value=1,
                    max_value=64,
                    value=32,
                    help="Higher values create more dramatic motion, lower values create subtle motion"
                )
                
            with col2:
                seed = st.number_input(
                    "Seed (Optional)",
                    value=0,
                    help="Use the same seed to reproduce the same video motion"
                )
            
            # Add motion style selection
            motion_style = st.selectbox(
                "Motion Style",
                ["Smooth", "Dynamic", "Gentle", "Dramatic"],
                help="Choose the style of motion for your video"
            )
            
            # Map motion styles to motion bucket IDs
            motion_style_mapping = {
                "Smooth": 32,
                "Dynamic": 48,
                "Gentle": 16,
                "Dramatic": 64
            }
            
            # Update motion_bucket_id based on style
            motion_bucket_id = motion_style_mapping[motion_style]
                
            if st.button("Generate Video", type="primary"):
                with st.spinner("Generating video... This may take a few moments."):
                    try:
                        api_key = get_api_key()
                        if not api_key:
                            return

                        # Convert image to base64
                        image_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                        
                        # Generate video using the correct endpoint
url = "https://api.stability.ai/v1/generation/stable-video-diffusion/image-to-video/upscale"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

body = {
    "image": image_data,
    "seed": seed,
    "cfg_scale": 2.5,
    "motion_bucket_id": motion_bucket_id,
    "fps": 24
}

if prompt.strip():
    body["text_prompt"] = prompt
                                }
                            ]
                        }

                        response = requests.post(url, headers=headers, json=body)
                        
                        if response.status_code != 200:
                            st.error(f"Error: {response.text}")
                            return

                        result = response.json()
                        
                        # Updated response handling
                        if 'base64' in result:
                            # Save the video
                            video_data = base64.b64decode(result['base64'])
                            
                            # Save to a temporary file
                            temp_file = "temp_video.mp4"
                            with open(temp_file, "wb") as f:
                                f.write(video_data)
                            
                            # Display the video
                            st.success("✨ Video generated successfully!")
                            st.video(temp_file)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Video",
                                data=video_data,
                                file_name=f"generated_video_{int(time.time())}.mp4",
                                mime="video/mp4"
                            )
                            
                            # Display generation details
                            with st.expander("Generation Details"):
                                st.write(f"Motion Strength: {motion_bucket_id}")
                                st.write(f"Seed: {seed}")
                                if prompt:
                                    st.write(f"Prompt: {prompt}")
                                st.write(f"Style: {motion_style}")
                            
                            # Clean up temp file
                            try:
                                os.remove(temp_file)
                            except:
                                pass
                        else:
                            st.error("Invalid response format from API")

                    except Exception as e:
                        st.error(f"Error generating video: {str(e)}")

        # Add helpful tips
        with st.expander("Tips for better results"):
            st.markdown("""
            - Upload clear, high-quality images
            - Use descriptive prompts for specific motions
            - Experiment with different motion strengths
            - Try different seeds for varied results
            - Choose motion styles that match your desired outcome
            """)

    with tab3:
        st.title("Choose Your Plan")
        show_pricing_modal()

if __name__ == "__main__":
    main()
