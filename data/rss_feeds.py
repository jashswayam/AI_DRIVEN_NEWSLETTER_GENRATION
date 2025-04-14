def get_rss_feeds():
    """Return categorized RSS feeds"""
    return {
        "General News": [
            "http://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "http://feeds.reuters.com/reuters/topNews"
        ],
        "Technology": [
            "https://techcrunch.com/feed/",
            "https://www.wired.com/feed/rss",
            "https://www.technologyreview.com/feed/"
        ],
        "Finance": [
            "https://www.bloomberg.com/feed/podcast/etf-report",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "https://www.ft.com/rss/home"
        ],
        "Sports": [
            "https://www.espn.com/espn/rss/news",
            "http://feeds.bbci.co.uk/sport/rss.xml",
            "https://www.skysports.com/rss/12040"
        ],
        "Entertainment": [
            "https://variety.com/feed/",
            "https://www.hollywoodreporter.com/feed/",
            "https://www.billboard.com/feed/"
        ],
        "Science": [
            "https://www.nasa.gov/rss/dyn/breaking_news.rss",
            "https://www.sciencedaily.com/rss/all.xml",
            "https://arstechnica.com/science/feed/"
        ]
    }
