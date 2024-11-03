from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import matplotlib.pyplot as plt

# Initialize URL extractor
extract = URLExtract()

def fetch_stats(selected_user, df):
    """Fetch various statistics for a given user or overall in the DataFrame."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]

    # Total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    """Find the most active users in the chat."""
    user_counts = df['user'].value_counts().head()
    user_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return user_counts, user_percent

def create_wordcloud(selected_user, df):
    """Create a word cloud from messages of a selected user."""
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stop_words])

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    """Find the most common words used in messages."""
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        words.extend([word for word in message.lower().split() if word not in stop_words])

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return most_common_df

def emoji_helper(selected_user, df):
    """Extract and count emojis from messages."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Using a list comprehension to gather emojis from messages
    emojis = [char for message in df['message'] for char in message if char in emoji.EMOJI_DATA]

    # Create a DataFrame with the count of each emoji
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.items(), columns=['emoji', 'count']).sort_values(by='count', ascending=False)

    return emoji_df

def monthly_timeline(selected_user, df):
    """Generate a monthly timeline of messages."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline

def daily_timeline(selected_user, df):
    """Generate a daily timeline of messages."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby('only_date').count()['message'].reset_index()

def week_activity_map(selected_user, df):
    """Generate activity map based on the day of the week."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    """Generate activity map based on the month."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    """Create a heatmap of user activity over the week."""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

def most_common_words(selected_user, df):
    """Find the most common words used in messages."""
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        words.extend([word for word in message.lower().split() if word not in stop_words])

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])  # Ensure this line is correct
    return most_common_df

# Example usage:
# df = pd.read_csv('your_chat_data.csv')  # Load your DataFrame here
# selected_user = 'Overall'  # or a specific user
# stats = fetch_stats(selected_user, df)
# most_common_df = most_common_words(selected_user, df)
# plot_most_common_words(most_common_df)
