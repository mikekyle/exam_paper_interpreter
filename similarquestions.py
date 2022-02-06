#%%
import numpy as np
import pandas as pd
import nltk
import re
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#Read in fulldf.csv to df
def get_df():
    fulldf = pd.read_csv('fulldf.csv', index_col=0)
    return fulldf

# lem = nltk.stem.wordnet.WordNetLemmatizer()
# ps = nltk.stem.porter.PorterStemmer()

def mk_tok(sentence):
    words = nltk.tokenize.word_tokenize(sentence)
    words = [re.sub(r'[^a-zA-Z]+','', word) for word in words]
    words = [word for word in words if len(word)>1]
    stems = words#[ps.stem(x) for x in words]
    return stems
    #return list(nltk.everygrams(stems, max_len=7))

def get_stopwords():
    my_stop_words = set(nltk.corpus.stopwords.words("english"))
    my_stop_words |= {'may', 'becau'}
    my_stop_words |= set(mk_tok(' '.join(my_stop_words)))
    return my_stop_words

def get_vectoriser_transformer():
    my_stop_words = get_stopwords()
    fulldf = get_df()
    qvect = TfidfVectorizer(stop_words=my_stop_words,tokenizer=mk_tok)#nltk.tokenize.word_tokenize)
    q_tfidf = qvect.fit_transform(fulldf.question_text)
    return (qvect, q_tfidf)

def collapsep(title,p):
    return f'<details><summary>{title}</summary><p>{p}</p></details>'

def similar_qs(text,response_no=10,include_identical=True):
    fulldf = get_df()
    qvect, q_tfidf = get_vectoriser_transformer()
    cosine_similarities = linear_kernel(qvect.transform([text]), q_tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-(response_no+1):-1]
    #print(np.sort(cosine_similarities)[:-response_no:-1])
    htmlout = ''
    for i in related_docs_indices:
        title = f'{fulldf.full_date[i]} - Q{fulldf.question_no[i]} - ({cosine_similarities[i]:.2%} match)'
        contents = fulldf.question_text[i].replace('\n','<br>')
        contents += '<br>' + ('-'*70) + '<br>'
        contents += fulldf.answer_text[i].replace('\n','<br>')
        htmlout += collapsep(title,contents)
    return htmlout

# %%
