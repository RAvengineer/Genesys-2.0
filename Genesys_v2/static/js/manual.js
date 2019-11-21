setInterval(getGamepadKeys,data_refresh_interval);

function getGamepadKeys(){
    $.ajax({
        url: "/getGamepadKeys",
        success: updateRoverMotorsStatus,
        fail: function(){
            console.log("Get Gamepad Keys in manual.js FAILED");
        }
    });
}

function updateRoverMotorsStatus(data){
    if(data.mode==="baseMotors"){
        $("#BaseStatus").text(data.command)
    }
}