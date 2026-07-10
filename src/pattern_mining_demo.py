import os
import pandas as pd


def load_window_features(file_path):
    """
    Load window-level emotional feature data.

    Expected columns:
    - user_id
    - window
    - first_emotion
    - category
    """
    df = pd.read_csv(file_path)

    required_columns = {"user_id", "window", "first_emotion", "category"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["window_index"] = (
        df["window"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(int)
    )

    return df


def build_user_sequences(df):
    """
    Build one five-step emotional sequence for each user.
    """
    user_sequences = []

    for user_id, user_df in df.groupby("user_id"):
        user_df = user_df.sort_values("window_index")

        if len(user_df) != 5:
            continue

        emotion_sequence = user_df["first_emotion"].tolist()
        category_sequence = user_df["category"].tolist()

        user_sequences.append({
            "user_id": user_id,
            "emotion_sequence": emotion_sequence,
            "category_sequence": category_sequence,
        })

    return user_sequences


def mine_full_length_patterns(user_sequences):
    """
    Mine full five-window sequential patterns.

    This simplified demo mines full-length patterns only.
    The original research also explored different pattern lengths
    and used the mined patterns for PIS-based prediction.
    """
    pattern_counts = {}

    for item in user_sequences:
        emotion_pattern = tuple(item["emotion_sequence"])
        category_pattern = tuple(item["category_sequence"])

        key = (emotion_pattern, category_pattern)
        pattern_counts[key] = pattern_counts.get(key, 0) + 1

    total_sequences = len(user_sequences)

    first_emotion_counts = {}
    prefix_counts = {}

    for (emotion_pattern, _), count in pattern_counts.items():
        first_emotion = emotion_pattern[0]
        prefix = emotion_pattern[:-1]

        first_emotion_counts[first_emotion] = (
            first_emotion_counts.get(first_emotion, 0) + count
        )

        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + count

    results = []

    for (emotion_pattern, category_pattern), count in pattern_counts.items():
        first_emotion = emotion_pattern[0]
        prefix = emotion_pattern[:-1]

        support = count / total_sequences
        confidence = count / first_emotion_counts[first_emotion]
        sequential_confidence = count / prefix_counts[prefix]

        results.append({
            "Sequential Pattern": " -> ".join(emotion_pattern),
            "Category Pattern": " -> ".join(category_pattern),
            "Support": round(support, 4),
            "Confidence": round(confidence, 4),
            "Sequential Confidence": round(sequential_confidence, 4),
            "Count": count,
        })

    output_df = pd.DataFrame(results)
    output_df = output_df.sort_values(
        by=["Count", "Support"],
        ascending=False
    )

    return output_df


def main():
    # This demo uses prepared window-level feature samples.
    # The feature extraction demo output is provided separately as another modular example.
    input_file = "sample_data/sample_window_features.csv"
    output_file = "results/generated_patterns_demo.csv"

    df = load_window_features(input_file)
    user_sequences = build_user_sequences(df)
    output_df = mine_full_length_patterns(user_sequences)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    output_df.to_csv(output_file, index=False)

    print("Generated sequential patterns:")
    print(output_df.to_string(index=False))
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
