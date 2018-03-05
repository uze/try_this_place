import tweepy, os, requests, shutil, random, time, json
from credentials import *

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Base Url for unsplashed API
baseUrl = 'https://source.unsplash.com/1024x512/?'

# Retweets, Favorites, and follows users with a specific hashtag
def reply():
    for tweet in tweepy.Cursor(api.search, q='#foodie').items(10):
        try:
            # Add \n escape character to print() to organize tweets
            print('\nTweet by: @' + tweet.user.screen_name)

            # Retweet tweets as they are found
            #tweet.retweet()
            #print('Retweeted the tweet')

            # Favorite the tweet
            tweet.favorite()
            print('Favorited the tweet')

            # Follow the user who tweeted
            tweet.user.follow()
            print('Followed the user')

            if not tweet.user.following:
                tweet.user.follow()
                print('Followed the user')

            print(tweet.text)
            print(tweet.user.screen_name)

            filename = 'temp.jpg'
            request = requests.get(baseUrl + 'food', stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)

                api.update_with_media(filename, status=message(tweet.user.screen_name), in_reply_to_status_id=tweet.id)
                os.remove(filename)

            else:
                print("Error")

            print (message(tweet.user.screen_name))

        except tweepy.TweepError as e:
            time.sleep(60)
            print(e.reason)

        except StopIteration:
            break

def recommendation():
    key = ["burgers", "salad"]
    word = random.choice(key)
    return " Next time you're hungry go for some " + word + " at a restaurant near you."

def message(user):
    return "@" + user + recommendation()

def mainTweet(url, message):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)

    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status = message)
        os.remove(filename)
        time.sleep(3 * 60)
    else:
        print("Error")

def twitterCaption(word):
    return "Were in the mood for a " + word + "!"

def post():
    key = ["Burger", "Salad", "Breakfast", "Dessert", "Pasta", "Ice Cream"]
    word = random.choice(key)
    mainTweet(baseUrl + word, twitterCaption(word))

while True:
    reply()
    post()
