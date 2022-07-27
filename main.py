import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import twitter_api
import analysis

import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Twitter Data Collection and Basic Analysis')
st.write('Be Sure you have a twitter developer account. \n')
token = st.text_input('*Token')
keyword = st.text_input('*Keyword',
                        '5G (Tower OR antenna) (Covid-19 OR coronavirus OR covid19 OR Corona OR newcoronavirus)')
start_date = st.text_input('Start Date')
end_date = st.text_input('End Date')

if st.button('Send Query'):
    df = twitter_api.send_request(token, keyword, start_date, end_date)
    topics = analysis.get_topic(df)
    st.write(topics)
else:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_json(uploaded_file)
        topics = analysis.get_topic(df)
        st.write(topics.show_topics(10))
st.write('The App will show top 5 Topics but possible to find the best fit model numbers and have that '
         'number of topics')

# Generate word cloud from the text
if st.button('Generate Graph'):
    text = analysis.word_cloud(df)
    wc = WordCloud(background_color="white",
                   max_words=350,
                   width=1000,
                   height=600,
                   random_state=1).generate(text)

    fig = plt.figure(figsize=(10, 4))
    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    st.write('Word cloud from the tweets')
    st.pyplot(fig)

    dates = analysis.time_graph(df)
    fig1 = plt.figure(figsize=(10, 4))
    fig1, bx = plt.subplots()
    bx.set_xlabel('Date')
    bx.set_ylabel('Number of Tweets')
    bx.plot(dates['created_at'], dates['count'])
    bx.set_xticklabels(dates.created_at[::30])
    st.write('Tweets occured over the period')
    st.pyplot(fig1)
