# Amy Finnegan
# database of users and crawls

"""
- Crawls have Users, Users have Followers

Crawls - id = primaryKey, user_id & time began, ForeignKey('users'
Users - id = primaryKey, user_id, following_user, screen_name, followers_count

1 mike_ward time
2 mike's_first_follower time
3 mike's_second_follower time

1 mike_ward follower_count
2 mike_ward_first_follwer follower_count

Put mike ward as first, give him a followers_count and list of followers_ids
Put first follower_id as second, give him a followers_count
Put next follower_id as third, give him a followers_count
"""


# libraries for database

import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, and_, or_, func
from sqlalchemy.orm import relationship, backref, sessionmaker, aliased

from sqlalchemy.types import TypeDecorator, Unicode

# tweepy libraries
import tweepy
from time import sleep
import csv

import time

consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

#First parameter is Consumer Key, second is Consumer Secret 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)      
api = tweepy.API(auth)

#Some info about sqlalchemy
print sqlalchemy.__version__

#Connect to the local database, can use :memory: to just try it out in memory, it doesn't have to exist
engine = sqlalchemy.create_engine('sqlite:///HW7_twitter.db', echo=False)
# echo true is debug information

Base = declarative_base() 

# create the tables

# parent is the users table
class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True)
  user_id = Column(String)
  time_began = Column(String)
  
  crawls = relationship("Crawl", backref="users")
  
  def __init__(self, user_id, time_began):
    self.user_id = user_id
    self.time_began = time_began
    
  def __repr__(self):
    return "User: %s, Start Time: %s" % (self.user_id, self.time_began)
    
# child is the crawls table
class Crawl(Base):
  __tablename__ = "crawls"
  
  id = Column(Integer, primary_key=True)
  screen_name = Column(String)
  follower_count = Column(Integer)
  
  initiating_id = Column(Integer, ForeignKey("users.id"))
  
  def __init__(self, screen_name, follower_count, user=None):
    self.screen_name = screen_name
    self.follower_count = follower_count
    
  def __repr__ (self):
    return "%s has %s followers" % (self.screen_name, self.follower_count)




#First time create tables
Base.metadata.create_all(engine) 

#Create a session to actually store things in the db
Session = sessionmaker(bind=engine)
session = Session()


# initiate a crawl for a user - if I had more than one, I could
# gather them in a list and add to it.
mike_ward = api.get_user('3876')
time = time.clock()
user = User("mike_ward", time)
session.add(user)
session.commit()

# find a user's followers
mikes_followers = api.followers_ids(screen_name='3876')

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

for i in range(len(ids)):
  crawlee = ids[i]
  fc = fc_ct[i]
  crawl = Crawl(crawlee, fc)
  crawl.user = "mike_ward"
  session.add(crawl)


# Persist all of this information
session.commit()
