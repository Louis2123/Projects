import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import numpy as np
import io

# Define working directory options
Workdirectorya = '/Users/'

# Set the current working directory
current_directory = Workdirectorya

# Load dataset
csv_filename = "All_Reviews_Washington_ratings_fixed.csv"
csv_path = os.path.join(current_directory, csv_filename)
df = pd.read_csv(csv_path, delimiter=";", encoding='ISO-8859-1')

##############################################################################################################################
##############################################################################################################################
# Display basic info about the dataset
print(df.info())

# Capture df.info() output as text
buffer = io.StringIO()
df.info(buf=buffer)
info_text = buffer.getvalue()
buffer.close()

# Display df.info() as an image
fig, ax = plt.subplots(figsize=(12, 6))
ax.text(0, 1, info_text, fontsize=10, family="monospace", verticalalignment="top")
ax.axis("off")
plt.show()

#Dropping missing values
df = df.dropna()

#Display further basic information
print(df.describe().T.round(2))

# Display df.describe() as an image
desc_stats = df.describe().T.round(2)
fig, ax = plt.subplots(figsize=(12, len(desc_stats) * 0.4))
ax.axis("tight")
ax.axis("off")
table = ax.table(cellText=desc_stats.values, colLabels=desc_stats.columns, rowLabels=desc_stats.index,
                 cellLoc="center", loc="center")
plt.show()

##############################################################################################################################
##############################################################################################################################

# Histogram of ratings
plt.figure(figsize=(8, 5))
sns.histplot(df['rating'], bins=5)
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.title("Distribution of Ratings")
plt.show()

# Histogram of the friends per user
plt.figure(figsize=(8, 5))
sns.histplot(df['friends'], bins=100)
plt.xlabel("Friends")
plt.ylabel("Frequency")
plt.title("Distribution of Friends")
plt.show()

# Histogram of the review count per user
plt.figure(figsize=(8, 5))
sns.histplot(df['reviews'], bins=100)
plt.xlabel("Review count")
plt.ylabel("Frequency")
plt.title("Distribution of Review count")
plt.show()

# Histogram of the Photos posted count per user
plt.figure(figsize=(8, 5))
sns.histplot(df['Posted photoes'], bins=10)
plt.xlabel("Photos posted ")
plt.ylabel("Frequency")
plt.title("Distribution of Photos posted")
plt.show()

# Histogram of the word per review per user
plt.figure(figsize=(8, 5))
sns.histplot(df['word length'], bins=100)
plt.xlabel("Word Length")
plt.ylabel("Frequency")
plt.title("Distribution of Word Length")
plt.show()

# Histogram of the characters per review per user
plt.figure(figsize=(8, 5))
sns.histplot(df['Char length'], bins=100)
plt.xlabel("Character Length")
plt.ylabel("Frequency")
plt.title("Distribution of Character Length")
plt.show()
##############################################################################################################################
##############################################################################################################################

# Ensure 'date_review' is in datetime format
df['date_review'] = pd.to_datetime(df['date_review'])

# Extract the year from the date column
df['year'] = df['date_review'].dt.year

plt.figure(figsize=(14, 5))
sns.histplot(df['year'], bins=df['year'].nunique(), discrete=True)
plt.xlabel("Year")
plt.ylabel("Frequency")
plt.title("Number of Reviews per Year")
plt.xticks(sorted(df['year'].unique()))  
plt.show()

##############################################################################################################################
##############################################################################################################################
#Distribution of the average ratings over time
#(1)Line plot

# Average ratings per quarter
df['year_quarter'] = df['date_review'].dt.to_period('Q')
avg_rating_per_quarter = df.groupby('year_quarter')['rating'].mean()

# Line plot
plt.figure(figsize=(14, 6))
avg_rating_per_quarter.index = avg_rating_per_quarter.index.astype(str)
sns.lineplot(x=avg_rating_per_quarter.index, y=avg_rating_per_quarter.values, marker="o", linestyle="-")

# Set X-axis
xticks_labels = avg_rating_per_quarter.index[::4]
xticks_positions = range(0, len(avg_rating_per_quarter), 4)
plt.xticks(xticks_positions, xticks_labels, rotation=45)

# Formatting
plt.xlabel("Year - Quarter")
plt.ylabel("Average Rating")
plt.title("Average Star Rating Over Time (Quarterly)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#(2)Boxplot
# Boxplot of ratings over time
plt.figure(figsize=(14, 6))
sns.boxplot(x=df['year_quarter'].astype(str), y=df['rating'])

# Set X-axis
xticks_labels = df['year_quarter'].astype(str).unique()[::4]
xticks_positions = range(0, len(df['year_quarter'].unique()), 4)
plt.xticks(xticks_positions, xticks_labels, rotation=45)

# Formatting
plt.xlabel("Year - Quarter")
plt.ylabel("Rating")
plt.title("Distribution of Ratings Over Time (Boxplot)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

##############################################################################################################################
##############################################################################################################################
# Scatterplot of Ratings vs Number of Reviews
plt.figure(figsize=(8, 5))
sns.scatterplot(x='reviews', y='rating', data=df, alpha=0.5)
plt.xlabel("Number of Reviews")
plt.ylabel("Rating")
plt.title("Ratings vs. Number of Reviews")
plt.show()

# Scatterplot of Ratings vs Number of Friends
plt.figure(figsize=(8, 5))
sns.scatterplot(x='friends', y='rating', data=df, alpha=0.5)
plt.xlabel("Number of Friends")
plt.ylabel("Rating")
plt.title("Ratings vs. Number of friends")
plt.show()

# Scatterplot of Ratings vs Number of Characters
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Char length', y='rating', data=df, alpha=0.5)
plt.xlabel("Number of Characters")
plt.ylabel("Rating")
plt.title("Ratings vs. Number of Characters")
plt.show()

# Scatterplot of Ratings vs Number of Words
plt.figure(figsize=(8, 5))
sns.scatterplot(x='word length', y='rating', data=df, alpha=0.5)
plt.xlabel("Number of Words")
plt.ylabel("Rating")
plt.title("Ratings vs. Number of Words")
plt.show()

##############################################################################################################################
##############################################################################################################################
# Boxplot of Word Count vs. Rating
plt.figure(figsize=(8, 5))
sns.boxplot(x=df['rating'], y=df['word length'])
plt.xlabel("Rating")
plt.ylabel("Word Count")
plt.title("Word Count vs. Rating")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


##############################################################################################################################
##############################################################################################################################
# Compute Average Word Length
df['avg_word_length'] = df['Char length'] / df['word length']

# Boxplot of Average Word Length vs. Rating
plt.figure(figsize=(8, 5))
sns.boxplot(x=df['rating'], y=df['avg_word_length'])
plt.xlabel("Rating")
plt.ylabel("Average Word Length")
plt.title("Average Word Length vs. Rating")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


##############################################################################################################################
##############################################################################################################################

#Location Analysis: Do toursist (people outside of Washington) have more nagetive reviews than locals (People from Washington)
# Define threshold for negative vs. positive reviews
negative_threshold = 2
positive_threshold = 5-negative_threshold  

# Categorize Washington vs. Other locations
df['is_washington'] = df['location'].apply(lambda x: 'Washington, DC' if x == 'Washington, DC' else 'Other')

# Categorize reviews as Positive or Negative
df['review_category'] = df['rating'].apply(lambda x: 'Negative' if x <= negative_threshold else 'Positive')

# Histogram of the amount of postive and negative reviews
plt.figure(figsize=(8, 5))
sns.histplot(df['review_category'], bins=2)
plt.xlabel("Review length")
plt.ylabel("Frequency")
plt.title("Distribution of Negative and Postive Reviews")
plt.show()


# Histogram of the amount of postive and negative reviews
plt.figure(figsize=(8, 5))
sns.histplot(df['is_washington'], bins=2)
plt.xlabel("Reviewr place")
plt.ylabel("Frequency")
plt.title("Distribution of Washington or Other")
plt.show()

# Count reviews per location and category
review_counts = df.groupby(['is_washington', 'review_category']).size().unstack().fillna(0)

# Normalize to get proportions (Optional: Comment out if you want raw counts)
review_counts = review_counts.div(review_counts.sum(axis=1), axis=0)

# Plot stacked bar chart
review_counts.plot(kind='bar', stacked=True, figsize=(8, 5), color=['red', 'green'])

# Formatting
plt.xlabel("Location")
plt.ylabel("Proportion of Reviews")
plt.title("Proportion of Positive vs. Negative Reviews (Washington, DC vs. Others)")
plt.legend(title="Review Type")
plt.xticks(rotation=0)
plt.show()

# Normalize and print the proportions 
review_percentages = review_counts.div(review_counts.sum(axis=1), axis=0) * 100
print(review_percentages)

##############################################################################################################################
##############################################################################################################################

# Extract year and quarter
df['year_quarter'] = df['date_review'].dt.to_period('Q')

# Count the number of reviews per quarter
quarterly_reviews = df['year_quarter'].value_counts().sort_index()

# Convert PeriodIndex to string for better plotting
quarterly_reviews.index = quarterly_reviews.index.astype(str)

# Select every third quarter for labeling, display 
xticks_labels = quarterly_reviews.index[::3]
if quarterly_reviews.index[-1] not in xticks_labels:
    xticks_labels = list(xticks_labels) + [quarterly_reviews.index[-1]]
xticks_positions = [quarterly_reviews.index.tolist().index(q) for q in xticks_labels]

# Plot the review counts per quarter
plt.figure(figsize=(10, 5))
sns.barplot(x=quarterly_reviews.index, y=quarterly_reviews.values, color='blue')

# Formatting
plt.xlabel("Year - Quarter")
plt.ylabel("Number of Reviews")
plt.title("Number of Reviews per Quarter")
plt.xticks(xticks_positions, xticks_labels, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Define review categories based on rating thresholds
negative_threshold = 2
df['review_category'] = df['rating'].apply(lambda x: 'Negative' if x <= negative_threshold else 'Positive')

# Count reviews per quarter and category
quarterly_counts = df.groupby(['year_quarter', 'review_category']).size().unstack().fillna(0)

# Normalize to get proportions
quarterly_proportions = quarterly_counts.div(quarterly_counts.sum(axis=1), axis=0)

# Convert PeriodIndex to string for better plotting
quarterly_proportions.index = quarterly_proportions.index.astype(str)
xticks_labels = quarterly_proportions.index[::3]
if quarterly_proportions.index[-1] not in xticks_labels:
    xticks_labels = list(xticks_labels) + [quarterly_proportions.index[-1]]
xticks_positions = [quarterly_proportions.index.tolist().index(q) for q in xticks_labels]

# Plot stacked bar chart
quarterly_proportions.plot(kind='bar', stacked=True, figsize=(10, 5), color=['red', 'green'])

# Formatting
plt.xlabel("Year - Quarter")
plt.ylabel("Proportion of Reviews")
plt.title("Proportion of Positive vs. Negative Reviews per Quarter")
plt.legend(title="Review Type")
plt.xticks(xticks_positions, xticks_labels, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

##############################################################################################################################
##############################################################################################################################

#Create an (non-)active profile(using the 4 variables) link the active profile to positive and negative ratings
# Define a function that checks if the profile is active
def is_active(row):
    return (row['friends'] >= 11 and 
            row['reviews'] >= 16 and 
            row['Profile'] == 1 and 
            row['Posted photoes'] >= 2)


# Add a new column 'active_profile' based on the is_active function
df['active_profile'] = df.apply(is_active, axis=1)

# Define threshold for negative vs. positive reviews
negative_threshold = 2
positive_threshold = 5 - negative_threshold  

# Categorize users as Active or Non-Active based on the 'active_profile' column
df['is_active'] = df['active_profile'].apply(lambda x: 'Active' if x else 'Non-Active')

# Categorize reviews as Positive or Negative based on rating
df['review_category'] = df['rating'].apply(lambda x: 'Negative' if x <= negative_threshold else 'Positive')

# Count reviews per user activity status and category
review_counts = df.groupby(['is_active', 'review_category']).size().unstack().fillna(0)

# Normalize to get proportions (Optional: Comment out if you want raw counts)
review_counts = review_counts.div(review_counts.sum(axis=1), axis=0)

# Plot stacked bar chart
review_counts.plot(kind='bar', stacked=True, figsize=(8, 5), color=['red', 'green'])

# Formatting
plt.xlabel("User Activity Status")
plt.ylabel("Proportion of Reviews")
plt.title("Proportion of Positive vs. Negative Reviews (Active vs. Non-Active Users)")
plt.legend(title="Review Type")
plt.xticks(rotation=0)
plt.show()

# Normalize and print the proportions 
review_percentages_active = review_counts.div(review_counts.sum(axis=1), axis=0) * 100

# Analyze Average Rating by Active vs. Non-Active Users
active_rating = df.groupby('is_active')['rating'].mean()

plt.figure(figsize=(8, 5))
active_rating.plot(kind='bar', color=['blue', 'orange'])
plt.xlabel("User Activity Status")
plt.ylabel("Average Rating")
plt.title("Average Rating by Active vs. Non-Active Users")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

print(review_percentages_active)
##############################################################################################################################
##############################################################################################################################

# Function to count punctuation marks (., , and !)
def count_punctuation(text):
    return text.count('.') + text.count(',') + text.count('!')

# Apply the function to the 'text' column and create a new column 'punctuation_count'
df['punctuation_count'] = df['text'].apply(count_punctuation)

# Group by 'is_active' and calculate the mean punctuation count per group
punctuation_analysis = df.groupby('is_active')['punctuation_count'].mean()

# Plotting the punctuation analysis
punctuation_analysis.plot(kind='bar', figsize=(8, 5), color=['blue', 'orange'])

# Formatting for punctuation plot
plt.xlabel("User Activity Status")
plt.ylabel("Average Punctuation Count in Reviews")
plt.title("Average Punctuation Count in Reviews (Active vs. Non-Active Users)")
plt.xticks(rotation=0)
plt.show()

print(punctuation_analysis)

##############################################################################################################################
##############################################################################################################################

# Conduct regression analysis between the rating and other features
X = df[['word length', 'avg_word_length', 'friends', 'reviews', 'is_active']]

# Convert 'is_active' to numeric
X['is_active'] = X['is_active'].map({'Active': 1, 'Non-Active': 0})

# Add intercept
X = sm.add_constant(X)

# Target variable
y = df['rating']

# Ensure X and y have the same number of rows
X, y = X.align(y, join='inner', axis=0)

# Run regression
model = sm.OLS(y, X).fit()

# Print summary
print(model.summary())


# Display regression summary as an image
summary_str = model.summary().as_text()
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')
ax.text(0, 1, summary_str, fontsize=10, family='monospace', verticalalignment='top')
plt.show()
