# Amy Finnegan
# Final Project
# May 4, 2013

# make the sql db to store scrapes in

# libraries for database

import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, and_, or_, func
from sqlalchemy.orm import relationship, backref, sessionmaker, aliased

from sqlalchemy.types import TypeDecorator, Unicode

from matplotlib import pyplot

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
  #where_from = Column(String)
  
  datas = relationship("Data", backref="source")
  #players = relationship("Player", backref="team") # function in the base , backref: you need to send me info back, rel needs to be two ways for it to work
  
  def __init__(self, country, report_year):
    self.country = country
    self.report_year = report_year
  
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

# add the entries here


#Persist all of this information
session.commit()

Source.__table__
Data.__table__

# Show me all the entries

for data in session.query(Source).order_by(Source.id):
  print data.country, data.report_year
  
for stuff in session.query(Data).order_by(Data.where_from):
  print stuff.year, stuff.maternal, stuff.where_from, stuff.source

# store a query in a list so I can plot it in matplotlib

countries = ['malawi', 'zambia', 'senegal', 'mozambique', 'tanzania', 'uganda', 'congo']
idx = 0
for i in countries:


  # Get the mdgTable data (blue)
  y = []
  i = 0
  for stuff in session.query(Data).filter(and_(Data.where_from == 'mdgTable', Data.country == countries[idx])).order_by(Data.year):
    y.append(stuff.maternal)
    i += 1

  xlab = []
  for stuff in session.query(Data).filter(and_(Data.where_from == 'mdgTable', Data.country == countries[idx])).order_by(Data.year):
    xlab.append(stuff.year)

  # Get the SItable (red)
  y2 = []
  i = 0
  for stuff in session.query(Data).filter(and_(Data.where_from == 'SItable', Data.country == countries[idx])).order_by(Data.year):
     y2.append(stuff.maternal)
     i += 1

  xlab2 = []
  for lab in session.query(Data).filter(and_(Data.where_from == 'SItable', Data.country == countries[idx])).order_by(Data.year):
     xlab2.append(lab.year)
   
  # Get the text (green)
  y3 = []
  i = 0
  for stuff in session.query(Data).filter(and_(Data.where_from == 'text', Data.country == countries[idx])).order_by(Data.year):
     y3.append(stuff.maternal)
   
  xlab3 = []
  for lab in session.query(Data).filter(and_(Data.where_from == 'text', Data.country == countries[idx])).order_by(Data.year):
     xlab3.append(lab.year)

 
  # Plot each country
  pyplot.axis([1985, 2012, 0,1300])
  pyplot.plot( xlab, y, '^-' , label = 'MDG Table')
  pyplot.plot( xlab2, y2, 'r^-', label = 'SI Table')
  pyplot.plot( xlab3, y3, 'g^-', label = 'Text')
  title = countries[idx].upper() + " " + "Maternal Mortality Trend"
  pyplot.title( title )
  pyplot.legend()
  pyplot.xlabel( 'Year' )
  pyplot.ylabel( 'Maternal Deaths per 100,000 live births' )
  plot_name = title + '.png'
  pyplot.savefig( plot_name )
  pyplot.show()
  idx += 1


