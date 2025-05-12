# Startup Funding Estimation

This project builds a regression-based machine learning model to estimate total investment received by startups, based on founding characteristics, sector, and macroeconomic conditions. The goal is to capture how structural factors—such as industry type, founding year, and global GDP—relate to long-term funding outcomes.

We used data from over 28,000 startups founded between 1995 and 2015, merged with annual global GDP figures. Key features were engineered to capture time-to-funding, company age at last investment, and category diversity. Skewed variables were log-transformed. The modeling pipeline included scaling, one-hot encoding, and cross-validation using scikit-learn’s `ColumnTransformer`.

Four regression models were trained and evaluated: Linear Regression, Decision Tree, AdaBoost, and XGBoost. After hyperparameter tuning with `GridSearchCV` and 5-fold cross-validation, XGBoost was selected for its superior performance on unseen data.

The model revealed sector-level differences—biotech startups typically receive more investment than software startups—and identified a divergence between GDP and funding trends post-2008. This approach offers a scalable way to simulate funding dynamics and can support early-stage investment screening and startup ecosystem analysis.

## Files

- **startup_trend_analysis.ipynb** – Funding trend and sector analysis  
- **funding_prediction_modeling.ipynb** – Feature engineering and model training  
- **organisations.csv** – Startup dataset  
- **World_Gross domestic product.csv** – Yearly GDP data

## Tools

Python, pandas, scikit-learn, XGBoost, Jupyter Notebook
