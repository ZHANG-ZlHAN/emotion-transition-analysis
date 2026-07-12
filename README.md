# Social Media Emotion Transition Analysis and Prediction

This repository is a portfolio version of my master's research project:

**Exploring Emotional Transitions on Social Media Through Sequential Pattern Mining**

The project analyzes emotional transitions in Reddit user posts and predicts future emotional states using sequential pattern mining and an interpretable Pattern Intensity Set (PIS)-based prediction method.

---


[日本語版 README](README_ja.md)

## Overview

Social media platforms contain large amounts of user-generated text that reflect emotional and psychological states over time. This project studies how emotions change across time windows and how frequent emotional transition patterns can be used to predict future emotional tendencies.

The original research used large-scale Reddit data from 2018 to 2022. Users were categorized into four cohorts:

- Depressive users
- Normal users
- Recovering users
- Deteriorating users

For each user, the most active 15-day period was selected and divided into five consecutive 3-day windows. Emotional features were extracted from each window, and sequential pattern mining was applied to discover frequent emotional transition patterns.

These patterns were then aggregated into a Pattern Intensity Set (PIS), which was used to predict future emotional states through interpretable pattern matching and scoring.

---

## Technologies

- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- Plotly
- Sequential Pattern Mining
- Pattern Intensity Set (PIS)
- Top-k prediction
- Sankey diagram visualization

Original research also used:

- Reddit data from Academic Torrents / Pushshift archive
- Empath-based emotion feature extraction
- Emoji normalization
- Text preprocessing with NLTK

---

## My Role

This was my master's research project. I was responsible for:

- Collecting and processing Reddit post data
- Designing user cohort filtering logic
- Selecting each user's most active 15-day period
- Dividing user activity into five 3-day windows
- Extracting emotional features from text
- Constructing emotional sequences
- Mining sequential emotional transition patterns
- Designing a PIS-based prediction algorithm
- Evaluating Top-1, Top-3, and Top-5 prediction accuracy
- Visualizing emotional transition flows with Sankey diagrams

---

## Research Workflow

The original research workflow consisted of the following stages:

1. **Data Collection**
   - Reddit posts from 2018 to 2022 were collected from archived `.zst` files.

2. **User Cohort Identification**
   - Users were categorized into depressive, normal, recovering, and deteriorating groups.

3. **Data Filtering and Preprocessing**
   - Deleted users and invalid posts were removed.
   - Users with fewer than 15 active posting days were excluded.
   - Text was cleaned and normalized.

4. **Active Period Selection**
   - For each user, the most active 15-day period was identified.

5. **Window Segmentation**
   - The 15-day period was divided into five consecutive 3-day windows.

6. **Emotion Feature Extraction**
   - Emotional features were extracted for each window.
   - Each user was represented as a 5-step emotional sequence.

7. **Sequential Pattern Mining**
   - Frequent emotional transition patterns were mined.
   - Support, confidence, sequential confidence, and count were calculated.

8. **PIS Construction and Prediction**
   - Mined patterns were aggregated into a Pattern Intensity Set.
   - Recent emotional subsequences were matched against PIS patterns.
   - Future emotional states were predicted using a scoring-based Top-k method.

---

## Key Concepts

### 1. Five-Window Emotional Sequence

Each user's most active 15-day period was divided into five windows:

```text
W1 -> W2 -> W3 -> W4 -> W5
```

Each window represents a 3-day period.

Example:

```text
friends -> work -> pain -> death -> healing
```

### 2. Sequential Pattern

A sequential pattern represents a common emotional transition path.

Example:

```text
friends -> work -> pain -> death -> healing
```

### 3. Support

Support measures how frequently a pattern appears among all sequences.

```text
Support(P) = Count(P) / Total number of sequences
```

### 4. Confidence

Confidence measures how likely a pattern appears given the first emotion.

```text
Confidence(P) = Count(P) / Count(patterns starting with the same first emotion)
```

### 5. Sequential Confidence

Sequential confidence measures how likely the final emotion follows a specific prefix sequence.

```text
Sequential Confidence(P) = Count(P) / Count(patterns with the same prefix)
```

### 6. Pattern Intensity Set (PIS)

The Pattern Intensity Set stores mined emotional transition patterns together with their statistical metrics:

- Sequential Pattern
- Category Pattern
- Support
- Confidence
- Sequential Confidence
- Count

The PIS is used as the basis for future emotion prediction.

---

## Simplified Demo Design

This repository provides a simplified and runnable version of the research workflow.

The full research pipeline used large-scale Reddit data and Empath-based feature extraction. Since the original dataset is large and not suitable for public release, this repository uses small artificial sample data to demonstrate the core logic.

The repository includes three modular demos:

```text
sample posts
↓
feature_extraction_demo.py
↓
window-level emotional features
```

```text
window-level emotional features
↓
pattern_mining_demo.py
↓
sequential patterns
```

```text
sequential pattern data
↓
demo.py
↓
Top-k next emotion prediction
```

Together, these demos cover the main logic of the research workflow:

```text
posts -> window features -> sequential patterns -> prediction
```

The demo scripts are modular examples. They demonstrate the main stages of the research workflow with small sample files, but the sample files are simplified and are not intended to fully reproduce the original experimental pipeline end-to-end.

---

## Visualization

### Data Pipeline

The following figure shows the data collection, organization, and filtering process used in the original research.

<img src="figures/data_pipeline.png" alt="Data Pipeline" width="30%">

### Prediction Workflow

The following figure shows the prediction workflow based on the Pattern Intensity Set (PIS).

<img src="figures/prediction_workflow.png" alt="Prediction Workflow" width="30%">

---

## Results and Evaluation

The original research evaluated the prediction framework under four emotion classification schemes:

- **Scheme 3**: coarse-grained classification with Positive / Negative / Neutral categories
- **Scheme 5**: medium-grained classification
- **Scheme 8**: fine-grained emotional classification
- **Scheme 12**: more detailed emotional classification

The evaluation used Top-1, Top-3, and Top-5 accuracy together with prediction coverage.

Selected results are provided in:

```text
results/evaluation_summary.csv
```

### Key Findings

- Scheme 3 achieved strong Top-1 accuracy with high coverage, showing that coarse-grained emotion prediction is stable and reliable.
- Scheme 5, Scheme 8, and Scheme 12 provide more detailed emotional categories.
- Finer-grained schemes may reduce Top-1 coverage, but they provide richer emotional interpretation.
- The results show a trade-off between prediction accuracy, coverage, and emotional granularity.

For example, under the setting `margin=20` and `min_top1=40`, the following results were observed:

| Scheme | Top-1 Accuracy | Top-3 Accuracy | Top-5 Accuracy | Top-1 Coverage |
|---|---:|---:|---:|---:|
| Scheme 3 | 88.82% | — | — | 89.96% |
| Scheme 5 | 89.67% | 99.31% | — | 62.31% |
| Scheme 8 | 89.30% | 98.37% | 99.80% | 60.43% |
| Scheme 12 | 92.67% | 96.38% | 99.14% | 53.77% |

---

## Repository Structure

```text
emotion-transition-analysis/
├── README.md
├── requirements.txt
├── src/
│   ├── feature_extraction_demo.py
│   ├── pattern_mining_demo.py
│   └── demo.py
├── sample_data/
│   ├── sample_posts.csv
│   ├── sample_window_features.csv
│   └── sample_patterns.csv
├── figures/
│   ├── data_pipeline.png
│   └── prediction_workflow.png
└── results/
    ├── extracted_window_features_demo.csv
    ├── generated_patterns_demo.csv
    ├── demo_output.txt
    └── evaluation_summary.csv
```

---

## How to Run

This repository provides three simplified demos based on the research workflow.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### 1. Feature Extraction Demo

This demo shows how sample posts are divided into five 3-day windows and converted into window-level emotional features.

```bash
python src/feature_extraction_demo.py
```

Input:

```text
sample_data/sample_posts.csv
```

Output:

```text
results/extracted_window_features_demo.csv
```

### 2. Pattern Mining Demo

This demo generates full five-window sequential patterns from window-level emotional features.

```bash
python src/pattern_mining_demo.py
```

Input:

```text
sample_data/sample_window_features.csv
```

Output:

```text
results/generated_patterns_demo.csv
```

### 3. Prediction Demo

This demo predicts the next emotional state from a prepared sequential pattern table.

```bash
python src/demo.py
```

Input:

```text
sample_data/sample_patterns.csv
```

Example output:

```text
Current emotion sequence:
friends -> work -> pain -> death

Predicted next emotions:
Top 1: healing | score = 0.3580
Top 2: optimism | score = 0.1480
```

---

## Sample Data

### `sample_data/sample_posts.csv`

Small artificial sample post data used to demonstrate the feature extraction workflow.

### `sample_data/sample_window_features.csv`

Example window-level emotional features. Each row represents one user and one 3-day window.

### `sample_data/sample_patterns.csv`

Example sequential pattern data containing:

- Sequential Pattern
- Category Pattern
- Support
- Confidence
- Sequential Confidence
- Count

---

## Demo Outputs

### `results/extracted_window_features_demo.csv`

Actual output from running `src/feature_extraction_demo.py`.

This file demonstrates how sample post data is converted into five 3-day window-level emotional features.

### `results/generated_patterns_demo.csv`

Actual output from running `src/pattern_mining_demo.py`.

This file demonstrates how window-level emotional features are converted into full five-window sequential patterns with support, confidence, sequential confidence, and count.

### `results/demo_output.txt`

Actual output from running `src/demo.py`.

This file demonstrates the simplified Top-k next emotion prediction result.

### `results/evaluation_summary.csv`

Selected evaluation results from the original research experiment.

---

## Code and Data Availability

This repository is a portfolio version of my master's research project.

The full research project used large-scale Reddit data from 2018 to 2022 and included Reddit data extraction, text preprocessing, user cohort filtering, most-active 15-day period selection, 3-day window segmentation, Empath-based emotion feature extraction, sequential pattern mining, PIS construction, and Top-k emotion prediction.

Due to data size, privacy considerations, and dataset usage restrictions, the original Reddit dataset and full experimental pipeline are not included in this repository.

Instead, this repository provides simplified and reproducible demo files:

- `src/feature_extraction_demo.py` demonstrates how sample posts are converted into five 3-day window-level emotional features.
- `src/pattern_mining_demo.py` demonstrates how window-level emotional features are converted into sequential patterns with support, confidence, sequential confidence, and count.
- `src/demo.py` demonstrates how prepared sequential pattern data can be used for Top-k next emotion prediction.
- `sample_data/` contains small artificial sample data for demonstration.
- `results/` contains actual outputs from the demo scripts and selected evaluation results from the original research.

The simplified demos are designed to show the core workflow and logic of the research in a compact, readable, and runnable form.

---

## Target Positions

This project is relevant to positions such as:

- Data Analyst
- Python Developer
- AI / Machine Learning Assistant Engineer
- Research Assistant
- Software Engineer with data analysis responsibilities

---

## Notes

This repository is intended for portfolio and job-hunting purposes.

The goal is to present the research workflow, implementation logic, and selected results in a clear and reproducible way, while avoiding the release of large-scale raw social media data.
