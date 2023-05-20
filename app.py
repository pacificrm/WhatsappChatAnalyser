import streamlit as st
import matplotlib.pyplot as plt
import preprocess, function
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")
upload_file = st.sidebar.file_uploader("Chosse a file")
if upload_file is not None:
  bytes_data=upload_file.getvalue()
  data=bytes_data.decode('utf-8')
  df=preprocess.preprocess(data)
  # st.dataframe(df)
  users=df['users'].unique().tolist()
  users.remove('grp_notification')
  users.sort()
  users.insert(0,'Overall')
  selected_user = st.sidebar.selectbox("Show analysis wrt",users)
  
  if st.sidebar.button('Show Analysis'):
    num_msgs,words,media,links=function.stats(selected_user,df)
    st.title("Top Statistics")
    col1,col2,col3,col4=st.columns(4)
    with col1:
      st.header("Total Messages")
      st.title(num_msgs)
    with col2:
      st.header("Total Words")
      st.title(words)
    with col3:
      st.header("Total Media")
      st.title(media)
    with col4:
      st.header("Total Links")
      st.title(links)  

     # monthly timeline
    st.title("Monthly Timeline")
    timeline = function.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['msgs'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

        # daily timeline
    st.title("Daily Timeline")
    daily_timeline = function.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['msgs'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

        # activity map
    st.title('Activity Map')
    col1,col2 = st.columns(2)
    with col1:
      st.header("Most busy day")
      busy_day = function.week_activity_map(selected_user,df)
      fig,ax = plt.subplots()
      ax.bar(busy_day.index,busy_day.values,color='purple')
      plt.xticks(rotation='vertical')
      st.pyplot(fig)

    with col2:
      st.header("Most busy month")
      busy_month = function.month_activity_map(selected_user, df)
      fig, ax = plt.subplots()
      ax.bar(busy_month.index, busy_month.values,color='orange')
      plt.xticks(rotation='vertical')
      st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = function.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    st.header("Users Sentiments")
    senti = function.sentiments(selected_user, df)
    fig, ax = plt.subplots()
    ax.bar(senti['sentiments'], senti['msgs'],color='red')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)



    if selected_user =='Overall':
      st.title('Most Busy Users')
      x,nd=function.busyusers(df)
#       fig,ax=plt.subplots()
      col1,col2=st.columns(2)
      with col1:
#         st.bar_chart(x=x.values,y=x.index)
        st.bar_chart(x)
#         ax.bar(x.index,x.values)
#         st.pyplot(fig)
      with col2:
        st.dataframe(nd)

    st.title('Word Cloud')
    df_wc=function.wordcld(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    
    st.title('Most Used Words')
    most_used_words=function.most_used_words(selected_user,df)
    fig,ax = plt.subplots()

    ax.barh(most_used_words[0],most_used_words[1])
    plt.xticks(rotation='vertical')

    # st.title('Most commmon words')
    st.pyplot(fig)
    # st.dataframe(most_used_words)
    # st.bar_chart(most_used_words)
    emoji_df = function.emoji_fun(selected_user,df)
    st.title("Emoji Analysis")
    col1,col2 = st.columns(2)
    with col1:
      st.dataframe(emoji_df)
    with col2:
      fig,ax = plt.subplots()
      ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct="%0.2f")
      st.pyplot(fig)
    if selected_user =='Overall':
      st.title('Most Positive User')
      pos=function.most_positive_usr(df)
      # st.dataframe(pos)
      fig, ax = plt.subplots()
      ax.bar(pos['user_name'], pos['positive_msgs'], color='cyan')
      plt.xticks(rotation='vertical')
      st.pyplot(fig)

      st.title('Most Negative User')
      neg=function.most_negative_usr(df)
      # st.dataframe(pos)
      fig, ax = plt.subplots()
      ax.bar(neg['user_name'], neg['negative_msgs'], color='magenta')
      plt.xticks(rotation='vertical')
      st.pyplot(fig)
                       
  
               