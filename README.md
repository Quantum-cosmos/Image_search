# Image Search and Analysis App

This Streamlit application combines Google Image Search, CLIP model, and Gemini AI to provide an advanced image search and analysis experience.

## Features

- Search for images using Google Custom Search API
- Analyze images using OpenAI's CLIP model
- Generate detailed descriptions using Google's Gemini AI
- Interactive UI with customizable search parameters
- Visual analysis of search queries
- Score-based image ranking

## Setup

1. Clone this repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   GOOGLE_SEARCH_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_custom_search_engine_id
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your search query in the text input field
2. Adjust the number of images to search and display using the sliders
3. Click "Search and Analyze" to process your query
4. View the analysis and ranked images in the results section

## Requirements

See `requirements.txt` for a full list of dependencies.

Advance Image Search