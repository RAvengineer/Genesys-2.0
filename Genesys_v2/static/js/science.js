setInterval(getSensorValues,data_refresh_interval);

function getSensorValues() {
    $.ajax({
        url: "/getSensorValues",
        success:updateSensorValues,
        fail: function(){
            console.log("Get Sensor Values in science.js failed");
        }
    });
}

function updateSensorValues(data) {
    // console.log("Updating Sensors"); // Debugging
    $("#atmPressure").text(data.atmPressure);
    $("#atmTemp").text(data.atmTemp);
    $("#atmHum").text(data.atmHum);
    $("#CH4").text(data.CH4);
    $("#UV").text(data.UV);
    $("#soilTemp").text(data.soilTemp);
    $("#soilpH").text(data.soilpH);
    $("#soilMoisture").text(data.soilMoisture);
    $("#motor6").text(data.motor6);
}