var data_refresh_interval = 1000; // in (ms)

$("#cameraNumber").on('change',function(){
    data_to_be_sent = {'cameraNumber':this.value};
    $.ajax({
        type: "POST",
        url: "/changeCamera",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data_to_be_sent),
    });
});

setInterval(getSensorValues,20000);
setInterval(getGpsCompassValues,data_refresh_interval*3);
// setInterval(getCompassValues,1531);

function getSensorValues() {
    if($("#swtSensors").is(':checked')){
        $.ajax({
            url: "/getSensorValues",
            contentType: 'application/json',
            success:updateSensorValues,
            fail: function(){
                console.log("Get Electrical Values in common.js failed");
            }
        });
    }
}

function updateSensorValues(data) {
    // console.log("Updating Electrical Sensor Values"); // Debugging
    $("#battery1").text(data.battery1);
    $("#battery2").text(data.battery2);

    // console.log("Updating Sensors"); // Debugging
    $("#atmPressure").text(data.atmPressure);
    $("#atmTemp").text(data.atmTemp);
    $("#atmHum").text(data.atmHum);
    $("#CH4").text(data.CH4);
    $("#UV").text(data.UV);
    $("#soilTemp").text(data.soilTemp);
    $("#soilpH").text(data.soilpH);
    $("#soilMoisture").text(data.soilMoisture);
}


function getGpsCompassValues() {
    $.ajax({
        url: "/getGpsCompassValues",
        contentType: 'application/json',
        success:updateGpsCompassValues,
        fail: function(){
            console.log("Get GPS and Compass Values in common.js failed");
        }
    });
}

function updateGpsCompassValues(data) {
    console.log("Updating GPS and Compass"); // Debugging
    $("#currentGPS").text(data.current_gps);
    $("#compass").text(data.magnetometer);
}

/*
NOTE: For using Ajax, see to it that you have included the uncompressed version of JQuery!

References for Ajax:
https://code-maven.com/slides/python-programming/flask-and-ajax-jquery
https://flask.palletsprojects.com/en/1.1.x/patterns/jquery/
https://learn.jquery.com/ajax/jquery-ajax-methods/
*/
