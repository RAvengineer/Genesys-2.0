function updateLocationList(data){
    gpsList = data.gpsData;
    HfLT = "" // HTML for Location Table
    gpsList.forEach(gps => {
        if(gps[2]){
            HfLT += (
                "<tr><td class='bg-success'>" 
                + gps[0] 
                + "&#176; N "
                + gps[1]
                + "&#176; E</td></tr>"
            );
        }
        else{
            HfLT += (
                "<tr><td>" 
                + gps[0] 
                + "&#176; N "
                + gps[1]
                + "&#176; E</td></tr>"
            );
        }
    });
    $("#locationTable").html(HfLT);
}

$("#btnAddGPS").on("click",function () {
    data_to_be_sent = {
        "addGpsLat":$("#addGpsLat").val(),
        "addGpsLon":$("#addGpsLon").val(),
    }
    if($("#addGpsLat").val()!=="" && $("#addGpsLon").val()!=="")
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