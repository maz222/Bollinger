import math
import requests

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
	print(stockData)
	return(stockData["Time Series (Daily)"])
	#print(response.json())

def getPrices(symbol, periodLength):
	data = getData(symbol)
	prices = []
	dates = list(data.keys())
	for i in range(periodLength):
		prices.append(float(data[dates[i]]["4. close"]))
	return prices

testP = getPrices("asdghasgd",100)
data = getBands(testP, 2)
print(data["upper"])
print("---")
print(data["lower"])
print("---")
print(data["middle"])
