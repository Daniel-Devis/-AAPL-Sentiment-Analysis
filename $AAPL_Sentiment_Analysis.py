# Import libraries for Torch & NLP usage.
import torch
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import torch.nn.functional as F

# Initialise the FinBERT model and tokenizer
model_name = "yiyanghkust/finbert-tone" # FinBert model
model = AutoModelForSequenceClassification.from_pretrained(model_name) # Model for sequence classification tasks.
tokenizer = AutoTokenizer.from_pretrained(model_name) # Tokenizer that matches the pre-trained model.

# List of Apple-related headlines with sources
headlines = [
    "Apple’s $85bn-a-year services business faces legal reckoning - Financial Times",
    "Apple Stock Is Dropping Again. How It Can Get ‘Unstuck.’ - Barrons",
    "Apple Stock Got a New Bear Today. The Shares Dropped. - Wall Street Journal",
    "Apple hits seven-week low after Barclays downgrade on demand concerns - Reuters",
    "Apple Stock Downgraded as Barclays Warns on Cooling iPhone Demand - Bloomberg",
    "After Apple’s Stock Slide, Is Tech Due for a Correction? - Wall Street Journal",
    "Apple Stock Drops After Downgrade. What’s Causing Concern. - Barrons",
    "Short Interest in Apple Inc. (NASDAQ:AAPL) Rises By 8.7% - MarketBeat",
    "Apple’s stock suffers biggest drop in 4 months after ‘sell’ call from Barclays - MarketWatch",
    "Apple Inc. stock underperforms Tuesday when compared to competitors - MarketWatch",
    "Apple Stock Drops After Downgrade. What’s Causing Concern - Barrons",
    "Apple, the world’s most valuable stock, is about to start growing again - Financial Times",
    "China’s Luxshare expands Apple production capacity in deepening relationship - Financial Times",
    "Surveillance: Apple Trembles as Mystery Clouds Magnificent Seven - Bloomberg",
    "Is 2024 the Year US-China Tensions Finally Trip Up Apple - Bloomberg",
    "Why Apple and the Rest of the Magnificent 7 Aren’t the Big Risk Everyone Says They Are - Barrons",
    "Apple Downgrades Are Piling Up. The Latest One Hit the Stock Harder.- Barrons",
    "Apple, most valuable company in world and key member of ‘Magnificent 7,’ downgraded by Barclays - CNBC",
    "No reason to doubt Apple at this moment despite its recent slide - CNBC",
    "S&P, Nasdaq begin 2024 with lower close as Apple, big tech weighs - Reuters"
]

# Initialise a list to hold the sentiment scores
sentiment_scores = []

# Process each headline through FinBERT
for headline in headlines:
    headline_text = headline.split(" - ")[0] # Tokenize headlines: The headlines are split to separate the text from the source and are tokenized to be suitable for the model input.
    inputs = tokenizer(headline_text, return_tensors="pt", truncation=True, max_length=512) #  Tokenizer converts the text to the format expected by FinBERT.
    outputs = model(**inputs) # The tokenized input is fed into the model to get the raw output scores.
    probs = F.softmax(outputs.logits, dim=-1) # Use of softmax to convert output scores into probabilities representing the sentiment.
    sentiment_scores.append(probs) # Sentiment probabilities for headlines are added to the list.

# Convert the list of tensors to a tensor
sentiment_scores_tensor = torch.cat(sentiment_scores)

# Calculate and print the average sentiment scores
average_sentiment = torch.mean(sentiment_scores_tensor, dim=0)
print(average_sentiment)
