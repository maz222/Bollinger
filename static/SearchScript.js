function setStock(stockData, symbol, name) {
	$(".stockContainer").css("display","block");
	$(".searchContainer").css("display","none");
	$(".header").css("height","calc(10% - 20px)");
	$(".header").find("h1").css("display","none");
	stockData = JSON.parse(stockData);
	//console.log(stockData["pointsOfInterest"]);
	console.log(stockData["bands"]);
	var currPrices = stockData["prices"][Object.keys(stockData["prices"])[0]];
	$(".stockContainer").find(".stockOpen").text(parseFloat(currPrices["1. open"]).toFixed(2));
	$(".stockContainer").find(".stockHigh").text(parseFloat(currPrices["2. high"]).toFixed(2));
	$(".stockContainer").find(".stockLow").text(parseFloat(currPrices["3. low"]).toFixed(2));
	$(".stockContainer").find(".stockClose").text(parseFloat(currPrices["4. close"]).toFixed(2));
	$(".stockContainer").find(".stockDate").text(Object.keys(stockData["prices"])[0]);
	$(".stockContainer").find(".stockSymbol").text(symbol);
	$(".stockContainer").find(".stockName").text(name);
	setBands(stockData["bands"],stockData["pointsOfInterest"],stockData["prices"]);
}

function setResults(results) {
	$(".stockContainer").css("display","none");
	$(".searchContainer").css("display","block");
	results = JSON.parse(results);
	var $resultsContainer = $(".results");
	$resultsContainer.empty();
	//console.log(results);
	//console.log(results.symbolResults);
	for(var i in results.symbolResults) {
		var symbolText = "<h1>" + results.symbolResults[i][0] + "</h1>";
		var nameText = "<h2>" + results.symbolResults[i][1] + "</h2>";
		var tempDiv = "<div class='listing'>" + symbolText + nameText + "</div>";
		//console.log(tempDiv);
		$resultsContainer.append(tempDiv);
	}
	if(results.symbolResults == undefined) {
		$resultsContainer.append("<div id='emptyListing'>No results found :(</div>");
	}
	$(".listing").click(function(event) {
		console.log("clicked!");
		var symbol = $(this).find("h1").text();
		var name = $(this).find("h2").text();
		$.ajax({
			type: 'POST',
			url: "symbol/" + symbol,
			success: function(response) {
				//console.log(response);
				setStock(response, symbol, name);
			}
		});
	});
}

function formatBands(bands, prices) {
	console.log("formatting...");
	//console.log(prices);
	var formattedData = [["Day","Upper Band","Lower Band","Price"]];
	for(var i in Object.keys(bands)) {
		date = Object.keys(bands)[i]
		bandData = bands[date];
		priceData = prices[date];
		highBand = parseFloat(bandData["Real Upper Band"]);
		lowerBand = parseFloat(bandData["Real Lower Band"]);
		price = parseFloat(priceData["4. close"]);
		formattedData.push([date, highBand, lowerBand, price]);
		//formattedData.push([date, 24, 12, 8]);
	}
	return formattedData;
}

function setGraph(graphData) {

	function drawLineColors() {
		var data = google.visualization.arrayToDataTable(graphData);
  		var options = {
	    	height: "100%",
	    	legend: {
	      		position: 'top'
	    	},
	    	series: {
	      		0: {color: "green"},
	      		1: {color: "grey"},
	      		2: {color: "red"},
	      		3: {color: "black"},
	    	},
	    	hAxis: {
	      		title: "Date"
	    	},
	    	vAxis: {
	      		title: "Price"
	    	}
  		};
		var chart = new google.visualization.LineChart(document.getElementById('graph1'));
  		chart.draw(data, options);
  	}

	google.charts.load('current', {
  		callback: drawLineColors,
  		packages: ['corechart']
	});

}

//POI = [date, price, bandPrice, diff, % diff]
function setBands(bands, pointsOfInterest, prices) {
	console.log("setting bands");
	f = formatBands(bands, prices);
	console.log(f);
	setGraph(f);
	//setGraph(formarBands(bands))
	var POI = pointsOfInterest;
	if(POI.length == 0){
		$(".graphDetails").css("display","none");
		return;
	}
	var $graphTable = $(".events");
	for(var i in POI) {
		var $entry = $("<div class='bandPOI'></div>");
		for(var c in POI[i]) {
			var $cell = $("<div class='cell'></div>");
			var $cellContent = $("<h3></h3>");
			$cellContent.text(POI[i][c]);
			$cell.append($cellContent);
			$entry.append($cell);
		}
		$graphTable.append($entry);
	}
}

$(document).ready(function() {
	$("form").submit(function(event) {
		event.preventDefault();
		console.log($("#symbolSearch").val());
		$.ajax({
			type: 'POST',
			url: "search/" + $("#symbolSearch").val(),
			success: function(response) {
				//console.log(response);
				setResults(response);
			}
		});
	});
})