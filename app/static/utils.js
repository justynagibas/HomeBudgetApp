function deleteRecord(recordId, type){
    fetch('/delete-record',{
        method: 'POST',
        body: JSON.stringify({recordId: recordId, type: type})
    }).then((_res) =>{
        window.location.reload();
    })
}