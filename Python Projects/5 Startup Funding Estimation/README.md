# Startup Funding Estimation

This project builds a machine learning model to analyze how startup funding is influenced by founding conditions such as market type, timing, and macroeconomic context. The goal is not to predict specific outcomes for individual companies but to understand broader patterns in investment behavior across the startup landscape.

## Background

Startup funding varies significantly across industries and economic periods. While early-stage evaluations often rely on financial records or founder networks, this project takes a structured data approach. By modeling historical startup and GDP data, we explore how factors available at founding time relate to total investment received.

## Objective

To develop a regression-based model that explains and simulates total startup funding using structured company and economic data. The model aims to support large-scale analysis of funding dynamics and provide insight into how structural factors influence investment outcomes.

## Data

- 28,000+ startups founded between 1995 and 2015  
- Fields include founding year, country, market category, funding history  
- Global GDP data added by founding year to reflect macroeconomic context

## Method

- Cleaned and filtered startup data, removing invalid and missing values  
- Constructed features such as company age, time to funding, and category count  
- Merged annual GDP as an external variable  
- Applied log transformation to reduce skew in both features and target  
- Built a regression pipeline using scikit-learn tools for scaling and encoding  
- Trained and evaluated four models: Linear Regression, Decision Tree, AdaBoost, and XGBoost  
- Used 5-fold cross-validation and grid search for model tuning

## Results

- XGBoost performed best in both test accuracy and generalization  
- Biotech companies received more investment on average due to higher capital needs  
- Software startups were most common but had lower average funding  
- Funding patterns generally followed global GDP until 2008, after which they diverged

## Application

This model helps identify structural factors that influence startup funding. It can support early-stage investment screening, market analysis, and policy research on entrepreneurial finance.

## Files

- `startup_trend_analysis.ipynb`: Trend analysis and funding pattern exploration  
- `funding_prediction_modeling.ipynb`: Feature engineering, modeling, and evaluation  
- `organisations.csv`: Cleaned startup data  
- `World_Gross domestic product.csv`: Global GDP data by year

## Technologies

Python, pandas, scikit-learn, XGBoost, matplotlib, seaborn, Jupyter Notebook
