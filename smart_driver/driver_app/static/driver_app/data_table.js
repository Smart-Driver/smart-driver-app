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
        $('<th>').text('Time Worked'),
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
            console.log(getTotalEarned(dataTable.data()))

            // console.log(getTotalEarned(getPageData()))
        });
}

// GET DATA FOR THE WHOLE TABLE
function getTotalEarned(data) {
  var total_earned = 0;
  for (var i = 0; i < data.length; i++) {
    var row = data[i];
    total_earned += parseFloat(row.total_earned.substr(1))
  }
  return total_earned;
}

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
            });
}

function onChart2Created() {
    d3.select('#chart2 svg')
        .selectAll('.discreteBar')
        .on('click',
            function (d) {
                filterTable(d['label'])
            });
}
