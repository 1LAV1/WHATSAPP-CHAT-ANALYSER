import pandas as pd
import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud  import  WordCloud
extracter=URLExtract()
from collections import Counter
import emoji as em
def fetch_stats(selected_user,df):
    if selected_user!='overall':
        df = df[df['Name']==selected_user]
    # total messages
    nums_messages=df.shape[0]
    # total words
    words = []
    for message in df['Message']:
        words.extend(message.split())
    num_words = len(words)
    # total media
    num_media_files=df[df['Message']=='<Media omitted'].shape[0]

    # total links shared
    y = []
    for message in df['Message']:
        y.extend(extracter.find_urls(message))
    num_links=len(y)
    return nums_messages,num_words,num_media_files,num_links



def most_busy_users(df):
    x = df['Name'].value_counts().head()
    df=round((df['Name'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','Name':'Percent'})

    return x,df

def most_common_words(selected_user,df):
    if selected_user != 'overall':
        df = df[df['Name'] == selected_user]
    temp = df[df['Message'] != 'This message was deleted']
    temp = temp[temp['Message'] != '<Media omitted']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    f.close()
    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    word_df=pd.DataFrame(Counter(words).most_common(20))
    return word_df

def extract_emojis(selected_user,df):

    temp = df[df['Message'] != 'This message was deleted']
    temp = temp[temp['Message'] != '<Media omitted']
    emojis = []
    for message in temp['Message']:
        emojis.extend([c for c in message if c in em.distinct_emoji_list(message)])
    return emojis

def daily_timeline(selected_user,df):
    if selected_user != 'overall':
        df = df[df['Name'] == selected_user]
    daily_timeline_df = df.groupby('date').count()['Message'].reset_index()
    return daily_timeline_df

def monthly_timeline(selected_user,df):
    if selected_user != 'overall':
        df = df[df['Name'] == selected_user]
    timeline = df.groupby(['year', 'month', 'month_name']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_activity_map(selected_user,df):
    if selected_user != 'overall':
        df = df[df['Name'] == selected_user]
    daily_active_df = df.groupby('day_name').count()['Message'].reset_index()
    return daily_active_df

def monthly_activity_map(selected_user,df):
    if selected_user != 'overall':
        df = df[df['Name'] == selected_user]
    monthly_active_df = df.groupby('month_name').count()['Message'].reset_index()
    return monthly_active_df


def word_cloud(selected_user, df):
    # Filter the DataFrame based on the selected user
    if selected_user != 'overall':
        df = df[df['Name'] == selected_user]
    temp = df[df['Message'] != 'This message was deleted']
    temp = temp[temp['Message'] != '<Media omitted']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    f.close()

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)



    temp['Message'].apply(remove_stopwords)
    temp['Message'] = temp['Message'].astype(str)

    # Concatenate all messages into a single string
    text = ' '.join(temp['Message'].dropna().values)

    # Check if the text is empty
    if not text.strip():
        raise ValueError("We need at least 1 word to plot a word cloud, got 0.")

    # Generate the word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black').generate(text)
    return wc













