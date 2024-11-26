import streamlit as st

# Page config
st.set_page_config(
    page_title="AI Image Generator Guide",
    page_icon="🎨",
    layout="wide"
)

def main():
    st.title("🎨 Free AI Image Generator Guide")
    st.write("Generate high-quality images using Microsoft Designer!")

    # Quick Start Guide
    st.header("Quick Start Guide")
    st.markdown("""
    1. Go to [Microsoft Designer](https://designer.microsoft.com)
    2. Sign in with your Microsoft account (free)
    3. Click "Create with AI"
    4. Enter your prompt and generate!
    """)

    # Features
    st.header("✨ Features")
    st.markdown("""
    - 15 free images per day
    - High-quality DALL-E 3 generation
    - Multiple styles and sizes
    - No credit card needed
    - Commercial usage allowed
    """)

    # Pro Tips
    st.header("💡 Pro Tips for Better Images")
    
    with st.expander("📝 Prompt Tips"):
        st.markdown("""
        1. **Be Specific**
        - Bad: "a mountain"
        - Good: "a majestic snow-capped mountain at sunset with golden light reflecting off the peaks"

        2. **Specify Style**
        - Photography: "professional photography, 8K, HDR"
        - Art: "digital art, concept art, trending on artstation"
        - Painting: "oil painting, masterpiece, classical style"

        3. **Add Technical Details**
        - Camera: "shot with wide-angle lens, shallow depth of field"
        - Lighting: "dramatic lighting, golden hour, studio lighting"
        - Quality: "highly detailed, sharp focus, 8K resolution"
        """)
    
    with st.expander("🎯 Example Prompts"):
        st.markdown("""
        **Landscape Photography:**
        ```
        A breathtaking mountain landscape at sunset, snow-capped peaks reflecting golden light, crystal clear lake in foreground, shot with wide-angle lens, professional photography, 8K quality
        ```

        **Character Art:**
        ```
        A mystical warrior princess in elegant armor, standing in an enchanted forest, digital art style, magical lighting, highly detailed, trending on artstation
        ```

        **Abstract Art:**
        ```
        A surreal fusion of nature and technology, vibrant colors, flowing organic shapes intertwined with geometric patterns, modern digital art style
        ```
        """)

    # Common Issues
    st.header("❓ Common Questions")
    
    with st.expander("How many images can I generate?"):
        st.write("You get 15 free images per day. The counter resets every 24 hours.")

    with st.expander("Can I use these images commercially?"):
        st.write("Yes! Images generated with Microsoft Designer are free for commercial use.")

    with st.expander("What sizes are available?"):
        st.write("Microsoft Designer supports various sizes and aspect ratios, including square, portrait, and landscape formats.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        Ready to start? Visit <a href='https://designer.microsoft.com' target='_blank'>Microsoft Designer</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
