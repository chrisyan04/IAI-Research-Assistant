library(tidyverse)
library(ggplot2)

#Load data
my_data <- read.csv("merged108_148.csv")

# emails opened count vectors for week 1-3 
emails_opened <- my_data %>% summarize( 
  w1_o = sum(case_when(w1_opened == "EMAIL_OPENED" ~ 1, TRUE ~ 0)),
  w2_o = sum(case_when(w2_opened == "EMAIL_OPENED" ~ 1, TRUE ~ 0)),
  w3_o = sum(case_when(w3_opened == "EMAIL_OPENED" ~ 1, TRUE ~ 0))
) %>% unlist()

# sent emails count vectors for week 1-3
emails_sent <- data %>% summarize(
  w1_s = sum(case_when(w1_opened == "EMAIL_SENT" ~ 1, TRUE ~ 0)),
  w2_s = sum(case_when(w2_opened == "EMAIL_SENT" ~ 1, TRUE ~ 0)),
  w3_s = sum(case_when(w3_opened == "EMAIL_SENT" ~ 1, TRUE ~ 0))
) %>% unlist()

# sum vectors for total emails sent and opened
total <- emails_opened + emails_sent

# weekly email open rate
open_rate <- emails_opened * 100/total

# weekly email sent rate
sent_rate <- emails_sent * 100/total

data_f <- data.frame(
  Weeks = c("Week 1", "Week 2", "Week 3"),
  email_o = open_rate,
  email_s = sent_rate
)

# create diagram using ggplot
ggplot(data_f, aes(x = Weeks)) + 
  geom_bar(aes(y = emails_opened), stat = "identity", fill = "navy", color = "black", alpha = 0.9, position = "dodge", width = 0.9 ) +
  geom_bar(aes(y = emails_sent), stat = "identity", fill = "cyan", color = "black", alpha = 0.9, position = "dodge", width = 0.9) + 
  labs(title = "Weekly Emails Opened and Sent Rates for CSC148", x = "Weeks", y = "Rate (%)",fill = "Action") +
  scale_fill_manual(values = c("navy","cyan")) +
  theme_minimal() + 
  theme(panel.border = element_rect(color = "black", fill = NA),
        plot.title = element_text(hjust = 0.5, face = "bold", size = 12, family = "sans"),
        axis.title.x = element_text(face = "bold", size = 12, family = "sans"),
        axis.title.y = element_text(face = "bold", size = 12, family = "sans"),
        legend.position = "top")

