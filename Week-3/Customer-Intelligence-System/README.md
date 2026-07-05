# Customer Intelligence System using Classification, Ensemble Learning & Clustering

> An end-to-end Machine Learning project that predicts customer campaign responses and segments customers into meaningful groups using supervised and unsupervised learning techniques.

---

## Project Overview

This project builds a **Customer Intelligence System** that helps businesses understand customer behavior, predict campaign responses, and identify customer segments for targeted marketing.

The project combines:

- Classification
- Ensemble Learning (Random Forest & XGBoost)
- Clustering (K-Means & DBSCAN)

to generate actionable business insights.

---

## Problem Statement

Develop a Customer Intelligence System using classification, ensemble learning (Random Forest, XGBoost), and clustering (K-Means, DBSCAN), achieving optimized predictive performance and actionable customer segmentation insights.

---

## Objectives

- Analyze customer demographics and purchasing behavior.
- Predict whether a customer will respond to a marketing campaign.
- Compare multiple machine learning models.
- Segment customers into meaningful groups.
- Generate business recommendations based on customer intelligence.

---

## Dataset

The dataset contains customer information including:

- Demographics
- Income
- Education
- Marital Status
- Product Spending
- Purchase History
- Campaign Acceptance
- Website Activity

Target Variable:

- **Response**
  - 1 → Customer accepted the campaign
  - 0 → Customer did not accept the campaign

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- XGBoost
- Jupyter Notebook

---

## Project Workflow

```
Data Collection
        │
        ▼
Data Understanding
        │
        ▼
Data Cleaning
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Engineering
        │
        ▼
Classification Models
(Logistic Regression)
        │
        ▼
Ensemble Learning
(Random Forest & XGBoost)
        │
        ▼
Customer Segmentation
(K-Means & DBSCAN)
        │
        ▼
Business Insights
```

---

## Feature Engineering

The following features were created:

- Customer Age
- Customer Tenure
- Family Size
- Total Spending
- Total Purchases
- Total Accepted Campaigns
- Total Children

These engineered features improved both predictive modeling and customer segmentation.

---

## Machine Learning Models

### Classification

- Logistic Regression
- Random Forest
- XGBoost

### Clustering

- K-Means
- DBSCAN

---

## Model Performance

| Model | Accuracy | ROC-AUC |
|--------|----------|---------|
| Logistic Regression | **88.39%** | **0.877** |
| Random Forest | **88.62%** | **0.878** |
| **XGBoost** | **89.06%** | **0.903** |

### Best Performing Model

**XGBoost** achieved the highest ROC-AUC score, making it the best model for predicting customer campaign responses.

---

## Customer Segmentation

Customers were segmented using:

- K-Means Clustering
- DBSCAN Clustering

K-Means identified four major customer groups based on:

- Income
- Spending
- Purchase Frequency

These segments can be used for personalized marketing strategies.

---

## Key Business Insights

- Only **14.7%** of customers responded to the marketing campaign.
- **XGBoost** achieved the best predictive performance.
- **Recency** is the most influential feature for campaign prediction.
- Customer Tenure and Previous Campaign Acceptance are strong indicators of future responses.
- Higher-income customers generally spend more and respond more frequently.
- Wine and Meat Products contribute the highest overall revenue.
- K-Means identified a premium customer segment with high spending and frequent purchases.
- DBSCAN detected several outlier customer groups with unique purchasing behaviors.

---

## Business Recommendations

- Use the XGBoost model to identify customers most likely to respond before launching campaigns.
- Target premium customers with loyalty rewards and personalized offers.
- Focus marketing efforts on customers with recent purchases and high engagement.
- Promote wine and meat products through premium campaigns.
- Re-engage low-spending customers using discounts and personalized promotions.

---

## Project Structure

```
Customer-Intelligence-System/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── images/
│
├── notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_Feature_Engineering.ipynb
│   ├── 05_Classification_Ensemble.ipynb
│   ├── 06_Clustering.ipynb
│   └── 07_Business_Insights.ipynb
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## How to Run

Clone the repository

```bash
git clone <repository-url>
```

Navigate to the project

```bash
cd Customer-Intelligence-System
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch Jupyter Notebook

```bash
jupyter notebook
```

Run the notebooks in sequence from **01_Data_Understanding.ipynb** to **07_Business_Insights.ipynb**.

---

## Future Improvements

- Hyperparameter tuning using GridSearchCV
- Explainability with SHAP values
- Interactive dashboard using Streamlit
- Automated ML pipeline
- Model deployment using FastAPI or Flask

---

## Author

**Siddharth Gupta**

Machine Learning | Data Science | AI Enthusiast

---