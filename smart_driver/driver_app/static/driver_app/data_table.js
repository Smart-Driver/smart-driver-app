

var table_header = $('#table_id').find('tr')
var driverID = $('#driver_id').val()
var m = null
var w = null

function drawDayTable(month = m, weekday = w) {
    m = month
    w = weekday
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

            avg_per_unit = getAvg(dataTable.data())
            document.getElementById('total_earned').innerHTML = sum_total_earned
            document.getElementById('avg_per_unit').innerHTML = avg_per_unit
            document.getElementById('avg_per_hour').innerHTML = avg_per_hour

            // console.log(getTotalEarned(getPageData()))
        });
        $("#time_worked").qtip({
          position: {
            at: 'bottom center',
          }
        });
}

// GET AVERAGES FOR total_earned,rate_per_hour,  ... COLLUMNS USING DATA FOR THE WHOLE TABLE
var sum_total_earned = 0;
var avg_per_unit = 0;
var avg_per_hour = 0;

function getAvg(data) {
    var sum_total = 0
    var sum_rate_per_unit = 0;
    var sum_rate_per_hour = 0;

    for (var i = 0; i < data.length; i++) {
        var row = data[i];
        sum_total += parseFloat(row.total_earned.substr(1));
        sum_rate_per_hour += parseFloat(row.total_earned.substr(1));
    };

    sum_total_earned = sum_total.toFixed(2);
    avg_per_unit = sum_total_earned / (--i);
    sum_total_earned = "$" + sum_total_earned.toLocaleString();

    avg_per_hour = sum_rate_per_hour / (--i);
    avg_per_hour = "$" + avg_per_hour.toLocaleString();

    return '$' + avg_per_unit.toLocaleString();
};

// GET DATA FOR CURRENT ENTRIES SHOWN IN TABLE
// function getPageData() {
//   var pageData = [];
//   var data = dataTable.data();
//   var rows = dataTable.rows()[0];
//   var pageInfo = dataTable.page.info();
//   for (var i = pageInfo.start; i < pageInfo.end; i++) {
//     pageData.push(data[rows[i]]);
//   }
//   return pageData;
// }



// --------------------------------------------------------------------------

function destroyTable() {
    $('#table_id').DataTable().destroy();
    table_header.find('th').remove();
}

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
        $('<th>').text('Avg Rate/Day'),
        $('<th>').text('Avg Rate/Hr'),
        $('<th>').text('Total Rides'),
        $('<th>').text('Rate/Ride')
    );
    $.get(url,function(data) {
         $('#table_id').DataTable({
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


        }
    );
}

var filterSelection = document.getElementById('data_type').selectedIndex

function filterTable(m, w) {
    destroyTable();
    if (filterSelection == 0) {
        drawDayTable(m, w);
    }
    else {
        drawWeekTable(m);
    }
}

$(document).ready(function() {
    drawDayTable();

    $('#data_type').change(function() {
        filterSelection = document.getElementById('data_type').selectedIndex;
        filterTable(m, w);
    });

});

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
}

function onChart2Created() {
    d3.select('#chart2 svg')
        .selectAll('.discreteBar')
        .on('click',
            function (d) {
                filterTable(d['label'])
            }
        );
}
