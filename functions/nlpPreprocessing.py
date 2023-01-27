import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string

myStopwords = stopwords.words("english")


def preprocess(text: str) -> str:

    text = re.sub(r'[0123456789]+', ' ', text)
    words = word_tokenize(text)
    words = [word.lower()
             for word in words if not word.lower() in myStopwords]

    text = ' '.join(words)
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    text = re.sub(r' +', ' ', text)
    return text
