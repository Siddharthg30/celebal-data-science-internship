# End-to-End ML Pipeline on Tesla Sales & Delivery Data

## Overview

This project was completed as part of my Data Science Internship assignment. The objective was to build an end-to-end machine learning pipeline to predict Tesla vehicle deliveries using historical sales, production, pricing, and vehicle-related data.

The project covers the complete ML workflow, starting from data understanding and preprocessing to model building, evaluation, hyperparameter tuning, and time series forecasting.

---

## Dataset

- **Source:** Kaggle
- **Dataset:** Tesla EV Deliveries and Production Data (2015–2025)

The dataset contains information such as:

- Year and Month
- Region
- Vehicle Model
- Estimated Deliveries
- Production Units
- Average Price
- Battery Capacity
- Driving Range
- CO₂ Saved
- Charging Stations
- Source Type

---

## Project Workflow

1. Business Understanding
2. Dataset Understanding
3. Data Quality Assessment
4. Exploratory Data Analysis (EDA)
5. Feature Engineering
6. Data Preprocessing
7. Regression Model Comparison
8. Hyperparameter Tuning
9. Model Explainability
10. Time Series Forecasting (ARIMA)
11. Business Recommendations
12. Production Mindset

---

## Models Used

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor
- LightGBM Regressor

---

## Best Model

After comparing multiple regression models and tuning the best-performing model, **LightGBM Regressor** achieved the best performance.

| Metric | Score |
|--------|------:|
| MAE | 212.37 |
| RMSE | 277.16 |
| R² Score | 0.9950 |

---

## Time Series Forecasting

A baseline forecasting model was also built using **ARIMA(1,1,1)** to forecast Tesla's future monthly deliveries.

---

## Tools & Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- XGBoost
- LightGBM
- Statsmodels

---

## Project Outcome

This project demonstrates a complete end-to-end machine learning pipeline, including data preprocessing, feature engineering, model comparison, hyperparameter tuning, model interpretation, and forecasting. It also highlights how machine learning can support business decisions such as production planning and demand forecasting.

---
**Author:** Siddharth Gupta