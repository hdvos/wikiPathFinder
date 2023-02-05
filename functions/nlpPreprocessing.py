import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string

myStopwords = stopwords.words("english")


def preprocess(text: str) -> str:
    """ Preprocesses the text by removing numbers, stopwords, punctuation and extra spaces.

    :param text: Text to be preprocessed
    :type text: str
    :return: Preprocessed text
    :rtype: str
    """    

    # Remove all numbers
    text = re.sub(r'[0123456789]+', ' ', text)
    # Word tokenization
    words = word_tokenize(text)
    # Remove stopwords
    words = [word.lower()
             for word in words if not word.lower() in myStopwords]

    # Remove punctuation
    text = ' '.join(words)
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    
    # Remove extra spaces
    text = re.sub(r' +', ' ', text)
    return text
