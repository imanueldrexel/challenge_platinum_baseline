import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation

stopwords_list = stopwords.words('indonesian')
abusive = pd.read_csv('data/abusive.csv', encoding='utf-8')
new_kamusalay = pd.read_csv('data/new_kamusalay.csv', encoding='latin1')
new_kamus_alay = {}
for k,v in new_kamusalay.values:
    new_kamus_alay[k] = v


def processing_word(input_text):
    new_text = [] # set up new list
    new_new_text = [] # set up new new list
    text = input_text.split(" ") # split input_text menjadi list of words
    for word in text: # untuk setiap word in 'text'
        if word in abusive['ABUSIVE'].tolist(): # check word di dalam list_of_abusive_words
            continue # jika ada, skip
        else:
            new_text.append(word) # jika tidak ada, masukkan ke dalam list new_text
   
    for word in new_text:
        new_word = new_kamus_alay.get(word, word) # check ke new_kamus_alay, apakah word ada di dictionarynya. kalau ga ada, return word yang sama. kalau ada, kembalikan value barunya (value yang ada di dict)
        new_new_text.append(new_word)
    
    text = " ".join(new_new_text)
    return text

def processing_text(input_text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', 'EMAIL', input_text) #ganti email ke kata 'EMAIL'
    text = text.lower() # jadikan lowercase semua
    text = re.sub(r'[^\w\s]', '', text) # hapus semua punctuation (tanda baca)
    text = text.replace(" 62"," 0")
    text = re.sub(r"\b\d{4}\s?\d{4}\s?\d{4}\b", "NOMOR_TELEPON", text) #ganti nomor telepon ke kata 'NOMOR_TELEPON'
    text = text.replace("USER","")
    text = text.strip()
    
    text = processing_word(text)
    return text

def menghilangkan_stopwords(paragraph):
    tokenized_paragraph = word_tokenize(paragraph)
    new_tokenized_paragraph = []
    for token in tokenized_paragraph:
        if token in stopwords_list:
            continue
        elif token not in stopwords_list:
            new_tokenized_paragraph.append(token)
    
    return " ".join(new_tokenized_paragraph)

def lowercasing(paragraph):
    return paragraph.lower()

def menghilangkan_tandabaca(paragraph):
    new_paragraph = re.sub(fr'[{punctuation}]', r'', paragraph)
    return new_paragraph

def menghilangkan_link(paragraph):
    new_paragraph = re.sub(r'([a-zA-Z0-9]+)?(\.[a-zA-Z0-9]+)(\.[a-zA-Z]{2,3})(\.[a-zA-Z]{2,2})?', r'LINK_WEBSITE ', paragraph)
    new_paragraph = new_paragraph.replace("liputan6.com , ","LINK_WEBSITE ")
    return new_paragraph

def text_normalization(paragraph):
    paragraph = lowercasing(paragraph)
    paragraph = menghilangkan_stopwords(paragraph)
    paragraph = menghilangkan_link(paragraph)
    paragraph = menghilangkan_tandabaca(paragraph)
    paragraph = re.sub(r"[ ]+",r' ',paragraph)
    return paragraph