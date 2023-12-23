from tkinter import *
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import matplotlib.pyplot as plt


class TwitterClient(object): 
    def __init__(self):  
        consumer_key = 'xxxx'
        consumer_secret = 'xxxx'
        access_token = 'xxxx'
        access_token_secret = 'xxxx'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
            print("Connected")
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self, tweet):  
        analysis = TextBlob(self.clean_tweet(tweet)) 
 
        return(analysis.sentiment.polarity)

    def get_tweets(self, query, count = 10): 
 
        tweets = [] 
        try: 
 
            fetched_tweets = self.api.search(q = query, count = count, language='en') 

 
            for tweet in fetched_tweets: 

                parsed_tweet = {} 


                parsed_tweet['text'] = tweet.text

                parsed_tweet['polarity'] = self.get_tweet_sentiment(tweet.text)

                if parsed_tweet['polarity'] > 0:
                    parsed_tweet['sentiment'] =  'positive'
                elif parsed_tweet['polarity'] == 0:
                    parsed_tweet['sentiment'] = 'neutral'
                else:
                    parsed_tweet['sentiment'] = 'negative'


                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

            return tweets 

        except tweepy.TweepError as e:  
            print("Error : " + str(e))

def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    global e1
    query = e1.get()
    global e2
    count = e2.get()
    tweets = api.get_tweets(query = query, count = count)
    
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    p_polarity = [tweet['polarity'] for tweet in ptweets]
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    n_polarity = [tweet['polarity'] for tweet in ntweets]
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # picking neutral tweets from set of tweets
    netweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100*len(netweets)/len(tweets)))
    
    print("---------------------------------------------------------------------------")
    
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    
    print("\n\nPositive tweets:")
    c=0
    for tweet in ptweets: 
        c=c+1
        print("{}. {}".format(c,tweet['text'].translate(non_bmp_map)))
    print("---------------------------------------------------------------------------")
 
    print("\n\nNegative tweets:")
    c=0
    for tweet in ntweets: 
        c=c+1
        print("{}. {}".format(c,tweet['text'].translate(non_bmp_map)))
    print("----------------------------------------------------------------------------")
    
    print("\n\nNeutral tweets:")
    c=0
    for tweet in netweets: 
        c=c+1
        print("{}. {}".format(c,tweet['text'].translate(non_bmp_map))) 
    print("----------------------------------------------------------------------------")


    labels1 = 'Positive Tweets', 'Negative Tweets', 'Neutral Tweets'
    sizes = [100*len(ptweets)/len(tweets), 100*len(ntweets)/len(tweets), 100*len(netweets)/len(tweets)]
    explode = (0.1, 0, 0)
    fig1, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.pie(sizes, explode=explode, labels=labels1, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')
    ax1.set_title('Pie Chart of Tweet Sentiment Analysis')


    polarity_values=[p_polarity, n_polarity]
    labels2 = 'Positive Polarities', 'Negative Polarities'
    fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(6,6))
    ax2.boxplot(polarity_values,vert=True, patch_artist=True, labels=labels2)
    ax2.set_title('Rectangular Box Plot for Polarity Distribution')

    plt.show()

if __name__ == "__main__":
    root = Tk()
    root.config(background='black')
    root.geometry("500x350")
    root.resizable(0, 0)
    root.title('SENTIMENT ANALYSER Using NLP')

    l1= Label(root, text="SENTIMENT ANALYSER", bg="Black", fg="Green",
             height=3, width=500, font=("Courier", 30))
    l1.pack()

    l2 = Label(root, text="Enter the Keyword", bg="Black", fg="Green",
               font="Courier")
    l2.pack()

    e1 = Entry(root)
    e1.pack()

    l3 = Label(root, text="", bg="Black", fg="Green",font="Courier")
    l3.pack()

    l4 = Label(root, text="Enter the Count of Tweets", bg="Black", fg="Green",
               font="Courier")
    l4.pack()

    e2 = Entry(root)
    e2.pack()

    l5 = Label(root, text="", bg="Black", fg="Green",font="Courier")
    l5.pack()
    

    b = Button(root, text='GO', command=main, bg="Green",
               font="Courier", bd=0, width=5)
    b.pack()
    root.mainloop()

    # calling main function  
