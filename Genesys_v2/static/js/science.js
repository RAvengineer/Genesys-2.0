function getSoilChecked() {
    return [
    $("#swtatmPressure").is(':checked'),
    $("#swtatmTemp").is(':checked'),
    $("#swtatmHum").is(':checked'),
    $("#swtCH4").is(':checked'),
    $("#swtUV").is(':checked'),
    $("#swtsoilTemp").is(':checked'),
    $("#swtsoilpH").is(':checked'),
    $("#swtsoilMoisture").is(':checked'),
    ];
}

setInterval(getSensorValues,data_refresh_interval);

function getSensorValues() {
    data_to_be_sent = {'SoilSensorsChecked':getSoilChecked()};
    $.ajax({
        type: "POST",
        url: "/getSensorValues",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data_to_be_sent),
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
}