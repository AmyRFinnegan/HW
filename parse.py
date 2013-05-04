# Amy Finnegan
# Final Project
# May 4, 2013


# libraries for database

import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, and_, or_, func
from sqlalchemy.orm import relationship, backref, sessionmaker, aliased

from sqlalchemy.types import TypeDecorator, Unicode


#Some info about sqlalchemy
print sqlalchemy.__version__

#Connect to the local database, can use :memory: to just try it out in memory, it doesn't have to exist
engine = sqlalchemy.create_engine('sqlite:///mortality.db', echo=False)
# echo true is debug information

Base = declarative_base() 


# Parent -- sources have many datas, a "has many" relationship
class Source(Base):
  __tablename__ = "source"
  
  id = Column(Integer, primary_key=True)
  country = Column(String)
  report_year = Column(Integer)
  
  datas = relationship("Data", backref="source")
  #players = relationship("Player", backref="team") # function in the base , backref: you need to send me info back, rel needs to be two ways for it to work
  
  def __init__(self, country, report_year):
    self.country = country
    self.report_year = report_year
    #self.where_from = where_from
  
  def __repr__(self):
    return "Country: %s, Report year: %s" % (self.country, self.report_year)
    

#Child -- Define some schemas, straight from documentation, inhereit from declarative_base()
class Data(Base):
  __tablename__ = 'datas'
  
  #Have an ID column because player attributes (name, etc) are not unique
  id = Column(Integer, primary_key=True) # this just increments in the order you create them, stays unique
  year = Column(Integer)
  maternal = Column(Integer)
  where_from = Column(String)
  country = Column(String)
  
  source_id = Column(Integer, ForeignKey("source.id")) # source table's id column
  
  def __init__(self, year, maternal, where_from, country, source=None):
    self.year = year
    self.where_from = where_from
    self.maternal = maternal
    self.country = country
    
  def __repr__(self):
    return "For the year %s, MMR: %s, Country: %s" % (self.year, self.maternal, self.country)
    

#First time create tables
Base.metadata.create_all(engine) 

#Create a session to actually store things in the db
Session = sessionmaker(bind=engine)
session = Session()


import re

# make a list of files to open (phylis: tanzania, uganda, mozambique, malawi)

#  MISSINGS
# in uganda SItable was a picture, not table and not parsable
# congo doesn't have the MDG table
# zambia has a 3rd table of data, which is the same as the 2nd.  no text.

to_open = ['malawi2012.txt', 'zambia2013.txt', 'senegal2013.txt', 'tanzania2011.txt', 'uganda2010.txt', 'mozambique2012.txt', 'congo2012.txt']

#to_open = ['malawi.txt', 'zambia.txt', 'senegal.txt','tanzania.txt', 'uganda.txt', 'mozambique.txt', 'congo.txt']

index = 0
for i in to_open:

  opened = to_open[index]  
  file = open(opened, "r")
  text = file.readlines()
  file.close()


  # how to add SOURCE to database
  tmp = to_open[index].rstrip('.txt')
  date = tmp[-4:]
  hold = to_open[index][:-8]
  index += 1

  SItable = Source(hold, date)



  # SOCIAL INDICATORS TABLE (WDI)

  # get the dates from Social Indicators Table
  for n,line in enumerate(text):
      if "POPULATION" in line: 
        num = n-1
      
    
        SocIndDates = text[num]
        SocIndDates = SocIndDates.split()

        date1 = SocIndDates.pop(0) # removing date1 b/c it's typically n/a
        date2 = SocIndDates.pop(0)
        date3 = SocIndDates.pop(0)
        
        # I made new variables because I had to scrape off the last 3 digits
        # It's a five year range, so I add 2 to the base year
        
        # date1 = date1[:-3]
        date2 = date2[:-3]
        date2 = int(date2) + 2
        date3 = date3[:-3]
        date3 = int(date3) + 2
        

  # now find SOCIAL INDICATORS, record line number and range
  for n, line in enumerate(text):
      if "SOCIAL INDICATORS" in line: 
        start = n
    
        end = start + 70

        keyword = re.compile(r"aternal")
        for i,line in enumerate(text):
            if i >= start and i < end :
                if keyword.search(line):
                    tmpM = line
        tmpM = re.sub(r'\.\.', r'00', tmpM, 2)
        tmpM = tmpM.split()

        # ADD TO DATABASE
        
        #entry1 = Data(date1, tmpM[-5], 'SItable', hold) # I no longer use this b/c it's usually n/a
        #entry1.source = SItable

        entry2 = Data(date2, tmpM[-4],'SItable', hold)
        entry2.source = SItable

        entry3 = Data(date3, tmpM[-3], 'SItable', hold)
        entry3.source = SItable

        #session.add(entry1)
        session.add(entry2)
        session.add(entry3)


  ## Find the Millenium Development Goals table (MDG table)
  
  for n, line in enumerate(text):
      if 'With selected targets to achieve' in line:
        mdgStart = n
        mdgEnd = n + 35
        
        
        mdgDates = text[mdgStart + 4]
        mdgDates = mdgDates.split()
        
              
  
  for n, line in enumerate(text):
      if n >= mdgStart and n <= mdgEnd and 'Goal 5' in line:
        num2 = n        
        mdgData = text[num2 + 1]
        mdgData = re.sub(r'\.\.', r'00', mdgData)
        mdgData = re.sub(r'\,', r'', mdgData)
        mdgData = mdgData.split()
        
        
        
        
      
        # add to database
        mdgSource = Source(hold, date)
        mdgE1 = Data(mdgDates[-4], mdgData[-4], 'mdgTable', hold)
        mdgE1.source = mdgSource
        
        mdgE2 = Data(mdgDates[-3], mdgData[-3], 'mdgTable', hold)
        mdgE2.source = mdgSource
        
        mdgE3 = Data(mdgDates[-2], mdgData[-2], 'mdgTable', hold)
        mdgE3.source = mdgSource
        
        mdgE4 = Data(mdgDates[-1], mdgData[-1], 'mdgTable', hold)
        mdgE4.source = mdgSource
        
        session.add(mdgE1)
        session.add(mdgE2)
        session.add(mdgE3)
        session.add(mdgE4)
        
  ## Now parse any mention of maternal mortality in the text

  mStart = []
  for n, line in enumerate(text):
      if 'per 100,000 live births' in line:
        mStart.append(n)
           
        idx = 0
        for i in mStart:
        
          mStartPlus = mStart[idx] + 5
          mStartMinus = mStart[idx] - 5
          idx += 1

          blurb = []
          for i, line in enumerate(text):
              if i >= mStartMinus and i <= mStartPlus:
                  blurb.append(line)

          l = "".join(blurb)
            
          l = l.rstrip()
          # print l
          
        

    
        # try some regular expressions
          mal = re.search(r'\d{3,4} per 100,000 live births in \d{4}\sto\s\d{3,4}\sin\s\d{4}', l)
          
          sen = re.search(r'\d{3,4} for 100,000 births', l)
          
          tan = re.search(r'\d{4} \(\d{3,4} deaths per 100,000 live births\) and \d{4} \(\d{3,4}', l)
          tan2 = re.search(r'\d{3,4} deaths in \d{4}', l)
          
          ug = re.search(r'\d{3,4} deaths per 100,000 live births between \d{4}\sand\s\d{4}', l)
          ug2 = re.search(r'\d{3,4} deaths per 100,000 live births \(\d{4}\)', l)
          
          mo = re.search(r'\d{1}\D\d{3} to \d{3,4} per 100,000', l)
          mo2 = re.search(r'early \d{4}\D and \d{4}', l)
  
          con = re.search(r'\d{3,4} per 100,000 live births', l)
          con2 = re.search(r'according to DHS \d{4}', l)
        
        

          if mal:
             mal = mal.group()
             mal = mal.split()
             textS = Source(hold, date)
           
             tEntry1 = Data(mal[6], mal[0], 'text', hold)
             tEntry1.source = textS
           
             tEntry2 = Data(mal[-1], mal[-3], 'text', hold)
             tEntry2.source = textS
           
             session.add(tEntry1)
             session.add(tEntry2)
       
          elif sen:
             sen = sen.group()
             sen = sen.split()
             textS = Source(hold, date)
           
             tEntry1 = Data(2011, sen[0], 'text', hold)
             tEntry1.source = textS
             session.add(tEntry1)
       
          elif tan and tan2:
             tan = tan.group()
             tan = re.sub(r'\(', r'', tan)
             tan = tan.split()
             textS = Source(hold, date)
           
             tEntry1 = Data(tan[0], tan[1], 'text', hold)
             tEntry1.source = textS
           
             tEntry2 = Data(tan[-2], tan[-1], 'text', hold)
             tEntry2.source = textS
           
             session.add(tEntry1)
             session.add(tEntry2)
          
             tan2 = tan2.group()
             tan2 = tan2.split()
             # textS = Source(hold, date)
             
             tEntry1_2 = Data(tan2[-1], tan2[0], 'text', hold)
             tEntry1_2.source = textS
             
             session.add(tEntry1_2)
             
          elif con and con2:
             con = con.group()
             con = con.split()          
             textS = Source(hold, date)
             
             con2 = con2.group()
             con2 = con2.split()
            
             tEntry1 = Data(con2[-1], con[0], 'text', hold)
             tEntry1.source = textS
            
             session.add(tEntry1)
            
          elif mo and mo2:
              mo = mo.group()
              mo = mo.split()
              textS = Source(hold, date)
            
              tEntry1 = Data(mo2[0], mo[0], 'text', hold)
              tEntry1.source = textS
            
              tEntry2 = Data(mo2[-1], mo[2], 'text', hold)
              tEntry2.source = textS
            
              session.add(tEntry1)
              session.add(tEntry2)
            
          elif ug and ug2:
              ug = ug.group()
              ug = ug.split()
              textS = Source(hold, date)
            
              tEntry1 = Data(ug[-1], ug[0], 'text', hold)
              tEntry1.source = textS
            
              tEntry2 = Data(ug[-3], ug[0], 'text', hold)
              tEntry2.source = textS
            
              session.add(tEntry1)
              session.add(tEntry2)
              
              ug2 = ug2.group()
              ug2 = re.sub(r'\(', r'', ug2)
              ug2 = re.sub(r'\)', r'', ug2)
              ug2 = ug2.split()
              textS = Source(hold, date)
  
              tEntry1_2 = Data(ug2[-1], ug2[0], 'text', hold)
              tEntry1_2.source = textS
            
              session.add(tEntry1_2)
            
          else:
            pass
           




  #Persist all of this information
  session.commit()

