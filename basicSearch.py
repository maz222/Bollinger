import os
import sqlite3
import requests
import math
import json

def searchSymbol(symbol):
	path = os.path.dirname(os.path.abspath(__file__)) + "/stockDB.db"
	path = "stockDB.db"
	dataBase = sqlite3.connect(path)
	cursor = dataBase.cursor()
	sql = "select * from stocks where symbol like ?"
	cursor.execute(sql,(symbol+"%",))
	results = []
	for row in cursor:
		results.append(row)
	return results

def getDailyPrices(symbol):
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

def getDailyBands(symbol, timePeriod):
	API_URL = "https://www.alphavantage.co/query"
	key = "YD2JUIE8EPP3MQNB"
	data = {
		"function": "BBANDS",
		"interval": "daily",
		"symbol": symbol,
		"time_period": timePeriod,
		"series_type": "close",
		"datatype": "json",
		"apikey": key,
	}
	response = requests.get(API_URL, data)
	stockData = response.json()
	if len(stockData) == 1:
		return []
	return(stockData["Technical Analysis: BBANDS"])

def getBandPointsOfInterest(prices, bands, totalLength):
	POI = []
	for i in range(totalLength):
		d = list(prices.keys())[i]
		close = round(float(prices[d]["4. close"]),2)
		high = round(float(bands[d]["Real Upper Band"]),2)
		low = round(float(bands[d]["Real Lower Band"]),2)
		#print([close, high, low])
		if close > high:
			POI.append([d, close, high, close - high, (close / high - 1) * 100])
		elif close < low:
			POI.append([d, close, low, close - low, (close / low - 1) * 100])
	return POI

from flask import Flask, render_template
app = Flask(__name__)
 
@app.route("/")
def index():
	#prices = getPrices("MS")
	#bands = getBands(prices,5)
	#return str(bands)
	return render_template("/index.html")

@app.route("/symbol/<string:symbol>", methods=['GET', 'POST'])
def search(symbol):
	prices = getDailyPrices(symbol)
	bands = getDailyBands(symbol,2)
	numBands = 100
	POI = getBandPointsOfInterest(prices, bands, numBands)
	temp = {"prices":prices,"bands":bands,"pointsOfInterest":POI}
	return json.dumps(temp)


@app.route("/search/<string:symbol>", methods=['GET', 'POST'])
def searchSymbols(symbol):
	results = searchSymbol(symbol)
	if len(results) == 0:
		return json.dumps({"results":[]})
	else:
		temp = {"symbolResults":[]}
		for r in results:
			temp["symbolResults"].append((r[0],r[1]))
		return json.dumps(temp)

if __name__ == "__main__":
    app.run(debug=True)