console.log('julio')
$(document).ready(function(){
    $('#table_id').DataTable({
        "ajax": '/api/day_statements'
    });
});

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
