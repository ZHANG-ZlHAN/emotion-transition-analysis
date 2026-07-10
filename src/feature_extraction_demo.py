import os
import re
from collections import defaultdict
from datetime import timedelta

import pandas as pd


EMOTION_KEYWORDS = {
    "friends": ["friend", "friends"],
    "giving": ["give", "gave", "support", "help", "helped"],
    "optimism": ["optimism", "hope", "better"],
    "healing": ["healing", "recover", "recovered"],
    "love": ["love"],
    "fun": ["fun"],
    "work": ["work"],
    "emotional": ["emotional"],
    "pain": ["pain"],
    "sadness": ["sadness", "sad"],
    "nervousness": ["nervous", "nervousness"],
    "shame": ["shame"],
    "death": ["death"],
    "violence": ["violence"],
    "dispute": ["dispute"],
}


CATEGORY_MAPPING = {
    "friends": "Positive",
    "giving": "Positive",
    "optimism": "Positive",
    "healing": "Positive",
    "love": "Positive",
    "fun": "Positive",

    "work": "Neutral",
    "emotional": "Neutral",

    "pain": "Negative",
    "sadness": "Negative",
    "nervousness": "Negative",
    "shame": "Negative",
    "death": "Negative",
    "violence": "Negative",
    "dispute": "Negative",
}


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def score_window_text(text):
    text = clean_text(text)
    scores = defaultdict(int)

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            pattern = rf"\b{re.escape(keyword)}\b"
            scores[emotion] += len(re.findall(pattern, text))

    return dict(scores)


def format_emotional_characteristics(scores):
    positive_scores = {k: v for k, v in scores.items() if v > 0}

    if not positive_scores:
        return "silence", "silence", "silence"

    max_score = max(positive_scores.values())

    normalized = {
        emotion: count / max_score
        for emotion, count in positive_scores.items()
    }

    sorted_features = sorted(
        normalized.items(),
        key=lambda x: x[1],
        reverse=True
    )

    emotional_characteristics = ", ".join(
        f"{emotion}: {score:.2f}"
        for emotion, score in sorted_features
    )

    first_emotion = sorted_features[0][0]
    category = CATEGORY_MAPPING.get(first_emotion, "Unknown")

    return emotional_characteristics, first_emotion, category


def find_most_active_15_days(user_df):
    dates = sorted(user_df["created_at"].dt.date.unique())

    best_start = dates[0]
    best_count = -1

    for date in dates:
        start = pd.Timestamp(date)
        end = start + timedelta(days=14)

        count = user_df[
            (user_df["created_at"] >= start)
            & (user_df["created_at"] <= end)
        ].shape[0]

        if count > best_count:
            best_count = count
            best_start = start

    return best_start


def extract_window_features(input_file, output_file):
    df = pd.read_csv(input_file)
    df["created_at"] = pd.to_datetime(df["created_at"])

    results = []

    for user_id, user_df in df.groupby("user_id"):
        user_df = user_df.sort_values("created_at")
        start_date = find_most_active_15_days(user_df)

        for i in range(5):
            window_start = start_date + timedelta(days=i * 3)
            window_end = window_start + timedelta(days=2)

            window_df = user_df[
                (user_df["created_at"] >= window_start)
                & (user_df["created_at"] <= window_end)
            ]

            combined_text = " ".join(window_df["text"].astype(str).tolist())
            scores = score_window_text(combined_text)

            (
                emotional_characteristics,
                first_emotion,
                category,
            ) = format_emotional_characteristics(scores)

            results.append({
                "user_id": user_id,
                "window": f"W{i + 1}",
                "window_start_date": window_start.strftime("%Y-%m-%d"),
                "emotional_characteristics": emotional_characteristics,
                "first_emotion": first_emotion,
                "category": category,
            })

    output_df = pd.DataFrame(results)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    output_df.to_csv(output_file, index=False)

    return output_df


def main():
    input_file = "sample_data/sample_posts.csv"
    output_file = "results/extracted_window_features_demo.csv"

    output_df = extract_window_features(input_file, output_file)

    print("Extracted window-level emotion features:")
    print(output_df.to_string(index=False))
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
