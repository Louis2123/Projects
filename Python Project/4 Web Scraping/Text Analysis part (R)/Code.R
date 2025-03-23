###Step 1: Import Data

# Load packages
library(stm)        # Structural Topic Model
library(tm)         # Text Mining
library(SnowballC)  # Stemming words
library(ggplot2)    # Visualization
library(dplyr)      # Data manipulation
library(stargazer)  # Model output formatting
library(wordcloud)  # Word cloud visualization
library(parallel)   # Multiple core processing
library(gridExtra)  # Scatterplot
library(brglm2)


#import the review data
dir1 <- getwd()
yelp_reviews <- read.csv(file=paste0(dir1, "/Dataset_All_Reviews_Washington_ratings_fixed.csv"),
                         stringsAsFactors=FALSE, sep= ";")

###Step 2: Data Pre-processing
processed <- textProcessor(yelp_reviews$text, metadata = yelp_reviews)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
docs <- out$documents
vocab <- out$vocab
meta <-out$meta

###Step 3: Determining the Topic Number / Analysis Strategy

# Bottom-Up Approach
findingk <- searchK(out$documents, out$vocab, K = c(10:30),
                    prevalence =~ rating, data = meta, verbose=FALSE)
plot(findingk)

###Step 4: Running & Inspecting the Topic Model
First_STM <- stm(documents = out$documents, vocab = out$vocab,
                 K = 17, prevalence =~ rating,
                 max.em.its = 75, data = out$meta,
                 init.type = "Spectral", verbose = FALSE)

plot(First_STM)

# Keep only the rows in yelp_reviews that exist in out$meta,ensuring consistency after preprocessing (removing 21 empty documents)
yelp_reviews_cleaned <- yelp_reviews[rownames(yelp_reviews) %in% rownames(out$meta), ]

# Check topic keywords
labelTopics(First_STM, n = 20)

# choose the focal topic
focal_topics <- c(3, 8, 9, 10, 12, 13, 15, 16)

# Generate word clouds for focal topics
for (i in focal_topics) {
  cat("Showing topic:", i, "\n")
  cloud(First_STM, topic = i) }

# Display representative texts for focal topics
findThoughts(First_STM, texts = yelp_reviews_cleaned$text, n = 5, topics = focal_topics)

### plot the average rating per focal topic
topic_prop<-make.dt(First_STM, meta)
topic_means <- sapply(focal_topics, function(topic) {
  sum(topic_prop[[paste0("Topic", topic)]] * topic_prop$rating, na.rm = TRUE) / 
    sum(topic_prop[[paste0("Topic", topic)]], na.rm = TRUE)
})
barplot(topic_means, names.arg = paste0("Topic", focal_topics), las = 2, col = "gray", 
        main = "Average Rating per Focal Topic", ylab = "Average Rating")

###Step 5: Plotting Topics Over time (Focusing on Focal Topics)
meta$date_num <- as.Date(meta$date_review, format = "%m/%d/%Y")
meta$day <- as.numeric(meta$date_num - min(meta$date_num, na.rm = TRUE))
predict_topics <- estimateEffect(formula = focal_topics ~ day, 
                                 stmobj = First_STM, 
                                 metadata = meta, 
                                 uncertainty = "Global")

plot(predict_topics, "day", method = "continuous", 
     topics = focal_topics, 
     model = First_STM, 
     printlegend = TRUE, xaxt = "n", xlab = "Time", 
     main = "Topic Evolution Over Time")
yearseq <- seq(from = min(meta$date_num, na.rm = TRUE), 
                 to = max(meta$date_num, na.rm = TRUE), 
                 by = "1 year")  
yearlabels <- format(yearseq, "%Y")
axis(1, at = as.numeric(yearseq - min(meta$date_num, na.rm = TRUE)),  
       labels = yearlabels, las = 2, cex.axis = 0.8)

###Step 6: Scatter Plots (Topic Proportion vs Ratings)
focal_topics <- c("Topic3", "Topic8", "Topic9", "Topic10", "Topic12", "Topic13", "Topic15", "Topic16")
plots <- list()

for (topic in focal_topics) {
  p <- ggplot(topic_prop, aes_string(x = topic, y = "rating")) +
    geom_point(alpha = 0.5, color = "blue") +  # Scatter points
    geom_smooth(method = "lm", color = "red", se = TRUE) +  # Regression line
    theme_minimal() +
    labs(title = paste(topic, "vs Rating"), x = topic, y = "Rating")
  
  plots[[topic]] <- p
}
grid.arrange(grobs = plots, ncol = 2)

###Step 7: Predicators for High Ratings (Set ratings>=3 as 1; <3 as 0)
topic_prop <- as.data.frame(topic_prop)
topic_prop$high_rating <- ifelse(topic_prop$rating >= 3, 1, 0)
focal_topics <- c("Topic3", "Topic8", "Topic9", "Topic10", "Topic12", "Topic13", "Topic15", "Topic16")
topic_regression_data <- topic_prop[, c("high_rating", focal_topics)]
topic_regression_data <- as.data.frame(topic_regression_data)
logit_model <- glm(high_rating ~ ., data = topic_regression_data, family = binomial, method = "brglmFit")
summary(logit_model)
confint(logit_model)

path_A <- "/Users/logistic_regression_results.html"
output_path <- path_A
stargazer(logit_model, type = "html", out = output_path)