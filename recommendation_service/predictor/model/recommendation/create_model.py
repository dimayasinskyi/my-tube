import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump
import ast

from ...constants import COUNTRY_MAPPING, FEATURE_COLUMNS, ALL_TAGS


df = pd.read_csv("start_data.csv")

# preparation
df["tags"] = df["tags"].apply(ast.literal_eval)
y = df["is_finished"]
mlb = MultiLabelBinarizer(classes=ALL_TAGS)
tags_encoded = mlb.fit_transform(df["tags"])
tags_df = pd.DataFrame(tags_encoded, columns=[f"tag_{t}" for t in mlb.classes_])

country_df = df["country"].map(COUNTRY_MAPPING)
numerical_df = df[["user_id", "video_id", "duration_watched", "views", "likes"]]

X = pd.concat([numerical_df, tags_df, country_df], axis=1)
X = X[FEATURE_COLUMNS]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model creation
mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation="relu",
    solver="adam",
    max_iter=50,
    random_state=42,
)

mlp.fit(X_train, y_train)
y_pred = mlp.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# save
dump(mlp, "recommendation_model.joblib")