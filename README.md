# AI Image Generator

A Streamlit web application that generates images using Stability AI's API.

## Features

- Multiple aspect ratios
- Style presets
- Quality control
- Negative prompts
- Image history
- Download generated images

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API key:
   ```
   STABILITY_API_KEY=your_api_key_here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deployment

1. Create a GitHub repository
2. Push your code to GitHub
3. Visit [Streamlit Cloud](https://share.streamlit.io)
4. Connect your GitHub repository
5. Add your `STABILITY_API_KEY` to Streamlit secrets

## Environment Variables

- `STABILITY_API_KEY`: Your Stability AI API key

## Technologies Used

- Streamlit
- Stability AI API
- Python
- PIL (Python Imaging Library)
