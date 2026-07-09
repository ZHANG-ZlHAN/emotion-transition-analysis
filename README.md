# Social Media Emotion Transition Analysis and Prediction

## 日本語概要

本プロジェクトは、Redditのユーザー投稿データを対象に、テキスト感情分類、時系列分割、感情遷移パターンの抽出を行い、過去の感情変化から将来の感情傾向を予測するデータ分析プロジェクトです。

大学院研究として実施した内容を、ポートフォリオ向けに整理したものです。

## Overview

This project analyzes Reddit user post data to identify emotional transition patterns over time and predict future emotional tendencies based on previous emotional changes.

The project includes text preprocessing, time-series segmentation, sequential pattern mining, emotion transition visualization, and Top-k emotion prediction.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Sankey Diagram
- Sequential Pattern Mining

## My Role

- Collected and preprocessed Reddit user post data
- Designed the 15-day time-window structure
- Converted user posts into emotion sequences
- Implemented sequential pattern mining
- Calculated Support, Confidence, and Sequential Confidence
- Built a ranking-based future emotion prediction method
- Visualized emotional transition flows using Sankey diagrams
- Evaluated prediction results with Top-1, Top-3, and Top-5 accuracy

## Key Features

- Reddit post data preprocessing
- 15-day user activity extraction
- 3-day time-window segmentation
- Emotion sequence construction
- Sequential pattern mining
- Future emotion Top-3 prediction
- Sankey diagram visualization
- Basic model evaluation

## Workflow

1. Collect Reddit post data
2. Clean and filter user records
3. Extract emotional features from post text
4. Divide user activity into 3-day time windows
5. Convert emotional changes into sequences
6. Mine frequent emotional transition patterns
7. Predict future emotional categories
8. Visualize emotion flows with Sankey diagrams
9. Evaluate prediction performance

## Notes

The original Reddit dataset is not included due to data privacy and usage restrictions.

This repository provides a simplified portfolio version of the research project.
