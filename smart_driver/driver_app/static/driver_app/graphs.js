nv.addGraph(function() {
    var chart = nv.models.discreteBarChart()
        .x(function(d) { return d.label })
        .y(function(d) { return d.value })
        .staggerLabels(true)
        //.staggerLabels(historicalBarChart[0].values.length > 8)
        .showValues(true)
        .duration(250)
        .forceY([0, hourly_max + 5 - (hourly_max % 5)])
        chart.yAxis
          .axisLabel("Avg Hourly Rate in Dollars")
        ;
    d3.select('#chart1 svg')
        .datum(weekday_graph_data)
        .call(chart);

    onChart1Created();

    nv.utils.windowResize(chart.update);
    return chart;
});


var monthly_totals = [{key:"Total Earned per Month", values:[]}];
var max = 0
d3.json("/api/month_statements",
  function(error, data) {
      for(var i in data) {
          monthly_totals[0]["values"].push({"label":data[i]["month_name"],"value":data[i]["total_earned"]});
          if (parseInt(data[i]["total_earned"]) > max) {
              max = parseInt(data[i]["total_earned"])
          }
      }
      nv.addGraph(function() {
          var chart = nv.models.discreteBarChart()
              .x(function(d) { return d.label })
              .y(function(d) { return d.value })
              .staggerLabels(true)
              //.staggerLabels(historicalBarChart[0].values.length > 8)
              .showValues(true)
              .duration(250)
              .forceY([0, max + 500 - (max % 500)])
              chart.yAxis
                .axisLabel("Monthly Income In Dollars")
          d3.select('#chart2 svg')
              .datum(monthly_totals)
              .call(chart);

          onChart2Created();

          nv.utils.windowResize(chart.update);
          return chart;
      });
  }
);
