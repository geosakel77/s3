"""
<Cyber Threat Intelligence Relevance and Actionability Quality Metrics Implementation.>
    Copyright (C) 2025  Georgios Sakellariou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
    return custom_clean(text_data)


def custom_clean(text_data):
    custom_stopwords = ['opencti', 'report', 'enhanced', 'related', 'created', 'reference', 'name', 'types',
                        'description', 'indicators', 'observables', 'attack', 'patterns', 'malware', 'relationships',
                        'campaigns', 'external', 'statistical', 'analysis','pdf','generated']
    clean_data = []
    for word in text_data:
        check_flag = False
        for sw in custom_stopwords:
            if sw in word:
                check_flag = False
                break
            else:
                check_flag = True
        if check_flag:
            clean_data.append(word)
    return clean_data


def clean_dict(dict_data):
    text_data = dict_data
    text_data = text_data.lower().replace('}', '').replace('{', '').replace('"', '').replace('_', ' ').replace('\n',
                                                                                                               ' ').replace(
        '\t', ' ').replace(':', '').replace(',', '')
    return text_data
