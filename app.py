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

[... rest of your existing app.py code until the main() function ...]

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
        # Your existing image generation code...
        [... keep your existing image generation code ...]

    with tab2:
        # Video Generation Tab
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
                        # Get API key
                        api_key = os.getenv("STABILITY_API_KEY")
                        if not api_key:
                            try:
                                api_key = st.secrets["STABILITY_API_KEY"]
                            except:
                                st.error("API key not found. Please set STABILITY_API_KEY in secrets.toml or .env file")
                                return

                        # Convert image to base64
                        image_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                        
                        # Generate video
                        url = "https://api.stability.ai/v1/generation/stable-video-diffusion/text-to-video"
                        
                        headers = {
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        }

                        body = {
                            "image": image_data,
                            "motion_bucket_id": motion_bucket_id,
                            "seed": seed,
                            "prompt": prompt
                        }

                        response = requests.post(url, headers=headers, json=body)
                        
                        if response.status_code != 200:
                            raise Exception(f"Non-200 response: {response.text}")

                        result = response.json()
                        
                        if result:
                            st.success("✨ Video generated successfully!")
                            st.video(result['video_url'])
                            
                            # Download button
                            st.markdown(
                                f"""
                                <div style='text-align: center;'>
                                    <a href="{result['video_url']}" 
                                       target="_blank" 
                                       style="display: inline-block; 
                                              padding: 10px 20px; 
                                              background: linear-gradient(90deg, #6366f1, #8b5cf6); 
                                              color: white; 
                                              text-decoration: none; 
                                              border-radius: 5px; 
                                              margin-top: 10px;">
                                        📥 Download Video
                                    </a>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            # Display generation details
                            with st.expander("Generation Details"):
                                st.write(f"Motion Strength: {motion_bucket_id}")
                                st.write(f"Seed: {seed}")
                                if prompt:
                                    st.write(f"Prompt: {prompt}")
                                st.write(f"Style: {motion_style}")

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
