# Bayesian Tomatoes:
# Doing some Naive Bayes and Markov Models to do basic sentiment analysis.
#
# Input from train.tsv.zip at
# https:#www.kaggle.com/c/sentiment-analysis-on-movie-reviews
#
# itself gathered from the Rotten Tomatoes movie review aggregation site.
#
# Format is PhraseID[unused]   SentenceID  Sentence[tokenized] Sentiment
#
# We'll only use the first line for each SentenceID, since the others are
# micro-analyzed phrases that would just mess up our counts.
#
# Sentiment is on a 5-point scale:
# 0 - negative
# 1 - somewhat negative
# 2 - neutral
# 3 - somewhat positive
# 4 - positive
#
# For each kind of model, we'll build one model per sentiment category.
# Following Bayesian logic, base rates matter for each category; if critics
# are often negative, that should be a good guess in the absence of other
# information.
#
# Training input is assumed to be in a file called "train.tsv"
#
# Test sentences are received via stdin (thus either interactively or with input redirection).
# Output for each line of input is the following:
#
# Naive Bayes classification (0-4)
# Naive Bayes most likely class's log probability (with default double digits/precision)
# Markov Model classification (0-4)
# Markov Model most likely class's log probability

import sys
import math

# NLTK is a great toolkit that makes Python a nice choice for natural language processing (NLP)
# ... although to use this tokenizer, you will first need to
# >>> import nltk
# >>> nltk.download('punkt')
# ... to get the dataset it relies on
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
# Note that bigrams() returns an *iterator* and not a *list* - you will need to call it
# again or store as a list to iterate over the bigrams multiple times
from nltk.util import bigrams

CLASSES = 5
# Assume sentence numbering starts with this number in the file

FIRST_SENTENCE_NUM = 1
# Probability of either a unigram or bigram that hasn't been seen -
# needs to be small enough that it's "practically a rounding error"
OUT_OF_VOCAB_PROB = 0.0000000001


# tokenize():  get words from a line in a consistent way
# uses NLTK, standardizes to lowercase
# returns list of tokens
def tokenize(sentence):
    return [t.lower() for t in word_tokenize(sentence)]


class ModelInfo:
    # ModelInfo fields:
    # word_counts:  5 dicts from string to int, one per sentiment, in a list
    # bigram_counts: same
    # sentiment_counts:  list containing counts of the sentences with different sentiments
    # total_words:  list of counts of words for each sentiment
    # bigram_denoms:  Separate counts of how often a word starts a bigram, again one per sentiment.
    #   (Not quite the same as the word count since last words of sentences aren't counted here)
    # total_bigrams: counts of total bigrams for each sentiment level

    def __init__(self):
        self.word_counts = [{}, {}, {}, {}, {}]
        self.bigram_counts = [{}, {}, {}, {}, {}]
        self.sentiment_counts = [0, 0, 0, 0, 0]
        self.total_words = [0, 0, 0, 0, 0]
        self.bigram_denoms = [{}, {}, {}, {}, {}]
        self.total_bigrams = [0, 0, 0, 0, 0]
        self.total_examples = 0

    # update_word_counts
    # assume space-delimited words/tokens.
    #
    # To "tokenize" the sentence we'll make use of NLTK, a widely-used Python natural language
    # processing (NLP) library.  This will handle otherwise onerous tasks like separating periods
    # from their attached words.  (Unless the periods are decimal points ... it's more complex
    # than you might think.)  The result of tokenization is a list of individual strings that are
    # words or their equivalent.
    #
    # Note that sentiment is an integer, not a string, matching the data format
    def update_word_counts(self, sentence, sentiment):
        # Get the relevant dicts for the sentiment
        s_word_counts = self.word_counts[sentiment]
        s_bigram_counts = self.bigram_counts[sentiment]
        s_bigram_denoms = self.bigram_denoms[sentiment]
        tokens = tokenize(sentence)
        for token in tokens:
            self.total_words[sentiment] += 1
            s_word_counts[token] = s_word_counts.get(token, 0) + 1
        my_bigrams = bigrams(tokens)
        for bigram in my_bigrams:
            s_bigram_counts[bigram] = s_bigram_counts.get(bigram, 0) + 1
            s_bigram_denoms[bigram[0]] = s_bigram_denoms.get(bigram[0], 0) + 1
            self.total_bigrams[sentiment] += 1


# get_models:  returns a model_info object
def get_models():
    next_fresh = FIRST_SENTENCE_NUM
    info = ModelInfo()
    for line in sys.stdin:
        if line.startswith("---"):
            return info
        fields = line.split("\t")
        try:
            sentence_num = int(fields[1])
            if sentence_num != next_fresh:
                continue
            next_fresh += 1
            sentiment = int(fields[3])
            info.sentiment_counts[sentiment] += 1
            info.total_examples += 1
            info.update_word_counts(fields[2], sentiment)
        except ValueError:
            # Some kind of bad input?  Unlikely with our provided data
            continue
    return info


# classify_sentences:  takes a ModelInfo, reads sentences from stdin, prints
# their classification info for the two models
def classify_sentences(info):
    for line in sys.stdin:
        nb_class, nb_logprob = naive_bayes_classify(info, line)
        mm_class, mm_logprob = markov_model_classify(info, line)
        print(nb_class)
        print(nb_logprob)
        print(mm_class)
        print(mm_logprob)

    # naive_bayes_classify:  takes a ModelInfo containing all counts necessary for classsification


# and a String to be classified.  Returns a number indicating sentiment and a log probability
# of that sentiment (two comma-separated return values).
def naive_bayes_classify(info, sentence):
    # TODO
    prob_list = []
    tokens = tokenize(sentence)
    for index, value in enumerate(info.sentiment_counts):
        p = 0
        for token in tokens:
            if token in info.word_counts[index].keys():
                p += math.log(info.word_counts[index][token] / info.total_words[index])
            else:
                p += math.log(OUT_OF_VOCAB_PROB)
        p += math.log(info.sentiment_counts[index] / sum(info.sentiment_counts))
        prob_list.append(p)
    k, v = prob_list.index(max(prob_list)), max(prob_list)
    return k, v  # best class, log probability


# markov_model_classify:  like naive Bayes, but now use a bigram model.  First word
# still uses unigram count & probability.
def markov_model_classify(info, sentence):
    # TODO
    prob_list = []
    tokens = tokenize(sentence)
    for index, value in enumerate(info.sentiment_counts):
        p = 0
        if tokens[0] in info.word_counts[index].keys():
            p += math.log(info.word_counts[index][tokens[0]] / info.total_words[index])
        else:
            p += math.log(OUT_OF_VOCAB_PROB)
        i = 1
        while i < len(tokens):
            if (tokens[i-1],tokens[i]) in info.bigram_counts[index].keys():
                p += math.log(math.log(info.bigram_counts[index][(tokens[i-1],tokens[i])] / info.bigram_denoms[index][tokens[i-1]]))
            else:
                p += math.log(OUT_OF_VOCAB_PROB)
            i += 1
        p *= info.sentiment_counts[index] / sum(info.sentiment_counts)
        prob_list.append(p)
    k, v = prob_list.index(max(prob_list)), max(prob_list)

    return k, v  # best class, log probability


if __name__ == "__main__":
    info = get_models()
    classify_sentences(info)
