import pandas as pd
import gensim
import spacy
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel, LdaModel, LsiModel, HdpModel
import matplotlib.pyplot as plt
import streamlit as st

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
my_stop_words = [u'say', u'\'s', u'Mr', u'be', u'\n ', u'\\n', u'\n\n', u"\\n\\n", u" \n", u't', u'p', u'th', u'_',
                 u'have', u've']  # can include specific words to remove
for stopword in my_stop_words:
    lexeme = nlp.vocab[stopword]
    lexeme.is_stop = True


def get_topic(df):
    # Remove urls and amp
    df['text'] = df['text'].str.replace(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ')
    df['text'] = df['text'].str.replace('amp', ' ')
    text = df['text']
    lemmatized_texts = lemmatization(text)
    data_words = gen_words(lemmatized_texts)
    dictionary = Dictionary(data_words)
    corpus = [dictionary.doc2bow(text) for text in data_words]
    # model_list, coherence_values = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=data_words,
    # start=2, limit=10, step=1)

    # Show graph
    # limit = 10
    # start = 2
    # step = 1
    # x = range(start, limit, step)
    # plt.plot(x, coherence_values)
    # plt.xlabel("Num Topics")
    # plt.ylabel("Coherence score")
    # plt.legend(("coherence_values"), loc='best')
    # st.pyplot(plt)  # Print the coherence scores
    # highest_coherence = coherence_values.index(max(coherence_values)) + 1
    ldamodel = LdaModel(corpus=corpus, num_topics=5, id2word=dictionary)
    return ldamodel


def lemmatization(texts, allowed_postags=["NOUN", "ADJ", "VERB", "ADV", 'OBJ']):
    texts_out = []
    for text in texts:
        doc = nlp(text)
        new_text = []
        for token in doc:
            if token.pos_ in allowed_postags:
                new_text.append(token.lemma_)
        final = " ".join(new_text)
        texts_out.append(final)
    return texts_out


def gen_words(texts):
    final = []
    for text in texts:
        new = gensim.utils.simple_preprocess(text, deacc=True)
        final.append(new)
    return final


def compute_coherence_values(dictionary, corpus, texts, limit, start, step):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values


def word_cloud(df):
    df['text'] = df['text'].str.replace(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ')
    df['text'] = df['text'].str.replace('amp', ' ')
    text = ' '.join(df.text)
    nlp.max_length = len(text)
    doc = nlp(text)
    norm_text = []
    for token in doc:
        if not token.is_punct and not token.is_stop:
            norm_text.append(token.lemma_.lower())
    return ' '.join(norm_text)


def time_graph(df):
    # Changing object type column to datetime
    df['created_at'] = pd.to_datetime(df.created_at)
    df['date'] = df['created_at'].dt.date
    df_1 = pd.DataFrame({'created_at': df['date']})
    df_1['count'] = df_1.groupby('created_at')['created_at'].transform('count')
    df_1 = df_1.drop_duplicates()
    return df_1
