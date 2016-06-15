var tableHeader = $('#table_id').find('tr')
var driverID = $('#driver_id').val()
var m = null
var sumTotalEarned = 0;
var avgPerUnit = 0;
var avgPerHour = 0;

// GET AVERAGES FOR COLUMNS IN DATATABLE
function getStats(data) {
    var sumTotal = 0
    var sumRatePerHour = 0;

    for (var i = 0; i < data.length; i++) {
        var row = data[i];
        sumTotal += parseFloat(row.total_earned.substr(1));
        sumRatePerHour += parseFloat(row.rate_per_hour.substr(1));
    };

    sumTotalEarned = "$" + sumTotal.toFixed(2);

    avgPerUnit = sumTotal / (i);
    avgPerUnit =  '$' + avgPerUnit.toFixed(2);

    avgPerHour = sumRatePerHour / (i);
    avgPerHour = "$" + avgPerHour.toFixed(2);
};

// CREATE DATATABLE USING API CALL TO GET DAYSTATEMENTS
function drawDayTable(month = m, weekday) {
    m = month
    // w = weekday
    var url = '/api/day_statements/?driver=' + driverID
    if (month) {
        url += '&month=' + month
    }
    if (weekday) {
        url += '&weekday=' + weekday
    }
    tableHeader.append(
        $('<th>').text('Date'),
        $('<th>').text('Weekday'),
        $('<th>').text('Total Earned'),
        $('<th id="time_worked" title="Time elapsed from first ride request to last dropoff">').text('Time Worked'),
        $('<th>').text('Rate/Hr'),
        $('<th>').text('Total Rides'),
        $('<th>').text('Rate/Ride')
    );
    $.get(url, function(data) {
        window.dataTable = $('#table_id').DataTable({
            "pageLength": 30,
            "bLengthChange": false,
            "bFilter": false,
            data: data,
            columns: [
                {data: 'date'},
                {data: 'weekday'},
                {data: 'total_earned'},
                {data: 'time_worked'},
                {data: 'rate_per_hour'},
                {data: 'total_rides'},
                {data: 'rate_per_ride'}
            ],
            aaSorting: [[0, 'desc']]
        });
        console.log(data)
        getStats(dataTable.data());
        $('#avg_per_hour p').html(avgPerHour);
        $('#avg_per_unit h3').html('Avg Daily Rate');
        $('#avg_per_unit p').html(avgPerUnit);
        $('#total_earned p').html(sumTotalEarned);

        if (weekday == null) {
            drawWeekGraph(formatGraphData(data));
        };
    });
    $("#time_worked").qtip({
        position: {
            at: 'bottom center',
        }
    });
};

function destroyTable() {
    $('#table_id').DataTable().destroy();
    tableHeader.find('th').remove();
}

// CREATE DATATABLE USING API CALL TO GET WEEKSTATEMENTS
function drawWeekTable(month = m) {
    m = month
    var week_url = '/api/week_statements/?driver=' + driverID
    var day_url = '/api/day_statements/?driver=' + driverID
    var query = ''
    if (month) {
        query += '&month=' + month
    }
    tableHeader.append(
        $('<th>').text('Starting'),
        $('<th>').text('Ending'),
        $('<th>').text('Total Earned'),
        $('<th>').text('Rate/Day'),
        $('<th>').text('Rate/Hr'),
        $('<th>').text('Total Rides'),
        $('<th>').text('Rate/Ride')
    );
    $.get(week_url + query, function(data) {
        window.dataTable = $('#table_id').DataTable({
            "pageLength": 30,
            "bLengthChange": false,
            "bFilter": false,
            data: data,
            columns: [
                {data: 'starting_at'},
                {data: 'ending_at'},
                {data: 'total_earned'},
                {data: 'rate_per_day'},
                {data: 'rate_per_hour'},
                {data: 'total_rides'},
                {data: 'rate_per_ride'}
            ],
            aaSorting: [[0, 'desc']]
        });
        getStats(dataTable.data());
        $('#avg_per_hour p').html(avgPerHour);
        $('#avg_per_unit h3').html('Avg Weekly Rate');
        $('#avg_per_unit p').html(avgPerUnit);
        $('#total_earned p').html(sumTotalEarned);
    });
    $.get(day_url + query, function(data) {
        drawWeekGraph(formatGraphData(data));
    })
};

// FIND DAILY/WEEKLY OPTION SELECTED IN DROPDOWN (0=DAILY, 1=WEEKLY)
var filterSelection = $('#data-type option:selected').val();

// DETERMINE DAILY/WEEKLY OPTION SELECTED AND REDRAW FILTERED TABLE
function filterTable(m, w) {
    destroyTable();
    if (filterSelection == 'daily') {
        drawDayTable(m, w);
    }
    else {
        drawWeekTable(m);
    }
};

// CREATE INITIAL TABLE OF ALL DAYSTATEMENT, HOOK-UP DAILY/WEEKLY DROPDOWN
$(document).ready(function() {
    drawDayTable();

    $('#data-type').change(function() {
        filterSelection = $('#data-type option:selected').val();
        filterTable(m);
    });

});

// LINK WEEKDAY CHART (ONCE IT'S LOADED) TO REDRAWING FILTERED TABLE
function onChart1Created() {
    d3.select('#chart1 svg')
        .selectAll('.discreteBar')
        .on('click', function (d) {
            document.getElementById('data-type').selectedIndex = 'daily'
            filterSelection = 'daily'
            filterTable(m, d['label'])
        });
};

// LINK MONTH CHART (ONCE IT'S LOADED) TO REDRAWING FILTERED TABLE
function onChart2Created() {
    d3.select('#chart2 svg')
        .selectAll('.discreteBar')
        .on('click', function (d) {
            filterTable(d['label'])
        });
};

// FORMAT API RESPONSE DATA FOR REDRAWING WEEKDAY GRAPH PER MONTH
function formatGraphData(data) {
    graphData = [{key:"Avg Hourly Rate By Weekday", values:[]}];

    countList = {
        "Monday": {sum: 0, count: 0},
        "Tuesday": {sum: 0, count: 0},
        "Wednesday": {sum: 0, count: 0},
        "Thursday": {sum: 0, count: 0},
        "Friday": {sum: 0, count: 0},
        "Saturday": {sum: 0, count: 0},
        "Sunday": {sum: 0, count: 0}
    }

    for (var i = 0; i < data.length; i++) {
            countList[data[i].weekday].sum += Number(data[i].rate_per_hour.replace("$", ""))
            ++countList[data[i].weekday].count
    };

    for (i in countList) {
        if (countList[i].count == 0) {
            countList[i].count = 1
        };
        graphData[0]["values"].push(
            {"label": i, "value": countList[i].sum / countList[i].count}
        );
    };

    return graphData
};

// SHOW ALL BUTTON RESETS FILTERS, REDRAWS TABLE OF ALL DAY DATA
$("#reset").click(function() {
    console.log('clickedit')
    m = null
    filterTable(m);
})
