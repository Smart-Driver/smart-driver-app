var table_header = $('#table_id').find('tr')
var driverID = $('#driver_id').val()
var m = null
var sum_total_earned = 0;
var avg_per_unit = 0;
var avg_per_hour = 0;


// GET AVERAGES FOR COLUMNS IN DATATABLE
function getStats(data) {
    var sum_total = 0
    var sum_rate_per_hour = 0;

    for (var i = 0; i < data.length; i++) {
        var row = data[i];
        sum_total += parseFloat(row.total_earned.substr(1));
        sum_rate_per_hour += parseFloat(row.rate_per_hour.substr(1));
    };

    sum_total_earned = "$" + sum_total.toFixed(2);

    avg_per_unit = sum_total / (i);
    avg_per_unit =  '$' + avg_per_unit.toFixed(2);

    avg_per_hour = sum_rate_per_hour / (i);
    avg_per_hour = "$" + avg_per_hour.toFixed(2);
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
    table_header.append(
        $('<th>').text('Date'),
        $('<th>').text('Weekday'),
        $('<th>').text('Total Earned'),
        $('<th id="time_worked" title="Time elapsed from first ride request to last dropoff">').text('Time Worked'),
        $('<th>').text('Rate/Hr'),
        $('<th>').text('Total Rides'),
        $('<th>').text('Rate/Ride')
    );
    $.get(url,
        function(data) {
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
            getStats(dataTable.data());
            $('#avg_per_hour p').html(avg_per_hour);
            $('#avg_per_unit h3').html('Avg Daily Rate');
            $('#avg_per_unit p').html(avg_per_unit);
            $('#total_earned p').html(sum_total_earned);

            if (weekday == null) {
                drawWeekGraph(formatGraphData(dataTable.data()));
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
    table_header.find('th').remove();
}

// CREATE DATATABLE USING API CALL TO GET WEEKSTATEMENTS
function drawWeekTable(month = m) {
    m = month
    var url = '/api/week_statements/?driver=' + driverID
    if (month) {
        url += '&month=' + month
    }
    table_header.append(
        $('<th>').text('Starting'),
        $('<th>').text('Ending'),
        $('<th>').text('Total Earned'),
        $('<th>').text('Rate/Day'),
        $('<th>').text('Rate/Hr'),
        $('<th>').text('Total Rides'),
        $('<th>').text('Rate/Ride')
    );
    $.get(url,
        function(data) {
            window.dataTable = $('#table_id').DataTable({
                "pageLength": 30,
                "bLengthChange": false,
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
            $('#avg_per_hour p').html(avg_per_hour);
            $('#avg_per_unit h3').html('Avg Weekly Rate');
            $('#avg_per_unit p').html(avg_per_unit);
            $('#total_earned p').html(sum_total_earned);
        }
    );
};

// FIND DAILY/WEEKLY OPTION SELECTED IN DROPDOWN (0=DAILY, 1=WEEKLY)
var filterSelection = document.getElementById('data_type').selectedIndex;

// DETERMINE DAILY/WEEKLY OPTION SELECTED AND REDRAW FILTERED TABLE
function filterTable(m, w) {
    destroyTable();
    if (filterSelection == 0) {
        drawDayTable(m, w);
    }
    else {
        drawWeekTable(m);
    }
};

// CREATE INITIAL TABLE OF ALL DAYSTATEMENT, HOOK-UP DAILY/WEEKLY DROPDOWN
$(document).ready(function() {
    drawDayTable();

    $('#data_type').change(function() {
        filterSelection = document.getElementById('data_type').selectedIndex;
        filterTable(m, w);
    });

});

// LINK WEEKDAY CHART (ONCE IT'S LOADED) TO REDRAWING FILTERED TABLE
function onChart1Created() {
    d3.select('#chart1 svg')
        .selectAll('.discreteBar')
        .on('click',
            function (d) {
                document.getElementById('data_type').selectedIndex = 0
                filterSelection = 0
                filterTable(m, d['label'])
            }
        );
};

// LINK MONTH CHART (ONCE IT'S LOADED) TO REDRAWING FILTERED TABLE
function onChart2Created() {
    d3.select('#chart2 svg')
        .selectAll('.discreteBar')
        .on('click',
            function (d) {
                filterTable(d['label'])
            }
        );
};

function formatGraphData(data) {
    graphData = [{key:"Avg Hourly Rate By Weekday", values:[]}];

    var mondaySum = 0
    var mondayCount = 0
    var tuesdaySum = 0
    var tuesdayCount = 0
    var wednesdaySum = 0
    var wednesdayCount = 0
    var thursdaySum = 0
    var thursdayCount = 0
    var fridaySum = 0
    var fridayCount = 0
    var saturdaySum = 0
    var saturdayCount = 0
    var sundaySum = 0
    var sundayCount = 0

    for (i in data) {
        if (data[i].weekday == "Monday") {
            mondaySum += Number(data[i].rate_per_hour.replace("$", ""))
            ++mondayCount
        }
        else if (data[i].weekday == "Tuesday") {
            tuesdaySum += Number(data[i].rate_per_hour.replace("$", ""))
            ++tuesdayCount
        }
        else if (data[i].weekday == "Wednesday") {
            wednesdaySum += Number(data[i].rate_per_hour.replace("$", ""))
            ++wednesdayCount
        }
        else if (data[i].weekday == "Thursday") {
            thursdaySum += Number(data[i].rate_per_hour.replace("$", ""))
            ++thursdayCount
        }
        else if (data[i].weekday == "Friday") {
            fridaySum += Number(data[i].rate_per_hour.replace("$", ""))
            ++fridayCount
        }
        else if (data[i].weekday == "Saturday") {
            saturdaySum += Number(data[i].rate_per_hour.replace("$", ""))
            ++saturdayCount
        }
        else if (data[i].weekday == "Sunday") {
            sundaySum += Number(data[i].rate_per_hour.replace("$", ""))
            ++sundayCount
        }
    };

    graphData[0]["values"].push(
        {"label": "Monday", "value": mondaySum / mondayCount},
        {"label": "Tuesday", "value": tuesdaySum / tuesdayCount},
        {"label": "Wednesday", "value": wednesdaySum / wednesdayCount},
        {"label": "Thursday", "value": thursdaySum / thursdayCount},
        {"label": "Friday", "value": fridaySum / fridayCount},
        {"label": "Saturday", "value": saturdaySum / saturdayCount},
        {"label": "Sunday", "value": sundaySum / sundayCount}
    );

    return graphData
};
