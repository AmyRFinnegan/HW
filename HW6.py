# Amy Finnegan
# HW6 twitter

""" So, I need to do these things:

1. Pick a target.  Mike Ward.
2. Look at his followers and find the most followed one.  follwer_count attribute
3. The most followed user two degrees away - follower of followers
4. The most active user two degrees away
5. The user who has the most friends is not passively being followed, they are active.
6. How to store application and restart.
"""

#Register an app: https://dev.twitter.com/

#pip install tweepy
import tweepy
from time import sleep
import csv

consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

#First parameter is Consumer Key, second is Consumer Secret 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)	  
api = tweepy.API(auth)

what info am I storing?
headers = ['follower', 'follower_count']

where should we save info?
filename = "twitter_getter.csv"
readFile = open(filename, "wb")
csvwriter = csv.writer(readFile)
csvwriter.writerow(headers)


find a user's followers
mikes_followers = api.followers_ids(screen_name='3876')
write them to my csv
for f in mikes_followers:
	csvwriter.writerow([f])
	
# divide mikes_followers into easy to manage groups
first = (mikes_followers[0:100])
second = (mikes_followers[101:])

first_report = []
i = 0
while len(first) != i:
	for item in first:
		f = first[i]
		fc = api.get_user(f)
		first_report.append(fc.followers_count)
		#csvwriter.writerow([f, fc])
		i += 1
	print "Sleeping for 15 minutes..."
	sleep(900)  # resting for 15 minutes

print "Started the second set..."	   
second_report = []
i = 0
while len(second) != i:
	for item in second:
		f = second[i]
		fc = api.get_user(f)
		second_report.append(fc.followers_count)
		#csvwriter.writerow([f, fc])
		i += 1
	print "All finished!"
   
ids = first + second
fc_ct = first_report + second_report

# find the most popular follower
store_follower_counts = dict(zip(ids, fc_ct))
print store_follower_counts

for k, v in store_follower_counts.items():
	csvwriter.writerow([k,v])
	
most_popular = max(store_follower_counts, key = store_follower_counts.get)
name = api.get_user(id=most_popular)
print "{0}".format(name.screen_name.encode('ascii', 'ignore')), "is Mike's most popular follower"

readFile.close()

# I'm choosing not to do the part with degrees of seperation because it will take
# too long (longer than a week) to iterate through Mike's most followed-follwer (304,047 followers)
# and determine who is the most followed follwer 2 degrees away.

# Reading tweets and collecting followers is a passive twitter activity, but active users
# seek out/accept friendships.  I look for users with the most "friendships"


##  THIS ONE TIMES OUT REALLY QUICKLY. I THOUGHT I GOT 180 HITS/16 MINS?

# get those who mike follows
mikes_friends = api.friends_ids(screen_name='3876')

# what info am I storing?
headers = ['follower', 'friendships']

# where should we save info?
filename = "outgoing_getter.csv"
readFile = open(filename, "wb")
csvwriter = csv.writer(readFile)
csvwriter.writerow(headers)

# divide mikes_followers into easy to manage groups
first = (mikes_friends[0:100])
second = (mikes_friends[101:])

first_report = []
i = 0
while len(first) != i:
	for item in first:
		f = first[i]
		#fc = api.get_user(f)
		getFriendids = api.friends_ids(user_id=f)
		numFriends = len(getFriendids)
		first_report.append(numFriends)
		#csvwriter.writerow([f, fc])
		i += 1
	print "Sleeping for 15 minutes..."
	sleep(900)	 # resting for 15 minutes

print "Started the second set..."	 
second_report = []
i = 0
while len(second) != i:
	for item in second:
		f = second[i]
		#fc = api.get_user(f)
		getFriendids = api.friends_ids(user_id=f)
		numFriends = len(getFriendids)
		second_report.append(numFriends)
		#csvwriter.writerow([f, fc])
		i += 1
	print "All finished!"
   
ids = first + second
f_ct = first_report + second_report

# find the follower with the most friends
store_friends_counts = dict(zip(ids, f_ct))
print store_friends_counts

for k, v in store_friends_counts.items():
	csvwriter.writerow([k,v])
	
most_active = max(store_friends_counts, key = store_friends_counts.get)
name = api.get_user(id=most_active)
print "{0}".format(name.screen_name.encode('ascii', 'ignore')), "is Mike's most active friend"

readFile.close()




# just some notes of things that worked for referece

# print mike_ward.followers_count
# print mike_ward.friends.followers_count
# print mike_ward.friends_count

# for friend in followers_ids(mike_ward):
	# print followers.screen_name

# How many favorites does he have?
# # mike_ward.favourites_count


# #Who does Mike follow?
# mikes_friends = api.friends(id=mike_ward.screen_name)
# for f in mikes_friends:
  # #Note I am handling UTF encoded strings so I convert them to ASCII-compatible for my mac
  # print "{0}".format(f.screen_name.encode('ascii', 'ignore'))