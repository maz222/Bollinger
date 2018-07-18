$(document).ready(function () {
    $("#rightStock").css("display","none");
    //drawLineColors(bandData);

    $(".searchInput").on("input", function() {
        if($(this).val().length == 0) {
            $stock = $(this).closest(".stock");
            $stock.find(".searchResults").css("display","none");
            $stock.find(".stockPane").css("display","block");
        }
        else {
            $stock = $(this).closest(".stock");
            $stock.find(".searchResults").css("display","block");
            $stock.find(".stockPane").css("display","none");
        }
    });

    $(".searchResult").on("click", function() {
        $stock = $(this).closest(".stock");
        $stock.find(".searchResults").css("display","none");
        $stock.find(".stockPane").css("display","block");
    });

    $("#compareButton").on("click", function() {
        $("#leftStock").css("width","calc(50% - 30px)");
        $("#rightStock").css("display","block");
        $(this).closest(".searchButton").css("display","none")
        $(this).closest(".searchPane").find(".searchInput").css("width","100%");
        drawLineColors(bandData);
    })

    $("#closeButton").on("click", function() {
        $("#leftStock").css("width","calc(100% - 30px)");
        $("#rightStock").css("display","none");
        $("#leftStock").find(".searchButton").css("display","block");
        $("#leftStock").find(".searchInput").css("width","90%");
        drawLineColors(bandData);
    })
})

//stockInfo - {"name","symbol","prices","bands"}
//prices - {"open","close","high","low"}
//bands - {"upper","middle","lower"}
function updateStock(panelName, stockInfo) {
    var $pane = $(panelName).find(".stockPane");
    $pane.find(".stockHeader").find("h2").text(stockInfo["name"]);
    $pane.find(".openCell").text(stockInfo["prices"]["open"]);
    $pane.find(".closeCell").text(stockInfo["prices"]["close"]);
    $pane.find(".highCell").text(stockInfo["prices"]["high"]);
    $pane.find(".lowCell").text(stockInfo["prices"]["low"]);
}