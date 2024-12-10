from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

def clean_text(text_to_clean):
    text_data = text_to_clean
    text_data = text_data.lower()
    text_data = text_data.split()
    wl = WordNetLemmatizer()
    text_data = [wl.lemmatize(word) for word in text_data if not word in set(stopwords.words('english'))]
    text_data = [re.sub('[^A-Za-z0-9.-]+', '', word) for word in text_data if len(word) > 2]
    cleaned_text_words = []
    for word in text_data:
        if word.endswith('.'):
            text = word
            word = text[:text.rfind('.')] + text[text.rfind('.') + 1:]
            cleaned_text_words.append(word)
        else:
            cleaned_text_words.append(word)
    text_data = [word for word in cleaned_text_words if len(word) > 2]
    text_data = set(text_data)
    return text_data


def clean_dict(dict_data):
    text_data = dict_data
    text_data = text_data.lower().replace('}', '').replace('{', '').replace('"', '').replace('_', ' ').replace('\n',
                                                                                                               ' ').replace(
        '\t', ' ').replace(':', '').replace(',', '')
    return text_data
