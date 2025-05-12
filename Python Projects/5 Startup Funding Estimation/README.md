# Startup Funding Estimation

This project analyzes how founding conditions influence the total investment startups receive. Using data from over 28,000 companies founded between 1995 and 2015, we built a regression model to capture relationships between funding amounts, market type, founding year, location, and global economic context.

## What’s in the project

- Cleaned startup-level data and merged it with annual global GDP
- Created features such as time to first funding, age at last funding, and number of categories
- Applied log transformation to reduce skew
- Built a regression pipeline with scaling, encoding, and cross-validation
- Trained and compared four models: Linear Regression, Decision Tree, AdaBoost, and XGBoost
- Selected XGBoost based on test performance

## Key insights

- Biotech companies receive higher total funding due to capital intensity  
- Software startups are most common but receive lower funding on average  
- Funding patterns followed global GDP before 2008, then diverged after the financial crisis

## Use cases

The model supports early-stage investment screening, funding potential analysis, and startup ecosystem research. It offers a structured way to understand how timing, industry, and macro conditions shape long-term funding outcomes.

## Files

- **startup_trend_analysis.ipynb** – Explores startup trends and funding evolution  
- **funding_prediction_modeling.ipynb** – Feature engineering, model training, and evaluation  
- **organisations.csv** – Cleaned startup dataset  
- **World_Gross domestic product.csv** – Global GDP data by year

## Tools

Python, pandas, scikit-learn, XGBoost, matplotlib, seaborn
