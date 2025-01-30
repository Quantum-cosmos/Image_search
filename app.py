import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO  # Add this import
import requests
from utils import ImageAnalyzer
from config import (
    GOOGLE_SEARCH_KEY, 
    GOOGLE_CSE_ID, 
    GEMINI_API_KEY,
    DEFAULT_NUM_IMAGES, 
    MAX_NUM_IMAGES, 
    DEFAULT_MARKDOWN_LENGTH
)

# Custom CSS
st.set_page_config(page_title="Image Search & Analysis", layout="wide")

st.markdown("""
<style>
.main-title {
    text-align: center;
    padding: 20px;
    color: #1f1f1f;
    background: linear-gradient(90deg, #dae1e7, #cfd8dc);
    border-radius: 12px;
    margin-bottom: 30px;
}
.markdown-content {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.query-box {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-title"><h1>🎨 Advanced Image Search & Analysis</h1></div>', 
                unsafe_allow_html=True)

    # Initialize ImageAnalyzer
    analyzer = ImageAnalyzer(GOOGLE_SEARCH_KEY, GOOGLE_CSE_ID, GEMINI_API_KEY)

    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Search Configuration")
        st.markdown("---")
        num_images = st.slider("🔍 Number of images to search:", 
                             min_value=1, max_value=MAX_NUM_IMAGES, 
                             value=DEFAULT_NUM_IMAGES)
        display_images = st.slider("🖼️ Number of images to display:", 
                                 min_value=1, max_value=MAX_NUM_IMAGES, 
                                 value=DEFAULT_NUM_IMAGES)
        markdown_length = st.slider("📝 Analysis detail level:", 
                                  min_value=100, max_value=500, 
                                  value=DEFAULT_MARKDOWN_LENGTH)

    # Main content area
    st.markdown("""
    <div class="query-box">
        <p style='font-size: 1.2em; margin-bottom: 1em;'>
            Enter your image search query below. Be as specific as possible for better results.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Search query input
    query = st.text_input("🔎 Search Query:", 
                         placeholder="e.g., vintage red sports car on mountain road",
                         help="Try to be specific about colors, styles, and context")

    # Search button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        search_button = st.button("🔍 Search and Analyze", type="primary", use_container_width=True)

    if search_button:
        if query:
            try:
                with st.spinner("🔄 Processing your query..."):
                    # Analyze query and fetch images
                    keywords, descriptions = analyzer.analyze_query(query, markdown_length)
                    image_urls = analyzer.fetch_google_images(query, num_images)
                    images = analyzer.download_images(image_urls)
                    
                    if not images:
                        st.error("❌ No images found for your query. Please try a different search term.")
                        return
                    
                    scores = analyzer.compute_scores(query, images)

                    # Display Analysis Section
                    st.markdown('<div class="markdown-content">', unsafe_allow_html=True)
                    
                    # Query Analysis
                    st.markdown("## 📝 Query Analysis")
                    st.markdown(f"**Original Query:** {query}")
                    
                    # Visual Elements
                    st.markdown("### 🔑 Key Visual Elements")
                    for kw in keywords:
                        st.markdown(f"- **{kw}**")
                    
                    # Descriptions
                    st.markdown("### 📋 Visual Descriptions")
                    for kw, desc in descriptions.items():
                        with st.expander(f"📍 {kw}"):
                            st.markdown(desc)
                    
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Image Display Section
                    st.markdown("## 🖼️ Best Matching Images")
                    st.markdown("Images are ranked by relevance to your query.")
                    
                    # Sort images by score
                    best_indices = scores.argsort()[-display_images:][::-1]
                    
                    # Create image grid
                    cols = st.columns(min(3, display_images))
                    for idx, img_idx in enumerate(best_indices):
                        col_idx = idx % 3
                        with cols[col_idx]:
                            st.image(images[img_idx], 
                                   caption=f"Relevance Score: {scores[img_idx]:.2f}",
                                   use_column_width=True)
                            st.markdown("---")

                    # Add download button for best image
                    best_img = images[best_indices[0]]
                    buf = BytesIO()
                    best_img.save(buf, format="PNG")
                    st.download_button(
                        label="📥 Download Best Match",
                        data=buf.getvalue(),
                        file_name="best_match.png",
                        mime="image/png"
                    )

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.markdown("Please try again with a different query or check your API keys.")
        else:
            st.warning("⚠️ Please enter a search query.")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Powered by CLIP, Gemini AI, and Google Image Search</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()