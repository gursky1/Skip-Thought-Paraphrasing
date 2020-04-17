# This is the script that generates the neighborhood noise for my IR paper
library(tidyverse)
library(MASS)

# Creating our two multivariate normal clusters
cluster_1 <- mvrnorm(n=2000, mu=c(1,1),Sigma=matrix(c(5,-2.75,-1.5,3),2,2))
cluster_1 <- data.frame(cluster_1)
colnames(cluster_1) <- c('X1','X2')
cluster_2 <- mvrnorm(n=2000, mu=c(5,8),Sigma=matrix(c(10,-2,2,2),2,2))
cluster_2 <- data.frame(cluster_2)
colnames(cluster_2) <- c('X1','X2')

# Creating our three points
original_thought <- c(2.5,0.5)
good_thought <- original_thought + c(-3,1.5)
bad_thought <- original_thought + c(1.5,3)
other_thought <- c(5,7.5)

# Calculating distances
dist_mat <- matrix(c(original_thought, good_thought, bad_thought), nrow=3, byrow = TRUE)
dist(dist_mat)

# Creating our labels
original_label <- 'I saw a dog in the park.'
good_label <- 'There was a dog in the park.'
bad_label <- 'What is the dog doing today?'
other_label <- 'What are you doing today?'

# Plotting our data
ggplot()+
  ggtitle('Neighborhood-Aware Noise Application')+
  theme(legend.position="none") +
  coord_fixed() +
  geom_point(data=cluster_1, aes(x=X1,y=X2),color='red', alpha=0.5)+
  geom_point(data=cluster_2, aes(x=X1,y=X2),color='blue', alpha=0.5, shape=2)+
  geom_segment(aes(x=original_thought[1],y=original_thought[2], xend=good_thought[1], yend=good_thought[2]), size=1.4,arrow = arrow(length = unit(0.5, "cm")))+
  geom_segment(aes(x=original_thought[1],y=original_thought[2], xend=bad_thought[1], yend=bad_thought[2]), size=1.4,arrow = arrow(length = unit(0.5, "cm")))+
  geom_point(aes(x=original_thought[1],y=original_thought[2]),size=5)+
  geom_point(aes(x=good_thought[1],y=good_thought[2]),size=5)+
  geom_point(aes(x=bad_thought[1],y=bad_thought[2]),size=5) +
  geom_point(aes(x=other_thought[1],y=other_thought[2]),size=5) +
  geom_label(aes(x=original_thought[1],y=original_thought[2], label=original_label, size=2, fontface=2, hjust=-0.1)) +
  geom_label(aes(x=good_thought[1],y=good_thought[2], label=good_label, size=2, fontface=2, vjust=-1,hjust=0.8)) +
  geom_label(aes(x=bad_thought[1],y=bad_thought[2], label=bad_label, size=2, fontface=2, vjust=0,hjust=-0.05)) +
  geom_label(aes(x=other_thought[1],y=other_thought[2], label=other_label, size=2, fontface=2, vjust=-0.5, hjust=-0.05))
