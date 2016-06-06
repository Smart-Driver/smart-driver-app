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

function createWeeklyTable() {
    $.get('/api/week_statements/?driver=' + driverID,
        function(data) {
            $('#table_id').DataTable().destroy();
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
                ]
            });
        }
    )
}

$('#createWeek').click(function() {
    $.get('/api/week_statements/?driver=' + driverID,
        function(data) {
            $('#table_id').DataTable().destroy();
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
                ]
            });
        }
    )
})

// var $timeWorkedHeader = $('#table_id').find('th[name="Time Worked"]');
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
