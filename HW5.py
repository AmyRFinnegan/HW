# Amy Finnegan
# Scraper to collect information for HW5

import csv 
from nltk.util import clean_html
import urllib2 
import time
from bs4 import BeautifulSoup

# What page?
# Get a list of pages
pages_to_scrape = []
first = 'http://onlinecrackerbarrel.wordpress.com'
pages_to_scrape.append(first)

for i in range(1, 6):
  next = first + "/page/" + str(i)
  pages_to_scrape.append(next)


# What info do we want? 
headers = ["publish_date", "url", "post_title", "comment_count", "is_post"]

# Where do we save info?
filename = "myblog_info.csv"
readFile = open(filename, "wb")
csvwriter = csv.writer(readFile)
csvwriter.writerow(headers)

j = 1

for i in pages_to_scrape:

  time.sleep(2)
  
  # Open webpage
  page_to_scrape = pages_to_scrape[j]
  webpage = urllib2.urlopen(page_to_scrape)
  j += 1

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
    url = urls[i]
    u = url('a')[0]['href']
    post = post_title[i]
    p = clean_html(str(post.find("a")))
    comment = comment_count[i]
    c = clean_html(str(comment.find("span", attrs={'class':'comments'})))
    is_post = 1
    csvwriter.writerow([d, u, p, c, is_post])
    

# for date in publish_date:
  # d = clean_html(str(date.find("span", attrs={'class':'date'})))
  # print d

# for url in urls:
  # u = url('a')[0]['href']
  # print u
 
 # for post in post_title:
  # p = clean_html(str(post.find("a")))
  # print p
  
# for comment in comment_count:
  # c = clean_html(str(comment.find("span", attrs={'class':'comments'})))
  # print c
  

  
# csvwriter.writerow([p, d, c])

readFile.close()