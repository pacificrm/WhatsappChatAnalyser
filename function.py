import re
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def stats(user,df):
    if user != 'Overall':
        df=df[df['users']==user]
    total_msgs=df.shape[0]
    words=[]
    for msgs in df['msgs']:
        words.extend(msgs.split())
    media=df[df['msgs']=='<Media omitted>\n'].shape[0]
#     from urlextract import URLExtract
#     extr=URLExtract()
#     links=[]
#     for msgs in df['msgs']:
#         links.extend(extr.find_urls(msgs))
    nlinks=[]
    for msgs in df['msgs']:
        ck=re.search("(?P<url>https?://[^\s]+)", msgs)
        if ck:
            nlinks.append(ck.group("url"))
    return total_msgs,len(words),media,len(nlinks)
    

def busyusers(df):
    ndf=df[df['users']!='grp_notification']
    x=ndf['users'].value_counts().head(10)
    nd=round((ndf['users'].value_counts()/ndf.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,nd

def wordcld(user,df):
    if user != 'Overall':
        df=df[df['users']==user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    temp = df[df['users'] != 'grp_notification']
    temp = temp[temp['msgs'] != '<Media omitted>\n']
    temp = temp[temp['msgs'] != 'This message was deleted\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    # temp = df[df['users'] != 'grp_notification']
    # temp = temp[temp['msgs'] != '<Media omitted>\n']
    
    # temp = temp[temp['msgs'] != '<Media omitted>\n']
    temp['msgs'] = temp['msgs'].apply(remove_stop_words)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(temp['msgs'].str.cat(sep=" "))
    return df_wc



def most_used_words(user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if user != 'Overall':
        df = df[df['users'] == user]

    temp = df[df['users'] != 'grp_notification']
    temp = temp[temp['msgs'] != '<Media omitted>\n']
    temp = temp[temp['msgs'] != 'This message was deleted\n']

    words = []

    for message in temp['msgs']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_used_df = pd.DataFrame(Counter(words).most_common(20))
    return most_used_df

def emoji_fun(user,df):
    if user != 'Overall':
        df = df[df['users'] == user]

    emojis = []
    for message in df['msgs']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['msgs'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(user,df):

    if user != 'Overall':
        df = df[df['users'] == user]

    daily_timeline = df.groupby('only_date').count()['msgs'].reset_index()

    return daily_timeline

def week_activity_map(user,df):

    if user != 'Overall':
        df = df[df['users'] == user]

    return df['day_name'].value_counts()

def month_activity_map(user,df):

    if user != 'Overall':
        df = df[df['users'] == user]

    return df['month'].value_counts()

def activity_heatmap(user,df):

    if user != 'Overall':
        df = df[df['users'] == user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='msgs', aggfunc='count').fillna(0)

    return user_heatmap

def sentiments(user,df):
    if user != 'Overall':
        df = df[df['users'] == user]
    senti = df.groupby('sentiments').count()['msgs'].reset_index()
    return senti

def most_positive_usr(df):
    df = df[df['users'] != 'grp_notification']
    usr=df[df['sentiments']=='Positive']['users'].value_counts().head(10).reset_index().rename(columns={'users':'user_name','count':'positive_msgs'})
    return usr

def most_negative_usr(df):
    df = df[df['users'] != 'grp_notification']
    usr=df[df['sentiments']=='Negative']['users'].value_counts().head(10).reset_index().rename(columns={'users':'user_name','count':'negative_msgs'})
    return usr

