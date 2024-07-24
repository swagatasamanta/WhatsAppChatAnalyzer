from urlextract import URLExtract
extract = URLExtract()  # Create an object of type URLExtract

from wordcloud import WordCloud
from collections import Counter
import pandas as pd 
import emoji


def fetch_stats(selected_user, df):
    # ------------------------------------------------------------------------------------------------
    # if selected_user == 'Overall':
    #     # 1. Fetch num of messages
    #     num_messages = df.shape[0]
    #     # 2. Fetch num of words
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())
            
    #     return num_messages, len(words)
    # else:
    #     new_df =  df[df['user'] == selected_user]
        
    #     num_messages = new_df.shape[0] # 1. Fetch num of messages
    #     words = [] # 2. Fetch num of words
    #     for message in new_df['message']:
    #         words.extend(message.split())
            
    #     return num_messages, len(words)
    # ------------------------------------------------------------------------------------------------
    # ----------- Let's simplify it, as dataframe is changeing only selected_user != Overall-------------
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user] # Change the df
    
    # 1. Fetch num of messages
    num_messages = df.shape[0]
    # 2. Fetch num of words
    words = []
    for message in df['message']:
        words.extend(message.split())
        
    # 3. Fetch num of media shared
    num_media_shared = df[df['message'] == '<Media omitted>\n'].shape[0]
     
    # 4. Fetch num of Links shared 
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
         
    return num_messages, len(words), num_media_shared, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    
    # Convert it into a dataFrame using ----> .reset_index()
    df = round((df['user'].value_counts() / df.shape[0])*100, 4).reset_index().rename(columns={'user':'Name', 'count':'Percentage'})
    
    return x, df 


#----------------- WordCloud (Without filtering) ----------------------

# def create_wordcloud(selecte_user, df):
    
#     if selecte_user != 'Overall':
#         df = df[df['user'] == selecte_user]
    
#     wc = WordCloud(width=500, height=500,min_font_size=10, background_color='white')
#     df_wc = wc.generate(df['message'].str.cat(sep=" ")) # Return an img
#     return df_wc

# ----------------- WordCloud (With filtering--> means remove group notifications and <Media Ommited>) -------------------

def create_wordcloud(selected_user, df):
    file = open("stop_hinglish.txt", 'r')
    stop_words = file.read()
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
        
    # Remove group_notification & <Media Omitted>\n
    temp = df[df['user'] != 'group_notification'] 
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        
        return " ".join(y)
        
    
    wc = WordCloud(width=500, height=500,min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" ")) # Return an img
    return df_wc


# ---------------- Most common words --------------------
 
def most_common_words(selected_user, df):
    file = open("stop_hinglish.txt", 'r')
    stop_words = file.read()
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
        
    # Remove group_notification & <Media Omitted>\n
    temp = df[df['user'] != 'group_notification'] 
    temp = temp[temp['message'] != '<Media omitted>\n']
     
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    
    return most_common_df


# ---------------- Emoji Analysis --------------

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA]) 

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df

# --------------- monthly timeline ----------------------
def monthly_timeline(seleted_user, df):
    if seleted_user != 'Overall':
        df = df[df['user'] == seleted_user]
        
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    # Now merge year and month
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
        
    return timeline            

# ------------ Daily Timeline ------------------
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index() 
    
    return daily_timeline

# ----------- Week activity map ---------------------
def weekly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    return df['day_name'].value_counts()

# ----------- Month activity map ---------------------
def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    return df['month'].value_counts()

# ------------ Activity HeatMap ----------------
def activity_heapmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    user_heatmap =  df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap