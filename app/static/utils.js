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
    });
});