"""
Amy Finnegan
HW 2: portfolio
I worked with Lucy Sorenson
"""

import random
from datetime import datetime

stock_market = {}

class Portfolio(object):
    def __init__(self):
	    self.cash = 0
	    self.stock_list = {}
	    self.fund_list = {}
	    self.history_list = [str(datetime.now()) + " " + 'Open Portfolio']

    def addCash(self, amount):
		self.amount = amount
		self.cash = self.cash + amount
		self.history_list.append(str(datetime.now()) + " " + "$" + str(amount) + " cash added")
	
    def withdrawCash(self, amount):
		self.amount = amount
		self.cash = self.cash - amount
		self.history_list.append(str(datetime.now()) + " " + "$" + str(amount) + " cash withdrawn")

    def buyMutualFund(self, shares, symbol):
	  self.shares = shares
	  self.symbol = symbol
	  price = 1
	  self.withdrawCash(shares*price)
	  if self.symbol in self.fund_list:
	     self.fund_list[self.symbol] = self.fund_list[self.symbol] + shares
	  else: 
	     self.fund_list[self.symbol.symbol] = shares
	  self.history_list.append(str(datetime.now()) + " " + str(shares) + " MutualFund purhcased at $%d per share" % price)

    def sellMutualFund(self, symbol, shares):
	  self.shares = shares
	  self.symbol = symbol
	  tmp = random.uniform(0.9, 1.2)
	  price = round(tmp,2)
	  self.addCash(shares*price)
	  self.fund_list[symbol] = self.fund_list[symbol] - shares
	  self.history_list.append(str(datetime.now()) + " " + str(shares) + " MutualFund sold at $%d per share" % price)

    
    def buyStock(self, shares, symbol):
	  self.shares = shares
	  self.symbol = symbol
	  price = stock_market[symbol.symbol]
	  self.withdrawCash(shares*price)
	  if self.symbol.symbol in self.stock_list:
	     self.stock_list[self.symbol.symbol] = self.symbol.symbol[self.symbol.symbol] + shares
	  else: 
	     self.stock_list[self.symbol.symbol] = shares
	  self.history_list.append(str(datetime.now()) + " " + str(shares) + " stock purchased at $%d per share" % price)
	
    def sellStock(self, symbol, shares):
	  self.shares = shares
	  self.symbol = symbol
	  tmp = random.uniform(0.5, 1.5)
	  price = round(tmp, 2)
	  self.addCash(shares*price)
	  self.stock_list[self.symbol] = self.stock_list[self.symbol] - shares
	  self.history_list.append(str(datetime.now()) + " " + str(shares) + " stock sold at $%d per share" % price)
	
    def history(self):
        print " " + "\n ".join(self.history_list)
	
	def __str__(self):
	      return str(self.print_portfolio())

    def print_assets(self):
	  title = "\nPortfolio Assets"
	  coh = "\nCash: $" + str(round(self.cash, 2))
	  stocks = "\nStocks: " + str(self.stock_list)
	  mf = "\nMutual Funds: " + str(self.fund_list)
	  print str(title) + str(coh) + str(stocks) + str(mf)

 
class MutualFund(object):
  def __init__(self, symbol):
	  self.symbol = symbol

	
class Stock(object):
  def __init__(self, price, symbol):
	  self.symbol = symbol
	  stock_market[symbol] = price





	

# create a new portfolio
portfolio = Portfolio()

# add cash to the portfolio
portfolio.addCash(300.50)

# create a stock to buy
s = Stock(price=20, symbol="HFH")

# buy 5 shares of stock s
portfolio.buyStock(5, s)

# create two mutual funds
mf1 = MutualFund("BRT")
mf2 = MutualFund("GHT")

# Buy 10.3 shares of mf1
portfolio.buyMutualFund(10.3, mf1)

# Buy 2 shares of mf2
portfolio.buyMutualFund(2, mf2)

# Sell 3 shares of BRT
portfolio.sellMutualFund("BRT", 3)

# Sell 1 share of HFH
portfolio.sellStock("HFH", 1)

# WIthdraw $50
portfolio.withdrawCash(50)

# Show a transaction history ordered by time
portfolio.history()

# Final assets
portfolio.print_assets()



