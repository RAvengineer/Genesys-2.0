setInterval(getGamepadKeys,100);

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
    if(data.mode==="0"){
        $("#BaseStatus").text(data.command)
    }
}