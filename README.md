# new-aggrigator
# News Aggregator with Sentiment & Entity Analysis

## Overview
This is a Streamlit-powered web application that aggregates news articles based on a search query. It performs Named Entity Recognition (NER) using spaCy and sentiment analysis using VADER to provide real-time insights into news trends. The application also features a modern UI design with custom styling.

## Features
- Fetches news articles from NewsAPI
- Performs Named Entity Recognition (NER) to identify people, organizations, and locations
- Analyzes sentiment (Positive, Neutral, Negative) using VADER Sentiment Analyzer
- Displays results with a user-friendly UI styled in a gray, black, white, and blue theme
- Interactive sidebar for inputting search queries
- Uses caching to optimize API calls and improve performance

## Technologies Used
- **Streamlit**: For building the web application
- **spaCy**: For Named Entity Recognition (NER)
- **VADER Sentiment Analyzer**: For sentiment analysis
- **NewsAPI**: For fetching news articles
- **Pandas**: For handling data
- **Altair**: For data visualization
- **Custom CSS**: For enhanced UI styling

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/news-aggregator.git
   cd news-aggregator
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Replace `api_key` in the code with your **NewsAPI key**.

## Usage
1. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```
2. Enter a search query in the sidebar (e.g., "Elon Musk") and select the number of articles to analyze.
3. Click "Analyze" to fetch and analyze the articles.
4. View the extracted entities, sentiment analysis, and news summaries in the main interface.

## API Key Setup
- Obtain a free API key from [NewsAPI](https://newsapi.org/).
- Replace the placeholder in the code with your actual API key:
  ```python
  newsapi = NewsApiClient(api_key="your_api_key_here")
  ```

## Notes
- The app uses **caching** (`@st.cache_data`) to store API responses and avoid redundant requests.
- If no articles are found, an error message will be displayed.
- Streamlit styling has been enhanced using **custom CSS** for a better user experience.

## Future Improvements
- Add support for multilingual news articles
- Implement a more advanced sentiment analysis model
- Improve UI with more interactive elements and charts

## License
This project is open-source and available under the [MIT License](LICENSE).

---
### Contributors
- **Subash Kumar Yadav** (github.com/subash-0)

Feel free to fork and contribute to the project!

