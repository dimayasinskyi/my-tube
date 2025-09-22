FEATURE_COLUMNS = [
    "user_id", "video_id", "duration_watched", "views", "likes",
    'tag_music', 'tag_sports', 'tag_gaming', 'tag_education', 'tag_comedy', 
    'tag_news', 'tag_technology', 'tag_movies', 'tag_cooking', 'tag_travel',
    "country"
]

COUNTRY_MAPPING = {
    "UA": 0,  # Ukraine
    "US": 1,  # United States
    "UK": 2,  # United Kingdom
    "DE": 3,  # Germany
    "FR": 4,  # France
    "ES": 5,  # Spain
    "IT": 6,  # Italy
    "PL": 7,  # Poland
    "CN": 8,  # China
    "JP": 9,  # Japan
    "KR": 10, # South Korea
    "BR": 11, # Brazil
    "CA": 12, # Canada
    "AU": 13  # Australia
}

ALL_TAGS = ['music', 'sports', 'gaming', 'education', 'comedy', 'news', 'technology', 'movies', 'cooking', 'travel']