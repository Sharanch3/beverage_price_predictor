# 🍷 CodeX: Beverage Price Range Predictor

A machine learning web application that predicts the **price range of a beverage** a consumer is likely to purchase, based on their demographic profile, consumption habits, and brand preferences — built with **Streamlit**, **scikit-learn**, and **LightGBM**, with full experiment tracking via **MLflow + DagsHub**.

---

## Overview

Beverage companies struggle to identify which price tier a consumer is likely to target. This project solves that by training a classification model on real consumer survey data and deploying it as an interactive Streamlit app.

**Input:** 15 consumer attributes (age, zone, income, brand preference, etc.)  
**Output:** Predicted beverage price range (Budget / Mid-Range / Premium / Luxury)

---

## 🌐 Live Demo

**LINK:** https://beverage-price-predictor.streamlit.app/

---

## ML Pipeline

The full pipeline has 4 stages:

```
Raw Form Input (15 fields)
        │
        ▼
engineer_features()          ← runs outside the sklearn Pipeline
  • age         →  age_group (binned)
  • zone        →  ordinal int 1–4
  • income      →  ordinal int 0–5
  • frequency   →  ordinal int 1–3
  • awareness   →  ordinal int 1–3
  • cf_ab_score = freq / (freq + awareness)
  • zas_score   = zone × income
  • bsi         = brand switching indicator (0/1)
        │
        ▼
sklearn Pipeline
  ├── Step 1: ColumnTransformer (preprocessing)
  │     ├── OrdinalEncoder   → age_group, health_concerns, preferable_size
  │     ├── OneHotEncoder    → gender, occupation, brand, flavor, channel, etc.
  │     └── passthrough      → numeric engineered features
  │
  └── Step 2: LGBMClassifier (champion model)
        │
        ▼
LabelEncoder.inverse_transform()
        │
        ▼
   Predicted Price Range
```

---

## Feature Engineering

| Feature | Formula | Description |
|---|---|---|
| `age_group` | `pd.cut(age, bins)` | Age binned into 6 brackets |
| `cf_ab_score` | `freq / (freq + awareness)` | Brand loyalty ratio (0–1) |
| `zas_score` | `zone × income_levels` | Zone-adjusted spending power |
| `bsi` | `np.where(brand != Established & reason in [Price, Quality])` | Brand switching indicator |

---

## Models Evaluated

All 6 models were trained on a 75/25 train-test split and tracked via MLflow:

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Gaussian Naive Bayes | ~72% | ~71% | ~72% | ~71% |
| Logistic Regression | ~78% | ~78% | ~78% | ~78% |
| SVM | ~80% | ~80% | ~80% | ~80% |
| Random Forest | ~85% | ~85% | ~85% | ~85% |
| XGBoost | ~87% | ~87% | ~87% | ~87% |
| **LightGBM** ✅ | **~88%** | **~88%** | **~88%** | **~88%** |

**LightGBM** was selected as the champion model based on highest weighted F1 score and accuracy.

---

## Experiment Tracking

All training runs are logged to **DagsHub** via **MLflow**

View all runs at:  
🔗 `https://dagshub.com/Sharanch3/beverage_price_predictor`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web App | Streamlit |
| ML Framework | scikit-learn |
| Champion Model | LightGBM |
| Other Models | XGBoost, RandomForest, SVM, LogReg, GaussianNB |
| Experiment Tracking | MLflow + DagsHub |
| Data Manipulation | Pandas, NumPy |
| Model Persistence | Joblib |
| Visualization | Matplotlib, Seaborn |
| Language | Python 3.10+ |

---

> Built by [Sharanch3](https://github.com/Sharanch3)
