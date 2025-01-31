from dotenv import load_dotenv
import os

load_dotenv()

# API Keys
GOOGLE_SEARCH_KEY = "AIzaSyCIjeVCQVg9iPAYEYLYEIvewB_nXg6nnwU"
GOOGLE_CSE_ID = "93e00b09bfd6e4256"
GEMINI_API_KEY = "AIzaSyAulFzIkm9yvMawZBV5-HFoCEEu2BRzn7A"

# Model Configuration
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
GEMINI_MODEL_NAME = 'gemini-pro'

# Default Settings
DEFAULT_NUM_IMAGES = 5
MAX_NUM_IMAGES = 10
DEFAULT_MARKDOWN_LENGTH = 200