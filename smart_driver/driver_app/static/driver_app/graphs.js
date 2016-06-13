// DRAW WEEKDAY GRAPH USING DATA FROM CALL IN data_table.js FUNCTION
function drawWeekGraph(graphData) {
    nv.addGraph( function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            .showValues(true)
            .duration(250);
        chart.yAxis
            .axisLabel("Avg Hourly Rate in Dollars");
        d3.select('#chart1 svg')
            .datum(graphData)
            .call(chart);

        // LINKS BARS TO REDRAW DATATABLE FUNCTIONS IN data_table.js
        onChart1Created();

        nv.utils.windowResize(chart.update);
        return chart;
    });
}

// FORMAT API RESPONSE FOR DRAWING MONTH GRAPH
// MAX VARIABLE HANDLES Y-SCALE
var monthly_totals = [{key:"Total Earned per Month", values:[]}];
var max = 0
// CALL API
d3.json("/api/month_statements", function(error, data) {
    for(var i in data) {
        monthly_totals[0]["values"].push(
            {"label":data[i]["month_name"], "value":data[i]["total_earned"]}
        );

        if (parseInt(data[i]["total_earned"]) > max) {
            max = parseInt(data[i]["total_earned"])
        }
    };
    // DRAWS MONTLY GRAPH
    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            .showValues(true)
            .duration(250)
            .forceY([0, max + 500 - (max % 500)]);
        chart.yAxis
            .axisLabel("Monthly Income In Dollars");
        d3.select('#chart2 svg')
            .datum(monthly_totals)
            .call(chart);

        // LINK BARS TO FUNCTIONS FILTERING DATATABLE IN data_tables.js
        onChart2Created();

        nv.utils.windowResize(chart.update);
        return chart;
    });
});
