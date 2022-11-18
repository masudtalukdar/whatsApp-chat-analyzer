from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
extract = URLExtract()
import emoji

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #fetch the number of messages
    num_messages = df.shape[0]  

    #fetch the total number of words  
    words = []
    for message in df['message']:
            words.extend(message.split())

    #fetch number of media messages
    new_media_messages = df[df['message'] == '<Media omited>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),new_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head() 
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','user':'Percent'})

    return x,df

#wordcloud function
def create_wordcloud(selected_user,df):
    # if selected_user != 'Overall':
    #     df = df[df['user'] == selected_user]


    # wc = WordCloud(width = 800,height=400, min_font_size=10,background_color ='white')
    # df_wc = wc.generate(df['message'].str.cat(sep=" "))
    # return df_wc
    f = open('stopwords-en.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # nested function remove stop words
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
            return " ".join(y)

    wc = WordCloud(width = 800,height=400, min_font_size=10,background_color ='black')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc



#Most common word function
def most_common_words(selected_user,df):

    f = open('stopwords-en.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

    #emoji function
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
            emojis.extend([c for c in message if c in  emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df