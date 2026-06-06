import pandas as pd

# Load datasets
listening_logs = pd.read_csv("listening_logs.csv")
songs_metadata = pd.read_csv("songs_metadata.csv")

joined = listening_logs.merge(songs_metadata, on="song_id")

import os
os.makedirs("outputs", exist_ok=True)

# Task 1: User Favorite Genres
genre_counts = joined.groupby(["user_id", "genre"]).size().reset_index(name="listen_count")
favorite_genres = genre_counts.sort_values("listen_count", ascending=False) \
    .drop_duplicates(subset="user_id") \
    .sort_values("user_id")

favorite_genres.to_csv("outputs/task1_user_favorite_genres.csv", index=False)
print("Task 1 — User Favorite Genres:")
print(favorite_genres.head(10))

# Task 2: Average Listen Time
avg_listen_time = listening_logs.groupby("user_id")["duration_sec"] \
    .mean().round(2).reset_index(name="avg_duration_sec") \
    .sort_values("user_id")

avg_listen_time.to_csv("outputs/task2_avg_listen_time.csv", index=False)
print("\nTask 2 — Average Listen Time per User:")
print(avg_listen_time.head(10))

# Task 3: Genre Loyalty Scores - Top 10
total_listens = listening_logs.groupby("user_id").size().reset_index(name="total_listens")
top_genre = genre_counts.sort_values("listen_count", ascending=False) \
    .drop_duplicates(subset="user_id")[["user_id", "listen_count"]] \
    .rename(columns={"listen_count": "top_genre_count"})

loyalty_scores = top_genre.merge(total_listens, on="user_id")
loyalty_scores["loyalty_score"] = (loyalty_scores["top_genre_count"] / loyalty_scores["total_listens"] * 100).round(2)
loyalty_scores = loyalty_scores.sort_values("loyalty_score", ascending=False).head(10)[["user_id", "loyalty_score"]]

loyalty_scores.to_csv("outputs/task3_genre_loyalty_top10.csv", index=False)
print("\nTask 3 — Genre Loyalty Scores (Top 10):")
print(loyalty_scores)

# Task 4: Night Owl Users (12 AM - 5 AM)
listening_logs["timestamp"] = pd.to_datetime(listening_logs["timestamp"])
night_owl_users = listening_logs[listening_logs["timestamp"].dt.hour < 5] \
    .sort_values("user_id")[["user_id", "song_id", "timestamp", "duration_sec"]]

night_owl_users.to_csv("outputs/task4_night_owl_users.csv", index=False)
print("\nTask 4 — Night Owl Users (12 AM - 5 AM):")
print(night_owl_users.head(10))