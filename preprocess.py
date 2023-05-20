import numpy as np 
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    msgs=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_msgs':msgs, 'date': pd.to_datetime(dates,format='%d/%m/%y, %H:%M - ')})
    usrs=[]
    msgs=[]
    for msg in df['user_msgs']:
        entry=re.split('([\w\W]+?):\s',msg)
        if entry[1:]:
            usrs.append(entry[1])
            msgs.append(entry[2])
        else:
            usrs.append('grp_notification')
            msgs.append(entry[0])


    df['users']=usrs
    df['msgs']=msgs
    df.drop('user_msgs',axis=1)
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    df['only_date'] = df['date'].dt.date
    # df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    # df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    # df['hour'] = df['date'].dt.hour
    # df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    senti_obj= SentimentIntensityAnalyzer()
    senti=[]
    for msg in df['msgs']:
        sentiment_dict = senti_obj.polarity_scores(msg)
        if sentiment_dict['compound'] >= 0.05 :
            senti.append("Positive")
 
        elif sentiment_dict['compound'] <= - 0.05 :
            senti.append("Negative")
 
        else :
            senti.append("Neutral")
    df['sentiments']=senti

    return df