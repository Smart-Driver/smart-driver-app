

$(document).ready(function(){

  var a = document.getElementById('data_type').selectedIndex
  var table_header = $('#table_id').find('tr')
  if (a == 0){
    table_header.append(
      $('<th>').text('Date'),
      $('<th>').text('Weekday'),
      $('<th>').text('Total Earned'),
      $('<th>').text('Time Worked'),
      $('<th>').text('Rate/Hr'),
      $('<th>').text('Total Rides'),
      $('<th>').text('Rate/Ride')
    );
    $.get('/api/day_statements',
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
                ]
            });
        }
    );

  }

});
