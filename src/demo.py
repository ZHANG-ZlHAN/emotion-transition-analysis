import pandas as pd
from collections import defaultdict


def load_patterns(file_path):
    """
    Load sequential pattern data from a CSV file.

    Expected columns:
    - Sequential Pattern
    - Category Pattern
    - Support
    - Confidence
    - Sequential Confidence
    - Count
    """
    df = pd.read_csv(file_path)

    patterns = []
    for _, row in df.iterrows():
        sequence = [x.strip() for x in row["Sequential Pattern"].split("->")]
        category_sequence = [x.strip() for x in row["Category Pattern"].split("->")]

        patterns.append({
            "sequence": sequence,
            "category_sequence": category_sequence,
            "support": float(row["Support"]),
            "confidence": float(row["Confidence"]),
            "sequential_confidence": float(row["Sequential Confidence"]),
            "count": int(row["Count"]),
        })

    return patterns


def predict_next_emotions(current_sequence, patterns, top_k=3):
    """
    Predict possible next emotions based on prefix matching.

    If a pattern starts with the current sequence, the following emotion
    is treated as a candidate prediction.
    """
    candidate_scores = defaultdict(float)

    for pattern in patterns:
        sequence = pattern["sequence"]

        if len(sequence) <= len(current_sequence):
            continue

        prefix = sequence[:len(current_sequence)]

        if prefix == current_sequence:
            next_emotion = sequence[len(current_sequence)]

            # Simplified scoring for portfolio demo:
            # combine support, confidence, sequential confidence, and count.
            score = (
                pattern["support"] * 0.4
                + pattern["confidence"] * 0.3
                + pattern["sequential_confidence"] * 0.2
                + min(pattern["count"] / 100, 1.0) * 0.1
            )

            candidate_scores[next_emotion] += score

    ranked_predictions = sorted(
        candidate_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_predictions[:top_k]


def main():
    pattern_file = "sample_data/sample_patterns.csv"

    patterns = load_patterns(pattern_file)

    # Example input:
    # The model predicts the next emotion after these four emotional states.
    current_sequence = ["friends", "work", "pain", "death"]

    predictions = predict_next_emotions(current_sequence, patterns, top_k=3)

    print("Current emotion sequence:")
    print(" -> ".join(current_sequence))

    print("\nPredicted next emotions:")
    if predictions:
        for rank, (emotion, score) in enumerate(predictions, start=1):
            print(f"Top {rank}: {emotion} | score = {score:.4f}")
    else:
        print("No matching pattern found.")


if __name__ == "__main__":
    main()
