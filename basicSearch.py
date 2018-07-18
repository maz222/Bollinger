import os
import sqlite3
import requests
import math

def searchSymbol(symbol):
	path = os.path.dirname(os.path.abspath(__file__)) + "/stockDB.db"
	dataBase = sqlite3.connect(path)
	cursor = dataBase.cursor()
	sql = "select * from stocks where symbol like ?"
	cursor.execute(sql,(symbol+"%",))
	results = []
	for row in cursor:
		results.append(row)
	return results

def getData(symbol):
	API_URL = "https://www.alphavantage.co/query"
	key = "YD2JUIE8EPP3MQNB"
	data = {
		"function": "TIME_SERIES_DAILY",
		"symbol": symbol,
		"outputsize": "full",
		"datatype": "json",
		"apikey": key,
		}
	response = requests.get(API_URL, data)
	stockData = response.json()
	if len(stockData) == 1:
		return []
	return(stockData["Time Series (Daily)"])

def getPrices(symbol, periodLength=None):
	data = getData(symbol)
	if len(data) == 1:
		return []
	prices = []
	dates = list(data.keys())
	if periodLength == None:
		periodLength = len(dates)
	for i in range(periodLength):
		prices.append(float(data[dates[i]]["4. close"]))
	return prices

def getSMA(prices,periodLength):
	tempSum = 0
	avgs = []
	for i in range(len(prices)):
		tempSum += prices[i]
		if i == periodLength - 1:
			avgs.append(round(tempSum / periodLength, 2))
		elif i >= periodLength:
			tempSum -= prices[i - periodLength]
			avgs.append(round(tempSum / periodLength, 2))
	return avgs

def getStdDev(prices):
	avg = 0
	for p in prices:
		avg += p
	avg = round(avg / len(prices), 2)
	temp = []
	for p in prices:
		temp.append(round((p - avg) ** 2, 2))
	avg = 0
	for p in temp:
		avg += p
	avg = round(avg / len(temp),2)
	return math.sqrt(avg)

def getBands(prices, periodLength, numStdDev=2):
	middle = getSMA(prices, periodLength)
	stdDev = getStdDev(middle)
	top = []
	bottom = []
	for p in middle:
		top.append(round(p + stdDev * numStdDev, 2))
		bottom.append(round(p - stdDev * numStdDev, 2))
	return {"upper":top, "middle":middle, "lower":bottom}


from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def index():
	prices = getPrices("MS")
	#print(prices)
	bands = getBands(prices,5)
	#print(bands) 
	return str(bands)

@app.route("/<string:symbol>")
def search(symbol):
	prices = getPrices(symbol)
	bands = getBands(prices,5)
	return str(bands)

if __name__ == "__main__":
    app.run()

