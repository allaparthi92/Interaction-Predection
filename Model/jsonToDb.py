import json
import pprint
#import mysql
import pymysql

def parseFileToDb():

    db = pymysql.connect(host='localhost',user='root', passwd='1234', db='demo')
    cur = db.cursor()
    ## open the twitter data and read each tweet line by line
    with open('interaction.json',encoding='utf8') as data_file:
        i = 0
        # Fetching data from September 09th to October 10th.
        while i < 1700000:
            try:
                first = data_file.readline()
                first = first.replace("\n","")
                data = json.loads(first)
                user = data['screen_name_lower']
                id = data['id']
                keywords = data['keywords']
                location = data['location']
                latitude = location['lat']
                longitude = location['lng']
                text = data['text']
                retweetname = ''
                retweetflag = False
                if text[0:4] == "RT @":
                    text = text[4:len(text)]
                    splitText = text.split(' ')
                    splitText = splitText[0].split(":")
                    if len(splitText[0]) > 30:
                        print("Invalid Retweet Skipping tweet")
                        i=i+1
                        continue
                    retweetname = splitText[0]
                    retweetflag = True
                timestamp = data['timestamp']
                geoflag = data['geoflag']
                if geoflag == False:
                    geoflag = 'FALSE'
                else:
                    geoflag = 'TRUE'
                retweet_count = data['retweet_count']
                if retweetflag == True:
                    cur.execute('INSERT INTO user_tweet (tweetid,username,latitude,longitude,timestamp,geoflag,retweet_count,retweetflag,retweetname) VALUES (' + str(id) + ",\"" + user + "\"," + str(latitude) + "," + str(longitude) + "," + str(timestamp) + "," + geoflag + "," + str(retweet_count) + "," + "TRUE" + ",\"" + retweetname + "\")")
                else:
                    cur.execute('INSERT INTO user_tweet (tweetid,username,latitude,longitude,timestamp,geoflag,retweet_count,retweetflag) VALUES (' + str(id) + ",'" + user + "'," + str(latitude) + "," + str(longitude) + "," + str(timestamp) + "," + geoflag + "," + str(retweet_count) + "," + "FALSE" + ")")
                #print(keywords)
                mentions = []
                hashtags = []
                if retweetflag == True:
                    rt = '@'+retweetname+':'
                    for word in keywords:
                        if word[0] == '@' or word[0] == '#':
                            if word != rt:
                                if word[0] == '@':
                                    mentions.append(word[1:])
                                else:
                                    hashtags.append(word[1:])
                else:
                    for word in keywords:
                        if word[0] == '@':
                            mentions.append(word[1:])
                        elif word[0] == '#':
                            hashtags.append(word[1:])
                #print(mentions)
                #print(hashtags)
                for mention in mentions:
                    cur.execute('INSERT INTO tweet_mentions (tweetid, username, mention) VALUES (' + str(id) + ",'" + user + "','" + mention + "')")

                for hashtag in hashtags:
                    cur.execute('INSERT INTO tweet_hashtag (tweetid, username, hashtag) VALUES (' + str(id) + ",'" + user + "','" + hashtag + "')")
                print(i+1)
                i=i+1
            except UnicodeEncodeError:
                i=i+1
                print("Row No: " + str(i) + " has invalid unicode characters")
            db.commit()
        #db.commit()

parseFileToDb()