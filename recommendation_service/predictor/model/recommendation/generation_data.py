import pandas as pd
import random
from faker import Faker

from ...constants import COUNTRY_MAPPING, ALL_TAGS


fake = Faker()

# Parameters
num_users = 50
num_videos = 100
num_records = 200
tags_list = ALL_TAGS
countries = COUNTRY_MAPPING
age_limits = ['G', 'PG13', 'PG15', 'NC17']

# Generate videos
videos = []
for vid in range(num_videos):
    videos.append({
        'video_id': vid,
        'tags': random.sample(tags_list, k=random.randint(1,3)),
        'views': random.randint(0, 50000),
        'likes': random.randint(-50, 10000),
        'age_limit': random.choice(age_limits)
    })

videos_df = pd.DataFrame(videos)

# Generating viewing history
history = []
for _ in range(num_records):
    user_id = random.randint(0, num_users-1)
    video_id = random.randint(0, num_videos-1)
    
    watched_at = fake.date_time_between(start_date='-1y', end_date='now')
    duration_watched = random.randint(10, 3600) 
    is_finished = duration_watched > 0.8 * 3600 
    country = random.choice(countries)
    
    history.append({
        'user_id': user_id,
        'video_id': video_id,
        'watched_at': watched_at,
        'duration_watched': duration_watched,
        'is_finished': is_finished,
        'country': country,
        'tags': videos_df.loc[video_id, 'tags'],
        'views': videos_df.loc[video_id, 'views'],
        'likes': videos_df.loc[video_id, 'likes'],
        'age_limit': videos_df.loc[video_id, 'age_limit']
    })

history_df = pd.DataFrame(history)

print(history_df)
history_df.to_csv("start_data.csv", index=False)
