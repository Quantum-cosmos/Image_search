from dotenv import load_dotenv
import os

load_dotenv()

# API Keys
GOOGLE_SEARCH_KEY = os.getenv('GOOGLE_SEARCH_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Model Configuration
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
GEMINI_MODEL_NAME = 'gemini-pro'

# Default Settings
DEFAULT_NUM_IMAGES = 5
MAX_NUM_IMAGES = 10
DEFAULT_MARKDOWN_LENGTH = 200