var driverID = $('#driver_id').val()

$(document).ready(function(){
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
                ]
            });
        }
    )
});

var $timeWorkedHeader = $('#table_id').find('th[name="Time Worked"]');
// $('#deltaDescription').hide()
// $timeWorkedHeader.hover(function(){
//     $('#deltaDescription').show();
//     }, function(){
//     $('#deltaDescription').hide();
// });

// sudo code for wiring up buttons to different views:
// $(document).ready(function(){
//     $('#table_id').DataTable({
//         ajax: 'url'
//     });
// });
//
// button.click(function() {
//     deleteOldDataTable();
//     createNewDataTable();
// })
