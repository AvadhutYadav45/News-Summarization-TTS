from textblob import TextBlob

def analyze_sentiment(text):
    """
    Determines the sentiment of the given text using TextBlob.
    Returns: "Positive", "Negative", or "Neutral"
    """
    if not text:
        return "Neutral"

    sentiment_score = TextBlob(text).sentiment.polarity
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

def process_articles(articles):
    """
    Processes a list of articles, extracting titles and summaries, 
    then performs sentiment analysis on each.
    """
    processed_articles = []
    
    for article in articles:
        title = article.get("Title", "No Title")
        summary = article.get("Summary", title)  # Use title if summary is unavailable
        sentiment = analyze_sentiment(summary)

        processed_articles.append({
            "Title": title,
            "Summary": summary,
            "Sentiment": sentiment
        })

    return processed_articles
