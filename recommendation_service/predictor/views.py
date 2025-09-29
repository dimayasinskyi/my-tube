from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd

from .constants import COUNTRY_MAPPING, FEATURE_COLUMNS, ALL_TAGS


@api_view(['POST'])
def create_recommendation(request):
    """
    Predicts whether a user will like a video from the provided data.

    Required data:
    - user_id: int
    - video_id: int
    - duration_watched: int
    - views: int
    - likes: int
    - tags: list
    - country: str

    Example request:
    {
    "user_id": 123,
    "video_id": 456,
    "duration_watched": 120,
    "views": 350,
    "likes": 25,
    "tags": ["sports", "music"],
    "country": "UA"
    }
    """ 
    df = pd.DataFrame(request.data)

    mlb = MultiLabelBinarizer(classes=ALL_TAGS)
    tags_encoded = mlb.fit_transform(df["tags"])
    tags_df = pd.DataFrame(tags_encoded, columns=[f"tag_{t}" for t in mlb.classes_])

    country_df = df["country"].map(COUNTRY_MAPPING)
    numerical_df = df[["user_id", "video_id", "duration_watched", "views", "likes"]]

    X = pd.concat([numerical_df, tags_df, country_df], axis=1)
            
    for col in FEATURE_COLUMNS:
        if col not in X.columns:
            X[col] = 0

    is_liked_by_user = settings.MODEL.predict(X[FEATURE_COLUMNS])

    df["is_liked_by_user"] = is_liked_by_user

    result = df.to_dict(orient="records")
    return Response(result)