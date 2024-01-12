function deleteRecord(recordId, type){
    fetch('/delete-record',{
        method: 'POST',
        body: JSON.stringify({recordId: recordId, type: type})
    }).then((_res) =>{
        window.location.reload();
    })
}

$(document).ready(function(){
    $('#datePicker').datepicker({
      format: 'mm/yyyy',
      startDate: '01/1970',  // Set your desired start date (in the format MM/YYYY)
      endDate: new Date().toISOString().split('T')[0],  // Set end date to current date
      autoclose: true,
      todayHighlight: true,
      minViewMode: 1,  // Set the minViewMode to 1 to show only month and year
      changeMonth: false, // Disable the ability to change months
      changeYear: false,  // Disable the ability to change years
      beforeShow: function(input, inst) {
            $(input).prop('readonly', true); // Make the input field readonly
        }
    });
});

// function initializeDatepicker(fieldId) {
//     // generic date setter for all forms
//     $("#" + fieldId).datepicker({
//         dateFormat: 'yy-mm-dd',
//         minDate: new Date()
//     });
// }

$(document).ready(function(){
    var currentDate = new Date();
    var currentMonth = currentDate.getMonth() + 1; // Adding 1 because months are zero-indexed
    var currentYear = currentDate.getFullYear();
    var currentDay = currentDate.getDate();

    var start_date = "01/"+this_month+"/"+this_year;
    // Check conditions and update accordingly
    if (this_year < currentYear || (this_year === currentYear && this_month < currentMonth)) {
        // Use the last day of the given month
        var lastDay = new Date(this_year, this_month, 0).getDate();
        var end_date = lastDay + "/" + this_month + "/" + this_year;
    } else {
        // Use the current day
        var end_date = currentDay + "/" + this_month + "/" + this_year;
    }
    $('#outcome-date').datepicker({
      format: 'dd/mm/yyyy',
      startDate: start_date,
      endDate: end_date,
      autoclose: true,
      // todayHighlight: true,
      changeMonth: false, // Disable the ability to change months
      changeYear: false,  // Disable the ability to change years
      changeDay: false,
      beforeShow: function(input, inst) {
            $(input).prop('readonly', true); // Make the input field readonly
      }
    });

     $('#income-date').datepicker({
      format: 'dd/mm/yyyy',
      startDate: start_date,
      endDate: end_date,
      autoclose: true,
      todayHighlight: true,
      changeMonth: false, // Disable the ability to change months
      changeYear: false,  // Disable the ability to change years
      changeDay: false,
      beforeShow: function(input, inst) {
            $(input).prop('readonly', true); // Make the input field readonly
      }
    });

     $('#goal-progress-date').datepicker({
      format: 'dd/mm/yyyy',
      startDate: start_date,
      endDate: end_date,
      autoclose: true,
      todayHighlight: true,
      changeMonth: false, // Disable the ability to change months
      changeYear: false,  // Disable the ability to change years
      changeDay: false,
      beforeShow: function(input, inst) {
            $(input).prop('readonly', true); // Make the input field readonly
      }
    });

      $('#goal-deadline').datepicker({
      format: 'dd/mm/yyyy',
      startDate: (currentDay+1) + "/" + currentMonth + "/" + currentYear,
      autoclose: true,
      todayHighlight: true,
      changeMonth: false, // Disable the ability to change months
      changeYear: false,  // Disable the ability to change years
      changeDay: false,
      beforeShow: function(input, inst) {
            $(input).prop('readonly', true); // Make the input field readonly
      }
    });
});