function updateLocationList(data){

}

$("#btnAddGPS").on("click",function () {
    data_to_be_sent = {
        "addGpsLat":$("#addGpsLat").val(),
        "addGpsLon":$("#addGpsLon").val(),
    }
    $.ajax({
        type: "POST",
        url: "/addGPS",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data_to_be_sent),
        success:updateLocationList,
        fail: function(){
            console.log("Add GPS co-ordinates in autonomous.js failed");
        }
    });
    $("#addGpsLat").val("");
    $("#addGpsLon").val("");
});