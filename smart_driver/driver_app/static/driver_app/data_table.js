
var a = document.getElementById('data_type').selectedIndex
var table_header = $('#table_id').find('tr')


$(document).ready(function(){

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

  };

// $('#table_id').change(function() {
//     var a = selected
//     if a == 1
//       destroy table
//       table_header.remove()
//       $('#table_id').DataTable.destroy()
//       draw week table
//     if a == 0
//       draw day table
//
//     });

});
