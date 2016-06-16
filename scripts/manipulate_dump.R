library(plyr)
library(reshape2)

tweet_dump <- read.csv(file="/Users/dbuchan/Code/twittercoding/code_dump.csv", header=FALSE,  strip.white = TRUE, sep=",",na.strings= c("999", "NA", " ", ""))
