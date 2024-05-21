import pandas as pd
import facebook
import requests
from bs4 import BeautifulSoup as bs

url = f'https://symbolizationworld.com/blog/page/6/'
session = requests.Session()
response = session.get(url)

data = [] #All Data stored
soup = bs(response.text, 'html.parser')
posts = soup.find_all('div',{'class':'elementor-post__text'})
for post in posts:
    title = post.find('a').text.strip()
    post_url = post.find('a').get('href')
    # print(title)
    # print(post_url)
    data.append([title,post_url]) #data add
# Define headers based on the extracted data structure
    headers = ['title','post_url']
    df = pd.DataFrame(data, columns=headers)
    df.to_csv('message.csv', index=False)

# Configuration for Facebook Page post
csv_file_path = 'message.csv'  # Update this path to your CSV file
page_access_token = 'EAAPnuGYvFx0BO3kDc5ap74rcTYiO0FleeB8RK5Ls8x6FBgZBp83UQpNngNL10RKOB1BEpZB6MpllcNeUVZCrZCEHFaRBamzieZAb9kvUOlEC18aJGKUeYDek9hQYON8JhI89MvQAvVG8lHjSnazpk5iI5jQZArP6711uE4gwhqCa8xJJDOmn03Vy9NT9mvrVrYtGBzRedVDZB2SK0ybjePHF0AmYQZDZD'  # Replace with your actual Page Access Token
page_id = '341539205699083'  # Replace with your actual Page ID
# privacy = {'value':'EVERYONE'}
# Initialize the Facebook Graph API
graph = facebook.GraphAPI(access_token=page_access_token)

# Function to post a message to Facebook
def post_to_facebook(message,url):
    try:
        post = graph.put_object(parent_object='me', connection_name='feed',message=message,link=url)
        print(f"Successfully posted: {message}")
    except facebook.GraphAPIError as e:
        print(f"Failed to post: {message}")
        print(f"Error: {e}")

# Read CSV file
df = pd.read_csv(csv_file_path)

# Iterate through the DataFrame and post each message
for index, row in df.iterrows():
    message = row['title']# Adjust column name if necessary
    url = row['post_url']
    post_to_facebook(message,url) #Function Call for post