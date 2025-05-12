# Startup Funding Estimation

This project builds a regression-based machine learning model to explain how startup funding levels are shaped by founding context, market attributes, and macroeconomic conditions. The goal is to simulate funding outcomes across sectors and time, using structured data rather than financial statements or subjective assessments.

## Background

Startup investment behavior varies across industries, time periods, and economic cycles. To better understand the drivers behind total funding received, this project models historical startup data and global GDP to identify patterns in how funding is distributed based on early observable variables.

## Data

The dataset includes 28,000+ startups founded between 1995 and 2015. Key fields include founding year, country, industry categories, status, and total investment received. Global GDP data is added by founding year to capture external economic conditions.

## Method

- Cleaned and filtered the dataset, removing records with missing or zero funding
- Created features such as time to first and last funding, company age, category count, and GDP at founding
- Applied log transformation to skewed variables
- Built a pipeline using scikit-learn’s `ColumnTransformer` for scaling and encoding
- Trained and compared four regression models:
  - Linear Regression  
  - Decision Tree Regressor  
  - AdaBoost Regressor  
  - XGBoost Regressor
- Used 5-fold cross-validation and `GridSearchCV` for evaluation and tuning

## Results

XGBoost achieved the best performance and strongest generalization on the test set. The model revealed clear funding patterns:

- Biotech companies receive significantly more investment due to capital intensity
- Software startups are more common but receive less total funding on average
- Startup funding followed global GDP until 2008, after which the trend diverged

## Application

The model helps simulate startup funding potential based on founding variables. It can support investment screening, ecosystem analysis, and sector-level research in contexts where financial data is limited or unavailable.

## Files

- **startup_trend_analysis.ipynb** – Market-level trend analysis and exploratory insights
- **funding_prediction_modeling.ipynb** – Feature engineering, modeling, and evaluation
- **organisations.csv** – Cleaned startup dataset
- **World_Gross domestic product.csv** – Global GDP by year

## Tools

Python, pandas, scikit-learn, XGBoost, matplotlib, seaborn, Jupyter Notebook
