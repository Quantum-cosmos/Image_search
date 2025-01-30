import requests
import torch
import numpy as np
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from transformers import CLIPProcessor, CLIPModel
from config import (
    CLIP_MODEL_NAME, 
    GEMINI_MODEL_NAME,
    DEFAULT_MARKDOWN_LENGTH  # Add this import
)

class ImageAnalyzer:
    def __init__(self, google_api_key, cse_id, gemini_api_key):
        self.google_api_key = google_api_key
        self.cse_id = cse_id
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        self.clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        self.clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)

    def fetch_google_images(self, query, num=5):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "cx": self.cse_id,
            "key": self.google_api_key,
            "searchType": "image",
            "num": num
        }
        response = requests.get(url, params=params).json()
        return [item["link"] for item in response.get("items", [])]

    def download_images(self, image_urls):
        images = []
        for url in image_urls:
            try:
                response = requests.get(url, timeout=10)
                img = Image.open(BytesIO(response.content)).convert("RGB")
                images.append(img)
            except Exception as e:
                print(f"Failed to download {url}: {e}")
        return images

    def compute_scores(self, text_query, images):
        inputs = self.clip_processor(
            text=[text_query],
            images=images,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            text_features = self.clip_model.get_text_features(inputs["input_ids"], inputs["attention_mask"])
            image_features = self.clip_model.get_image_features(inputs["pixel_values"])

        text_features = text_features / text_features.norm(dim=1, keepdim=True)
        image_features = image_features / image_features.norm(dim=1, keepdim=True)

        scores = (text_features @ image_features.T).squeeze(0)
        return scores.numpy()

    def analyze_query(self, query, markdown_length=None):  # Add markdown_length parameter
        if markdown_length is None:
            markdown_length = DEFAULT_MARKDOWN_LENGTH

        keyword_prompt = f"""
        Analyze this image search query: "{query}"
        Identify and extract the MOST SPECIFIC compound noun phrases that represent
        the core visual subjects. Keep adjectives with their nouns as single units.
        Return ONLY a comma-separated list, no explanations.
        """
        keywords_response = self.gemini_model.generate_content(keyword_prompt)
        keywords = [k.strip() for k in keywords_response.text.split(',')]

        descriptions = {}
        for keyword in keywords:
            desc_prompt = f"""
            Write a visual-focused description for: "{keyword}". Focus on:
            - Color combinations
            - Material/texture hints
            - Spatial relationships
            - Distinctive visual features
            Keep the response within {markdown_length} characters.
            """
            desc_response = self.gemini_model.generate_content(desc_prompt)
            descriptions[keyword] = desc_response.text.strip()

        return keywords, descriptions