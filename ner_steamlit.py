import streamlit as st
import spacy
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import altair as alt

# Initialize tools
nlp = spacy.load("en_core_web_sm")
newsapi = NewsApiClient(api_key="c6f18ae314ed4cee848e8a7731afaffc")  # Replace with your NewsAPI key
sid = SentimentIntensityAnalyzer()

# Custom CSS for gray, black, white, and blue design
st.markdown("""
    <style>
    /* Global Styles */
    .main {
        background-color: #111827;  /* Darker background for better contrast */
        padding: 20px;
        border-radius: 12px;
        color: #f9fafb;  /* Brighter white for better readability */
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    
    /* Typography */
    .title {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        color: #f9fafb;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: -0.025em;
    }
    
    .subtitle {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        color: #9ca3af;  /* Softer gray for subtitle */
        font-size: 16px;
        margin-bottom: 24px;
        font-weight: 400;
        letter-spacing: -0.01em;
    }
    
    /* Cards and Containers */
    .entity-box {
        background-color: #1f2937;  /* Slightly lighter than main background */
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        color: #f9fafb;
        font-size: 18px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .entity-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .sentiment-box {
        background-color: #1f2937;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        color: #f9fafb;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .sentiment-box h3 {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 12px;
        color: #f9fafb;
    }
    
    .article-card {
        background-color: #1f2937;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        color: #f9fafb;
        margin-bottom: 16px;
        font-size: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .article-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .article-card a {
        color: #60a5fa;  /* Lighter blue for better contrast */
        text-decoration: none;
        font-weight: 500;
        transition: color 0.15s ease;
    }
    
    .article-card a:hover {
        color: #93c5fd;  /* Even lighter blue on hover */
        text-decoration: underline;
    }
    
    /* Streamlit Component Styling */
    .stButton>button {
        background-color: #3b82f6;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 15px;
        font-weight: 500;
        border: none;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5);
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 6px 10px -1px rgba(37, 99, 235, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    .stSidebar {
        background-color: #111827;
        padding: 20px;
        color: #f9fafb;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stSidebar .stMarkdown h3 {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 16px;
        color: #f9fafb;
    }
    
    .stTextInput>div>div {
        background-color: #1f2937 !important;
    }
    
    .stTextInput input {
        background-color: #1f2937;
        color: #f9fafb;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 15px;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
    }
    
    .stSlider .st-bd {
        background-color: #3b82f6;
    }
    
    .stSlider .st-ev {
        background-color: #60a5fa;
    }
    
    /* Data visualization elements */
    .stDataFrame {
        background-color: #1f2937;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stDataFrame th {
        background-color: #374151;
        color: #f9fafb;
        font-weight: 600;
        padding: 10px;
    }
    
    .stDataFrame td {
        color: #f9fafb;
        padding: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Entity list styling */
    .entity-box ul {
        list-style-type: none;
        padding: 0;
        margin: 8px 0 0 0;
    }
    
    .entity-box li {
        padding: 6px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .entity-box li:last-child {
        border-bottom: none;
    }
    
    /* Sentiment indicators */
    .sentiment-positive {
        color: #34d399;
        font-weight: 600;
    }
    
    .sentiment-neutral {
        color: #9ca3af;
        font-weight: 600;
    }
    
    .sentiment-negative {
        color: #f87171;
        font-weight: 600;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Function to fetch news articles
@st.cache_data
def fetch_articles(query, max_articles=10):
    try:
        response = newsapi.get_everything(q=query, language="en", page_size=max_articles)
        articles = response["articles"]
        return [
            {"title": article["title"], "description": article["description"], "url": article["url"]}
            for article in articles
        ]
    except Exception as e:
        st.error(f"Error fetching articles: {e}")
        return []

# Function to extract entities and sentiment
def analyze_text(text):
    doc = nlp(text)
    entities = {"PERSON": [], "ORGANIZATION": [], "LOCATION": []}
    label_mapping = {"PERSON": "PERSON", "ORG": "ORGANIZATION", "GPE": "LOCATION", "LOC": "LOCATION"}
    
    for ent in doc.ents:
        mapped_label = label_mapping.get(ent.label_, "MISC")
        if mapped_label in entities:
            entities[mapped_label].append(ent.text)
    
    sentiment = sid.polarity_scores(text)
    if sentiment["compound"] >= 0.05:
        sentiment_label = "Positive"
    elif sentiment["compound"] <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    
    return entities, sentiment_label

# Main Streamlit app
def main():
    # Header
    st.markdown('<h1 class="title">📰 News Aggregator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Real-time insights with sentiment & entities</p>', unsafe_allow_html=True)

    # Sidebar for inputs
    with st.sidebar:
        st.markdown("### 🔍 Search")
        query = st.text_input("", "Elon Musk", placeholder="Topic or Name", label_visibility="collapsed")
        max_articles = st.slider("", 5, 20, 10, label_visibility="collapsed")
        if st.button("Analyze", use_container_width=True):
            st.session_state["fetch"] = True
        else:
            st.session_state["fetch"] = False

    # Main content
    if st.session_state.get("fetch", False):
        with st.spinner("Analyzing news..."):
            articles = fetch_articles(query, max_articles)
            
            if not articles:
                st.warning("No articles found.")
                return
            
            # Process articles
            results = {"PERSON": [], "ORGANIZATION": [], "LOCATION": [], "Sentiments": []}
            article_data = []
            
            for article in articles:
                text = f"{article['title']}. {article['description']}"
                entities, sentiment = analyze_text(text)
                for entity_type in ["PERSON", "ORGANIZATION", "LOCATION"]:
                    results[entity_type].extend(entities[entity_type])
                results["Sentiments"].append(sentiment)
                article_data.append({
                    "Title": article["title"],
                    "Sentiment": sentiment,
                    "URL": article["url"]
                })
            
            # Summary Section
            st.markdown(f"#### 📊 Results for '{query}' ({len(articles)} articles)")
            
            # Entities in columns
            col1, col2, col3 = st.columns(3)
            for entity_type, col in zip(["PERSON", "ORGANIZATION", "LOCATION"], [col1, col2, col3]):
                unique_entities = sorted(set(results[entity_type]))
                with col:
                    st.markdown(f'<div class="entity-box"><b>{entity_type}</b> ({len(unique_entities)})</div>', unsafe_allow_html=True)
                    if unique_entities:
                        st.markdown('<div class="entity-box">' + "<br>".join([f"• {e}" for e in unique_entities[:5]]) + '</div>', unsafe_allow_html=True)
                        if len(unique_entities) > 5:
                            st.markdown('<div class="entity-box">+ more</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="entity-box">None</div>', unsafe_allow_html=True)

            # Sentiment Distribution
            st.markdown('<h3 class="sentiment-box">Sentiment</h3>', unsafe_allow_html=True)
            sentiment_counts = pd.Series(results["Sentiments"]).value_counts()
            sentiment_df = pd.DataFrame({
                "Sentiment": sentiment_counts.index,
                "Percentage": (sentiment_counts / len(articles) * 100).round(1)
            })
            
            colors = {"Positive": "#2ecc71", "Neutral": "#d1d5db", "Negative": "#ef4444"}  # Adjusted for theme
            chart = alt.Chart(sentiment_df).mark_bar().encode(
                x=alt.X("Sentiment", title=None),
                y=alt.Y("Percentage", title="%", axis=alt.Axis(grid=False)),
                color=alt.Color("Sentiment", scale=alt.Scale(domain=list(colors.keys()), range=list(colors.values())), legend=None)
            ).properties(
                width=alt.Step(40),
                height=200
            ).configure_view(strokeWidth=0).configure_axis(labelColor="#ffffff")
            st.altair_chart(chart, use_container_width=True)
            st.dataframe(sentiment_df.style.hide(axis="index").format({"Percentage": "{:.1f}%"}))

            # Articles Section
            st.markdown("#### 📰 Top Articles")
            for i, article in enumerate(article_data[:5], 1):
                sentiment_color = {"Positive": "#2ecc71", "Neutral": "#d1d5db", "Negative": "#ef4444"}
                st.markdown(
                    f'<div class="article-card"><span style="color:{sentiment_color[article["Sentiment"]]}"><b>{article["Sentiment"][0]}</b></span> <a href="{article["URL"]}">{article["Title"]}</a></div>',
                    unsafe_allow_html=True
                )
            if len(article_data) > 5:
                st.markdown(f'<div class="article-card">+ {len(article_data) - 5} more articles</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()