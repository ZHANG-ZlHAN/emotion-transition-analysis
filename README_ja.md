# SNSにおける感情遷移の分析と予測

[English README](README.md)

本リポジトリは、修士研究
**「Exploring Emotional Transitions on Social Media Through Sequential Pattern Mining」**
を、就職活動用のポートフォリオとして再整理したものです。

Redditの投稿データを用いて、ユーザーの感情状態を時系列的に分析し、
Sequential Pattern MiningとPattern Intensity Set（PIS）に基づく
解釈可能な手法によって、将来の感情カテゴリを予測します。

---

## 概要

SNS上の投稿には、ユーザーの感情状態や心理状態の変化が
時系列的に反映されることがあります。

本研究では、各投稿を独立して分析するのではなく、
一定期間内における感情の移り変わりに注目しました。

元の研究では、2018年から2022年までの大規模なRedditデータを使用し、
ユーザーを以下の4グループに分類しました。

- Depressive
- Normal
- Recovering
- Deteriorating

各ユーザーについて、投稿が最も活発な15日間を抽出し、
5つの連続した3日間ウィンドウに分割しました。

各ウィンドウから感情特徴を取得し、ユーザーごとの感情系列を作成した後、
頻出する感情遷移パターンを抽出しました。

抽出したパターンはPattern Intensity Set（PIS）として集約し、
直近の感情系列と照合することで、次に現れる感情カテゴリを予測しました。

---

## 使用技術

- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- Plotly
- Sequential Pattern Mining
- Pattern Intensity Set（PIS）
- Top-k予測
- Sankey Diagramによる可視化

元の研究では、以下も使用しました。

- Academic Torrents / Pushshift ArchiveのRedditデータ
- Empathによる感情特徴抽出
- 絵文字の正規化
- NLTKを用いたテキスト前処理

---

## 担当内容

本プロジェクトは私の修士研究です。

主に以下の作業を担当しました。

- Reddit投稿データの収集と前処理
- ユーザーグループ分類ロジックの設計
- 各ユーザーの最活発15日間の抽出
- 15日間を5つの3日間ウィンドウに分割
- 投稿テキストからの感情特徴抽出
- ユーザー単位の感情系列の構築
- 感情遷移に対するSequential Pattern Mining
- PISベースの予測アルゴリズムの設計
- Top-1、Top-3、Top-5精度による評価
- Sankey Diagramを用いた感情遷移の可視化

---

## 研究ワークフロー

元の研究は、主に以下の流れで実施しました。

1. **データ収集**
   - 2018年から2022年までのReddit投稿を、
     アーカイブされた`.zst`ファイルから取得しました。

2. **ユーザーグループの分類**
   - ユーザーをDepressive、Normal、Recovering、
     Deterioratingの4グループに分類しました。

3. **データのフィルタリングと前処理**
   - 削除済みユーザーや無効な投稿を除外しました。
   - アクティブな投稿日が15日未満のユーザーを除外しました。
   - 投稿テキストのクリーニングと正規化を行いました。

4. **最活発期間の選択**
   - 各ユーザーについて、最も投稿が活発な15日間を抽出しました。

5. **ウィンドウ分割**
   - 15日間を5つの連続した3日間ウィンドウに分割しました。

6. **感情特徴抽出**
   - 各ウィンドウから代表的な感情特徴を取得しました。
   - 各ユーザーを5ステップの感情系列として表現しました。

7. **Sequential Pattern Mining**
   - 頻出する感情遷移パターンを抽出しました。
   - Support、Confidence、Sequential Confidence、
     Countを計算しました。

8. **PIS構築と予測**
   - 抽出したパターンをPattern Intensity Setとして集約しました。
   - 直近の部分系列とPIS内のパターンを照合しました。
   - スコアリング方式によって将来の感情をTop-k形式で予測しました。

---

## 時系列分割

各ユーザーについて、投稿が最も活発な15日間を選択し、
以下の5つのウィンドウに分割しました。

| ウィンドウ | 対象期間 |
|---|---|
| W1 | 1日目～3日目 |
| W2 | 4日目～6日目 |
| W3 | 7日目～9日目 |
| W4 | 10日目～12日目 |
| W5 | 13日目～15日目 |

例：

```text
W1 → W2 → W3 → W4 → W5
Positive → Neutral → Negative → Negative → Positive
```

この系列は、15日間におけるユーザーの感情遷移を表します。

---

## 感情系列の構築

各3日間ウィンドウから抽出した感情カテゴリを並べ、
ユーザーごとの感情系列を構築しました。

例：

```text
[Positive, Neutral, Negative, Negative, Positive]
```

評価では、異なる粒度の感情分類方式を比較しました。

- 3カテゴリ
- 5カテゴリ
- 8カテゴリ
- 12カテゴリ

これにより、感情分類の細かさと予測性能の関係を比較できます。

---

## Sequential Pattern Mining

ユーザー単位の感情系列から、頻出する感情遷移パターンを抽出しました。

各パターンについて、以下の指標を計算しました。

### Support

データ全体におけるパターンの出現頻度を示します。

```text
Support = Pattern Count / Total Sequence Count
```

### Confidence

同じ開始感情を持つ系列の中で、
対象パターンが出現する割合を示します。

```text
Confidence = Pattern Count / First Emotion Count
```

### Sequential Confidence

特定の接頭系列が現れた後に、
次の感情が出現する割合を示します。

```text
Sequential Confidence = Pattern Count / Prefix Count
```

---

## Pattern Intensity Set（PIS）

PISには、抽出した感情遷移パターンと以下の統計情報を保存します。

- Sequential Pattern
- Category Pattern
- Support
- Confidence
- Sequential Confidence
- Count

このPISを将来の感情予測に利用します。

---

## 予測手法

直近の感情遷移から、次に現れる感情カテゴリを予測します。

例として、以下の系列が与えられた場合：

```text
[Positive, Neutral, Negative, Negative]
```

予測結果はランキング形式で出力されます。

```text
Top 1: Negative
Top 2: Neutral
Top 3: Positive
```

予測スコアには、主に以下の要素を使用しました。

- パターンの出現頻度
- Confidence
- パターン長
- 入力系列との距離
- Count

最終的に、可能性の高い将来の感情カテゴリをTop-k形式で返します。

---

## 簡略化デモ

本リポジトリでは、元の研究処理を簡略化した
実行可能なデモを提供しています。

元の大規模Redditデータは公開せず、
少量の人工サンプルデータを用いて主要処理を再現しています。

```text
サンプル投稿
    ↓
feature_extraction_demo.py
    ↓
ウィンドウ単位の感情特徴
    ↓
pattern_mining_demo.py
    ↓
感情遷移パターン
    ↓
demo.py
    ↓
次の感情のTop-k予測
```

各デモはモジュール単位の処理例です。

元の研究パイプライン全体を完全に再現するものではありませんが、
主要な処理ロジックを小規模なデータで確認できます。

---

## 可視化

### データ処理パイプライン

元の研究におけるデータ収集、整理、
フィルタリング処理を示します。

<img src="figures/data_pipeline.png" alt="Data Pipeline" width="30%">

### 予測ワークフロー

Pattern Intensity Setに基づく予測処理を示します。

<img src="figures/prediction_workflow.png" alt="Data Pipeline" width="30%">

---

## 評価結果

予測フレームワークは、以下の4つの感情分類方式で評価しました。

- Scheme 3：Positive / Negative / Neutralによる粗粒度分類
- Scheme 5：中粒度分類
- Scheme 8：より細かい感情分類
- Scheme 12：最も詳細な感情分類

評価指標には、以下を使用しました。

- Top-1 Accuracy
- Top-3 Accuracy
- Top-5 Accuracy
- Prediction Coverage

選択した結果は以下に保存しています。

```text
results/evaluation_summary.csv
```

### 主な結果

- Scheme 3では、高いカバレッジを維持しながら
  安定したTop-1精度を確認しました。
- Scheme 5、8、12では、より詳細な感情カテゴリを扱えます。
- 分類を細かくするとTop-1のカバレッジが下がる場合がありますが、
  より詳細な感情解釈が可能になります。
- 予測精度、カバレッジ、感情粒度の間には
  トレードオフが存在します。

`margin=20`、`min_top1=40`の設定例：

| Scheme | Top-1 Accuracy | Top-3 Accuracy | Top-5 Accuracy | Top-1 Coverage |
|---|---:|---:|---:|---:|
| Scheme 3 | 88.82% | — | — | 89.96% |
| Scheme 5 | 89.67% | 99.31% | — | 62.31% |
| Scheme 8 | 89.30% | 98.37% | 99.80% | 60.43% |
| Scheme 12 | 92.67% | 96.38% | 99.14% | 53.77% |

---

## リポジトリ構成

```text
emotion-transition-analysis/
├── README.md
├── README_ja.md
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

## 実行方法

### 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 1. 感情特徴抽出デモ

サンプル投稿を5つの3日間ウィンドウに分割し、
ウィンドウ単位の感情特徴へ変換します。

```bash
python src/feature_extraction_demo.py
```

入力：

```text
sample_data/sample_posts.csv
```

出力：

```text
results/extracted_window_features_demo.csv
```

### 2. パターン抽出デモ

ウィンドウ単位の感情特徴から、
5ステップの感情遷移パターンを生成します。

```bash
python src/pattern_mining_demo.py
```

入力：

```text
sample_data/sample_window_features.csv
```

出力：

```text
results/generated_patterns_demo.csv
```

### 3. 予測デモ

準備済みのSequential Patternデータから、
次に現れる感情を予測します。

```bash
python src/demo.py
```

入力：

```text
sample_data/sample_patterns.csv
```

出力例：

```text
Current emotion sequence:
friends -> work -> pain -> death

Predicted next emotions:
Top 1: healing | score = 0.3580
Top 2: optimism | score = 0.1480
```

---

## サンプルデータ

### `sample_data/sample_posts.csv`

感情特徴抽出処理を説明するための、
少量の人工的な投稿データです。

### `sample_data/sample_window_features.csv`

ウィンドウ単位の感情特徴データです。

各行は、1ユーザーの1つの3日間ウィンドウを表します。

### `sample_data/sample_patterns.csv`

以下の情報を含むSequential Patternのサンプルです。

- Sequential Pattern
- Category Pattern
- Support
- Confidence
- Sequential Confidence
- Count

---

## デモ出力

### `results/extracted_window_features_demo.csv`

`feature_extraction_demo.py`を実行して生成した出力です。

投稿データが5つのウィンドウ単位の感情特徴へ
変換される流れを確認できます。

### `results/generated_patterns_demo.csv`

`pattern_mining_demo.py`を実行して生成した出力です。

ウィンドウ単位の感情特徴から、
Support、Confidence、Sequential Confidence、
Countを持つ遷移パターンが生成されます。

### `results/demo_output.txt`

`demo.py`を実行して得られたTop-k予測結果です。

### `results/evaluation_summary.csv`

元の研究実験から選択した評価結果です。

---

## コードとデータの公開範囲

元の研究では、2018年から2022年までの大規模Redditデータを使用し、
以下を含む処理パイプラインを構築しました。

- Redditデータ抽出
- テキスト前処理
- ユーザーグループ分類
- 最活発15日間の選択
- 3日間ウィンドウへの分割
- Empathによる感情特徴抽出
- Sequential Pattern Mining
- PIS構築
- Top-k感情予測

データサイズ、プライバシー、利用条件を考慮し、
元のRedditデータセットと完全な実験パイプラインは
本リポジトリに含めていません。

代わりに、以下を公開しています。

- 簡略化したPythonデモ
- 少量の人工サンプルデータ
- デモコードの実行結果
- 元の研究から選択した評価結果
- データ処理および予測フローの図

---

## 想定職種

本プロジェクトは、以下の職種に関連します。

- データアナリスト
- Pythonエンジニア
- AI・機械学習アシスタントエンジニア
- 研究開発アシスタント
- データ可視化エンジニア
- データ分析業務を含むソフトウェアエンジニア

---

## 備考

本リポジトリは、研究内容、実装ロジック、
評価結果を分かりやすく提示することを目的とした
就職活動用ポートフォリオです。

大規模なSNS生データを公開せずに、
研究の主要な処理フローと再現可能なデモを提供しています。
