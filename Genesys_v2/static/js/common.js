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


function getElectricalChecked() {
    return [
    $("#swtBattery1").is(':checked'),
    $("#swtBattery2").is(':checked'),
    $("#swtMotor1").is(':checked'),
    $("#swtMotor2").is(':checked'),
    $("#swtMotor3").is(':checked'),
    $("#swtMotor4").is(':checked'),
    $("#swtMotor5").is(':checked'),
    $("#swtMotor6").is(':checked'),
    ];
}

setInterval(getElectricalGpsValues,data_refresh_interval);

function getElectricalGpsValues() {
    data_to_be_sent = {'ElectricalSensorsChecked':getElectricalChecked()};
    $.ajax({
        type: "POST",
        url: "/getElectricalGpsValues",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data_to_be_sent),
        success:updateElectricalGpsValues,
        fail: function(){
            console.log("Get Electrical Values in common.js failed");
        }
    });
}

function updateElectricalGpsValues(data) {
    // console.log("Updating"); // Debugging
    $("#currentGPS").text(data.current_gps);
    $("#battery1").text(data.battery1);
    $("#battery2").text(data.battery2);
    $("#motor1").text(data.motor1);
    $("#motor2").text(data.motor2);
    $("#motor3").text(data.motor3);
    $("#motor4").text(data.motor4);
    $("#motor5").text(data.motor5);
    $("#motor6").text(data.motor6);
}

/*
NOTE: For using Ajax, see to it that you have included the uncompressed version of JQuery!

References for Ajax:
https://code-maven.com/slides/python-programming/flask-and-ajax-jquery
https://flask.palletsprojects.com/en/1.1.x/patterns/jquery/
https://learn.jquery.com/ajax/jquery-ajax-methods/
*/