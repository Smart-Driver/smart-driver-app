var table_header = $('#table_id').find('tr')
var driverID = $('#driver_id').val()

function drawDayTable() {
    table_header.append(
        $('<th>').text('Date'),
        $('<th>').text('Weekday'),
        $('<th>').text('Total Earned'),
        $('<th>').text('Time Worked'),
        $('<th>').text('Rate/Hr'),
        $('<th>').text('Total Rides'),
        $('<th>').text('Rate/Ride')
    );
    $.get('/api/day_statements/?driver=' + driverID,
        function(data) {
            $('#table_id').DataTable({
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
        }
    );
}

function destroyTable() {
    $('#table_id').DataTable().destroy();
    table_header.find('th').remove();
}

function drawWeekTable() {
    table_header.append(
        $('<th>').text('Starting'),
        $('<th>').text('Ending'),
        $('<th>').text('Total Earned'),
        $('<th>').text('Avg Rate/Day'),
        $('<th>').text('Avg Rate/Hr'),
        $('<th>').text('Total Rides'),
        $('<th>').text('Rate/Ride')
    );
    $.get('/api/week_statements/?driver=' + driverID,
       function(data) {
           $('#table_id').DataTable({
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

var a = document.getElementById('data_type').selectedIndex

$(document).ready(function() {
    drawDayTable();

    $('#data_type').change(function() {
        a = document.getElementById('data_type').selectedIndex;
        if (a == 0) {
            destroyTable();
            drawDayTable();
        }
        else {
            destroyTable();
            drawWeekTable();
        }
    });

});
