# Startup Funding Estimation

This project builds a regression-based ML pipeline to predict startup funding amounts based on founding year, market, country, and macroeconomic data. The goal is to identify structural patterns in funding outcomes across industries and time.

This project used data from over 28,000 startups (1995–2015) and merged it with global GDP figures. Key features include time-to-first/last funding, startup age, and category diversity. Skewed variables were log-transformed. The pipeline used scaling, encoding, and 5-fold cross-validation.

Four models were trained and compared: Linear Regression, Decision Tree, AdaBoost, and XGBoost. XGBoost achieved the best test R² (0.53). The model revealed sector-level differences and post-2008 divergence between GDP and funding trends.

This end-to-end pipeline is reproducible and extendable, suitable for exploring early-stage investment patterns and startup ecosystem dynamics.

## Files

- **startup_trend_analysis.ipynb** – Funding trend and sector analysis  
- **funding_prediction_modeling.ipynb** – Feature engineering and model training  
- **organisations.csv** – Startup dataset  
- **World_Gross domestic product.csv** – Yearly GDP data

## Tools

Python, pandas, scikit-learn, XGBoost, Jupyter Notebook
