# from urlextract import URLExtract
# import pandas as pd
# from collections import Counter

# extract = URLExtract()

# def fetch_stats(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]


#     num_messages = df.shape[0]

#     words = []
#     for message in df['message']:
#         words.extend(message.split())

#     num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

#     links = []
#     for message in df['message']:
#         links.extend(extract.find_urls(message))

#     return num_messages,len(words),num_media_messages,len(links)


# def most_common_words(selected_user,df):

#     f = open('stop_hinglish.txt','r')
#     stop_words = f.read()

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']

#     words = []

#     for message in temp['message']:
#         for word in message.lower().split():
#             if word not in stop_words:
#                 words.append(word)

#     most_common_df = pd.DataFrame(Counter(words).most_common(30))
#     return most_common_df


# def monthly_timeline(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

#     time = []
#     for i in range(timeline.shape[0]):
#         time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

#     timeline['time'] = time

#     return timeline
# def help_most_busy_month(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
#     time = []
#     for i in range(timeline.shape[0]):
#         time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

#     timeline['time'] = time
#     return timeline

# def week_activity_map(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     return df['day_name'].value_counts()

# def month_activity_map(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     return df['month'].value_counts()

# def solve(df,z):

#     months = df["month"].unique()
#     years = df["year"].unique()

# # Create an empty dictionary to store the number of messages sent in each month
#     month_dict = {}

# # Iterate through each month and year combination
#     for month in months:
#         month_dict[month] = {}
#         for year in years:
#             month_dict[month][year] = 1

# # Fill the dictionary with the actual message count
#     for index, row in df.iterrows():
#         month = row["month"]
#         year = row["year"]
#         month_dict[month][year] =row["message"]
#     return month_dict


# def solve2(df,y,m):
#     k=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
#     p=dict()
#     t = df.groupby(['year', 'month_num', 'month','day_name']).count()['message'].reset_index()
#     for i in k:
#        l=list()
#        for j in range(t.shape[0]):
#            if t['year'][j]==y and t['month'][j]==m and t['day_name'][j]==i:
#             l.append(t['message'][j])
#        p[i]=l
#     return p
        

from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt # Importing the 3D toolkit
import demoji
extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. number of messages
    num_messages = df.shape[0]

    # 2. number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. number of link shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)


def most_busy_users(df):
    df_filtered = df[df['user'] != 'group_notification']
    x = df_filtered['user'].value_counts().head()
    df_result = round((df_filtered['user'].value_counts() / df_filtered.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})

    return x, df_result



def create_wordcloud(selected_user,df):
    
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    

    wc = WordCloud(width=700,height=700,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Function to remove emojis from a message
    def remove_emojis(message):
        return demoji.replace(message, '')

    # Create a new DataFrame with the 'message' column having emojis removed
    temp_no_emojis = temp.copy()
    temp_no_emojis['message'] = temp_no_emojis['message'].apply(remove_emojis)

    words = []

    for message in temp_no_emojis['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap    

def solve(df,y):
    k=['January','February','March','April','May','June','July','August','September','October','November','December']
    p=dict()
    for i in k:
       l=list()
       for j in range(df.shape[0]):
           if df['year'][j]==y and df['month'][j]==i:
            l.append(df['message'][j])
       p[i]=l
    return p

def solve2(df,y,m,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    k=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    p=dict()
    t = df.groupby(['year', 'month_num', 'month','day_name']).count()['message'].reset_index()
    print(t)
    for i in k:
       l=list()
       for j in range(t.shape[0]):
           if t['year'][j]==y and t['month'][j]==m and t['day_name'][j]==i:
            l.append(t['message'][j])
       p[i]=l
    return p



    





    