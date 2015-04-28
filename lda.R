#load required libraries
library(svDialogs)
library(lda)
library(tm)
library(SnowballC)
library(reshape2)
library(ggplot2)

##Select and read the reviews file
read_file <- dlgOpen(getwd(), title="Please select the data",multiple = FALSE,gui = .GUI)$res
data <- read.csv(read_file)

##remove unwanted strings
reviews <- tolower(data[,2])
reviews <- removeWords(reviews, stopwords("english"))
reviews <- removePunctuation(reviews)
reviews <- stemDocument(reviews)
reviews <- removeNumbers(reviews)

lex_reviews <- lexicalize(reviews)

K <- 15 #number of topics

#fit LDA
result <- lda.collapsed.gibbs.sampler(documents=lex_reviews[[1]], 
                                      K, vocab=lex_reviews[[2]], num.iterations=3000,
                                      alpha=0.1, eta=0.1, compute.log.likelihood=TRUE)

## Get the top words in the cluster
top.words <- top.topic.words(result$topics, 5, by.score=TRUE)

##print top words
top.words
