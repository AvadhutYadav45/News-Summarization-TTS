from collections import Counter

def comparative_sentiment_analysis(processed_articles):
    """
    Analyzes sentiment distribution across multiple news articles 
    and identifies topic overlaps and differences.
    """
    sentiment_counts = Counter([article["Sentiment"] for article in processed_articles])
    
    # Ensure all sentiment categories exist in the output
    sentiment_distribution = {
        "Positive": sentiment_counts.get("Positive", 0),
        "Negative": sentiment_counts.get("Negative", 0),
        "Neutral": sentiment_counts.get("Neutral", 0),
    }

    # Extract article topics if available
    topic_sets = [set(article.get("Topics", [])) for article in processed_articles]
    common_topics = set.intersection(*topic_sets) if topic_sets else set()
    
    unique_topics = [
        {
            "Article": i + 1,
            "Unique Topics": list(topic_sets[i] - common_topics) if topic_sets else []
        }
        for i in range(len(topic_sets))
    ]

    # Compare sentiments in different articles
    coverage_differences = []
    for i in range(len(processed_articles) - 1):
        article_1 = processed_articles[i]
        article_2 = processed_articles[i + 1]

        coverage_differences.append({
            "Comparison": f"Article {i+1} discusses '{article_1['Title']}', while Article {i+2} focuses on '{article_2['Title']}'.",
            "Impact": f"Sentiment comparison: {article_1['Sentiment']} vs {article_2['Sentiment']}."
        })

    return {
        "Sentiment Distribution": sentiment_distribution,
        "Coverage Differences": coverage_differences,
        "Topic Overlap": {
            "Common Topics": list(common_topics),
            "Unique Topics Per Article": unique_topics
        }
    }
