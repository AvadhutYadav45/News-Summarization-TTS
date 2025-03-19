import requests
import random
from bs4 import BeautifulSoup
import json
import os
import certifi
from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Mock functions (replace with your actual implementations)
def process_articles(articles):
    """Mock sentiment analysis for articles."""
    sentiments = ["Positive", "Negative", "Neutral"]
    return [
        {
            "Title": article["Title"],
            "Sentiment": random.choice(sentiments),
            "Topics": ["Business", "Tech"] if "Tesla" in article["Title"] else ["General"]
        }
        for article in articles
    ]

def text_to_speech(text, filename):
    """Mock TTS function."""
    return filename  # Pretend it generates an audio file

# Fixed comparative_sentiment_analysis from your earlier submission
def comparative_sentiment_analysis(processed_articles):
    """
    Analyzes sentiment distribution across multiple news articles 
    and identifies topic overlaps and differences.
    """
    if not processed_articles:
        return {
            "Sentiment Distribution": {"Positive": 0, "Negative": 0, "Neutral": 0},
            "Coverage Differences": [],
            "Topic Overlap": {"Common Topics": [], "Unique Topics Per Article": []},
            "Error": "No articles provided for analysis"
        }

    try:
        sentiment_counts = Counter([article.get("Sentiment", "Unknown") for article in processed_articles])
    except Exception as e:
        sentiment_counts = Counter()

    sentiment_distribution = {
        "Positive": sentiment_counts.get("Positive", 0),
        "Negative": sentiment_counts.get("Negative", 0),
        "Neutral": sentiment_counts.get("Neutral", 0),
        "Unknown": sentiment_counts.get("Unknown", 0)
    }

    topic_sets = [set(article.get("Topics", [])) for article in processed_articles]
    common_topics = set.intersection(*topic_sets) if topic_sets and all(topic_sets) else set()

    unique_topics = [
        {
            "Article": i + 1,
            "Unique Topics": list(topic_sets[i] - common_topics) if topic_sets[i] else []
        }
        for i in range(len(topic_sets))
    ]

    coverage_differences = []
    if len(processed_articles) > 1:
        for i in range(len(processed_articles) - 1):
            article_1 = processed_articles[i]
            article_2 = processed_articles[i + 1]
            title_1 = article_1.get("Title", "Untitled")
            title_2 = article_2.get("Title", "Untitled")
            sentiment_1 = article_1.get("Sentiment", "Unknown")
            sentiment_2 = article_2.get("Sentiment", "Unknown")
            coverage_differences.append({
                "Comparison": f"Article {i+1} discusses '{title_1}', while Article {i+2} focuses on '{title_2}'.",
                "Impact": f"Sentiment comparison: {sentiment_1} vs {sentiment_2}."
            })

    return {
        "Sentiment Distribution": sentiment_distribution,
        "Coverage Differences": coverage_differences,
        "Topic Overlap": {
            "Common Topics": list(common_topics),
            "Unique Topics Per Article": unique_topics
        }
    }

# Fixed function to fetch news articles with Selenium
def fetch_news(company_name):
    """
    Scrapes Google News search results for the given company using Oxylabs Web Unblocker and Selenium.
    """
    search_url = f"https://www.google.com/search?q={company_name}+news&hl=en&gl=US&tbm=nws&tbs=qdr:w"
    USERNAME = os.environ.get('OXYLABS_USERNAME')
    PASSWORD = os.environ.get('OXYLABS_PASSWORD')

    if not USERNAME or not PASSWORD:
        return {"error": "Oxylabs credentials not found in environment variables."}

    proxies = {
        'http': f'http://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
        'https': f'https://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
    }

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f'--proxy-server={proxies["http"][7:]}')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36")
        chrome_options.add_argument('--ignore-certificate-errors')

        service = Service('./chromedriver')  # Replace with your chromedriver path
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(search_url)

        html_content = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html_content, "html.parser")
        articles = []

        for item in soup.find_all("div", class_="Gx5Zad fP1Qef xpd EtOod pkphOe"):
            try:
                title_element = item.find("h3")
                title = title_element.text.strip() if title_element else "No Title"

                source_element = item.find("div", class_="CEMjEf NUnG9d")
                source = source_element.text.strip() if source_element else "No Source"

                time_element = item.find("span", class_="WG9SHc")
                time = time_element.text.strip() if time_element else "No Time"

                link_element = item.find("a")
                link = "https://www.google.com" + link_element["href"] if link_element and link_element.has_attr('href') else "No Link"

                articles.append({
                    "Title": title,
                    "Source": source,
                    "Time": time,
                    "Link": link,
                })
            except Exception as e:
                print(f"Error parsing article: {e}")

        return articles if articles else {"error": "No articles found"}

    except Exception as e:
        return {"error": str(e)}

# Fixed function to process news and generate summary
def generate_news_summary(company_name):
    """
    Fetches news, processes sentiment, performs analysis, and generates Hindi TTS.
    """
    articles = fetch_news(company_name)
    if "error" in articles:
        return articles

    processed_articles = process_articles(articles)
    sentiment_summary = comparative_sentiment_analysis(processed_articles)

    final_summary = f"{company_name} की खबरें मिली हैं। सकारात्मक: {sentiment_summary['Sentiment Distribution']['Positive']}, नकारात्मक: {sentiment_summary['Sentiment Distribution']['Negative']}।"
    audio_file = text_to_speech(final_summary, "news_summary.mp3")

    output_json = {
        "Company": company_name,
        "Articles": processed_articles,
        "Comparative Sentiment Score": sentiment_summary,
        "Final Sentiment Analysis": final_summary,
        "Audio": audio_file
    }
    return output_json

# Run the script
if __name__ == "__main__":
    company = input("Enter company name: ")
    result = generate_news_summary(company)
    print(json.dumps(result, ensure_ascii=False, indent=4))