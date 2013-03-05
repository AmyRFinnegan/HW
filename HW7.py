# Amy Finnegan
# HW7

# libraries for database

import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, and_, or_, func
from sqlalchemy.orm import relationship, backref, sessionmaker, aliased

from sqlalchemy.types import TypeDecorator, Unicode

# libraries for web crawler

from nltk.util import clean_html
import urllib2 
import time
from bs4 import BeautifulSoup

#Some info about sqlalchemy
print sqlalchemy.__version__

#Connect to the local database, can use :memory: to just try it out in memory, it doesn't have to exist
engine = sqlalchemy.create_engine('sqlite:///HW7.db', echo=False)
# echo true is debug information

Base = declarative_base() 


# Parent -- sources have many posts, a "has many" relationship
class Source(Base):
  __tablename__ = "source"
  
  id = Column(Integer, primary_key=True)
  name = Column(String)
  site_url = Column(String)
  
  posts = relationship("Post", backref="source")
  #players = relationship("Player", backref="team") # function in the base , backref: you need to send me info back, rel needs to be two ways for it to work
  
  def __init__(self, name, site_url):
    self.name = name
    self.site_url = site_url
  
  def __repr__(self):
    return "Site crawled: %s, <%s>" % (self.name, self.site_url)
    

#Child -- Define some schemas, straight from documentation, inhereit from declarative_base()
class Post(Base):
  __tablename__ = 'scrapes'
  
  #Have an ID column because player attributes (name, etc) are not unique
  id = Column(Integer, primary_key=True) # this just increments in the order you create them, stays unique
  publish_date = Column(String)
  url = Column(String)
  post_title = Column(String)
  comment_count = Column(Integer)
  
  source_id = Column(Integer, ForeignKey("source.id")) # source table's id column
  
  def __init__(self, publish_date, url, post_title, comment_count, source=None):
    self.publish_date = publish_date
    self.url = url
    self.post_title = post_title
    self.comment_count = comment_count
    
  def __repr__(self):
    return "%s, posted on %s" % (self.post_title, self.publish_date)
    


#First time create tables
Base.metadata.create_all(engine) 

#Create a session to actually store things in the db
Session = sessionmaker(bind=engine)
session = Session()

## Crawling ##

# What page?
# Get a list of pages
pages_to_scrape = []
first = 'http://onlinecrackerbarrel.wordpress.com'
pages_to_scrape.append(first)

for i in range(2, 6):
  next = first + "/page/" + str(i)
  pages_to_scrape.append(next)


#j = 1

for i in range(len(pages_to_scrape)):

  
  time.sleep(2)
  
  # Open webpage
  # for j in range(len(pages_to_scrape)): 
  page_to_scrape = pages_to_scrape[i]
  
  s = Source("onlinecrackerbarrel", page_to_scrape)
  session.add(s)
  session.commit()
  
  webpage = urllib2.urlopen(page_to_scrape)
      #j += 1

  # Parse it
  soup = BeautifulSoup(webpage.read())
  soup.prettify()

  # extract all post_titles, publish_dates, comment_counts, urls
  post_title = soup.findAll("h2", attrs={'class':'entry-title'})
  publish_date = soup.findAll("div", attrs={'class':'postMeta'})
  comment_count = soup.findAll("p", attrs={'class':'container'})
  urls = soup.findAll("h2", class_="entry-title")



  for i in range(10):
    date = publish_date[i]
    d = clean_html(str(date.find("span", attrs={'class':'date'})))
    # d_clean = d.encode('ascii', 'ignore')
    d_clean = d.decode('utf-8')
        
    url = urls[i]
    u = url('a')[0]['href']
    # u_clean = u.encode('ascii', 'ignore')
    u_clean = u.decode('utf-8')

    post = post_title[i]
    p = clean_html(str(post.find("a")))
    # p_clean = p.encode('ascii', 'ignore')
    p_clean = p.decode('utf-8')

    comment = comment_count[i]
    c = clean_html(str(comment.find("span", attrs={'class':'comments'})))
    # c_clean = c.encode('ascii', 'ignore')
    c_clean = c.decode('utf-8')

    entry = Post(d_clean, u_clean, p_clean, c_clean)
    entry.source = s
    session.add(entry)
    #session.commit()
    

#Persist all of this information
session.commit()

Source.__table__
Post.__table__

# show me all the post titles with id and source info
for post in session.query(Post).order_by(Post.id):
  print post.id, post.source, "{0}".format(post.post_title.encode('ascii', 'ignore'))

# Order by post publish date
for post in session.query(Post).order_by(Post.publish_date):
  print "{0}: {1}".format(post.publish_date.encode('ascii', 'ignore'), post.post_title.encode('ascii', 'ignore'))

# # show me the sources
for source in session.query(Source):
  print "{0}: {1}".format(source.name.encode('ascii', 'ignore'), source.site_url.encode('ascii', 'ignore'))
  
# query all from one source (This isn't working, it just shows me all of them.)
for post, source in session.query(Post, Source).filter(Source.site_url.like("%page/5%")):
  print "{0}: {1}".format(post.post_title.encode('ascii', 'ignore'), post.source.site_url)