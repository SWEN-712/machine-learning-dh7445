import sys
from tweepy import OAuthHandler
from tweepy import API
import tweepy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import requests
from difflib import SequenceMatcher


# region Similarity function
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
# endregion

# region webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), options=chrome_options)
# endregion

# region Twitter API keys
consumer_key = "YOUR TWITTER API KEY"  # twitter app’s API Key
consumer_secret = "YOUR TWITTER API SECRET KEY"  # twitter app’s API secret Key
access_token = ""  # twitter app’s Access token
access_token_secret = ""  # twitter app’s access token secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)
# endregion

# region ComputerVision Keys
# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print(
        "\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "vision/v2.1/analyze"
headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params = {'visualFeatures': 'Categories,Description,Color'}

# endregion

# tweets = auth_api.user_timeline(screen_name="MSFTEnable", count=250, include_rts=True,
#                                       tweet_mode="extended", )
tweets = tweepy.Cursor(auth_api.user_timeline, screen_name='@googleaccess', tweetmode='extended', include_rts=True,
                       count=1000).items()

tweets_images_urls = []
total_tweets = 0

# region GetTweets
for tweet in tweets:
    total_tweets += 1
    if 'extended_entities' in tweet._json:
        for media in tweet._json["extended_entities"]['media']:
            if media['type'] == 'photo':
                image_complete_url = media["media_url_https"]
                image_url_code = media["media_url_https"].split("/media/")[1].split(".")[0]
                post_url = media["expanded_url"]
                tweets_images_urls.append([image_url_code, post_url, image_complete_url])
# endregion

images_alt_text = []
analyzed_tweets = 0

# region GetAltTexts
for tweet_image in tweets_images_urls:
    try:
        driver.get(tweet_image[1])
        wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//img[contains(@src, "{tweet_image[0]}")]'))
        )
        alt_text = wait.get_attribute("alt")
        if alt_text != "Image" and alt_text != "":
            images_alt_text.append([alt_text, tweet_image[2]])
        analyzed_tweets += 1
    except:
        continue
driver.quit()
# endregion

print(f"Total Tweets: {total_tweets}")
print(f"Total Analyzed Tweets: {analyzed_tweets}")
print(f"Tweets with photos: {len(tweets_images_urls)} photos out of {analyzed_tweets} tweets")
print(f"Photos with alt text: {len(images_alt_text)} out of {len(tweets_images_urls)}")

if len(images_alt_text) == 0:
    print("None of the images had alternative text! :(")
    sys.exit()


image_caption = []

# region Get Caption from Azure
# limited to 20 as per free API calls is limited to 20 per min.
for tweet_image in images_alt_text[0:19]:
    image_url = tweet_image[1]
    data = {'url': image_url}
    response = requests.post(analyze_url, headers=headers,
                             params=params, json=data)
    response.raise_for_status()
    analysis = response.json()
    try:
        image_caption.append([analysis["description"]["captions"][0]["text"].capitalize(), image_url])
    except:
        image_caption.append(["Image could not be captioned", image_url])
# endregion

# region Calculate Similarities
# Similarity calc is limited to the number of generated captions (20)
similarities = []
for i in range(0, len(image_caption)):
    caption = image_caption[i][0]
    alt_text = images_alt_text[i][0]
    image_url = image_caption[i][1]
    similarities.append([alt_text, caption, similar(alt_text, caption), image_url])
# endregion

print("Format: [alt_text, caption, similarity, photo link] \n")
print(*similarities, sep='\n')
