// Variables
var gamepad_NULL = "Null";
var prevCommand = window.gamepad_NULL;
var isGamepadActive = false;
var inArmMode = false;
var baseCommands = [
    "Backward",
    "Right",
    "Left",
    "Forward",
    window.gamepad_NULL,
    window.gamepad_NULL,
    "Decrease PWM",
    "Increase PWM",
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
];
var armCommands = [
    "Actuator 2 RETRACT",
    "Actuator 3 RETRACT",
    "Actuator 3 EXTEND",
    "Actuator 2 EXTEND",
    "Gripper Rotate LEFT",
    "Gripper Rotate RIGHT",
    "Gripper OPEN",
    "Gripper CLOSE",
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
    window.gamepad_NULL,
    "Actuator 1 EXTEND",
    "Actuator 1 RETRACT",
    "ARM Base Left",
    "ARM Base Right",
    window.gamepad_NULL,
];
/*
Index   Keys
0       A
1       B
2       X
3       Y
4       Bumper Left
5       Bumper Right
6       Trigger Left
7       Trigger Right
8       Back
9       Start
10      Unknown
11      Unknown
12      Button Up
13      Button Down
14      Button Left
15      Button Right
16      HOME
*/

window.addEventListener('gamepadconnected', event=>{
    console.log("Gamepad Connected!");
    console.log(event.gamepad);
});

window.addEventListener('gamepaddisconnected', event=>{
    console.log("Gamepad Disconnected!");
    console.log(event.gamepad);
});

function getParsedCommand(gamepad){
    // For Axes

    // For Buttons and Triggers
    var i;
    for (i = 0; i < gamepad.buttons.length; i++) {
        if(gamepad.buttons[i].pressed){
            // Gamepad On/Off
            if(i===9)
            return "gOF"; // gamepadOnOff
            // Toggle Mode: Arm or Wheels 
            else if(i===8)
            return "tm"; // toggleMode

            if(window.inArmMode)
            return window.armCommands[i];
            else
            return window.baseCommands[i];
        }
    }
    if(i===gamepad.buttons.length)
    return "STOP";

}


function gamepadStatusMode(command) {
    if(command==="gOF"){
        window.isGamepadActive = !window.isGamepadActive;
        window.inArmMode = false; // Reset the mode
        if(window.isGamepadActive)
        {$("#gamepadStatus").text("Gamepad ON");}
        else
        {$("#gamepadStatus").text("Gamepad OFF");}
        return window.gamepad_NULL;
    }
    else if(command==="tm"){
        window.inArmMode = !window.inArmMode;
        if(window.inArmMode)
        $("#gamepadStatus").text("Arm Mode");
        else
        $("#gamepadStatus").text("Base Wheels Mode");
        return window.gamepad_NULL;
    }
    return command;  
}


function sendDataToBackend(command){
    $.ajax({
        type: "POST",
        url: "/gamepadKeys",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({"command":command}),
    });
}


function addCssToStatus(command) {
    if(window.inArmMode){
        $("#BaseStatus").text("IDLE");
        $("#BaseStatus").attr("class","p-3 mb-2 rounded bg-primary text-center text-white");
        if(command==="STOP")
        $("#ArmStatus").attr("class","p-3 mb-2 rounded bg-danger text-center text-white");
        else if(command===window.gamepad_NULL)
        $("#ArmStatus").attr("class","p-3 mb-2 rounded bg-warning text-center text-white");
        else
        $("#ArmStatus").attr("class","p-3 mb-2 rounded bg-success text-center text-white");
    }
    else{
        $("#ArmStatus").text("IDLE");
        $("#ArmStatus").attr("class","p-3 mb-2 rounded bg-primary text-center text-white");
        if(command==="STOP")
        $("#BaseStatus").attr("class","p-3 mb-2 rounded bg-danger text-center text-white");
        else if(command===window.gamepad_NULL)
        $("#BaseStatus").attr("class","p-3 mb-2 rounded bg-warning text-center text-white");
        else
        $("#BaseStatus").attr("class","p-3 mb-2 rounded bg-success text-center text-white");
    }
    if(!window.isGamepadActive){
        $("#BaseStatus").text("IDLE");
        $("#BaseStatus").attr("class","p-3 mb-2 rounded bg-primary text-center text-white");
        $("#ArmStatus").text("IDLE");
        $("#ArmStatus").attr("class","p-3 mb-2 rounded bg-primary text-center text-white");
    }
}


function update(){
    const gamepads = navigator.getGamepads()
    if(gamepads[0]){
        var command = getParsedCommand(gamepads[0])
        if(command!==window.prevCommand){
            temp = window.prevCommand; // Line Number 150 to understand, why?
            window.prevCommand = command;
            command = gamepadStatusMode(command);
            
            // If isGamepadActive === false, then all inputs must be registered as Null
            if(!window.isGamepadActive && command!=="STOP")
            command = window.gamepad_NULL;
            // Send the command to the backend
            console.log(command);
            if(window.isGamepadActive){
                if(command==="STOP")
                sendDataToBackend(command+" "+temp);
                else
                sendDataToBackend(command);
            } 

            // Display it in the interface
            if(window.inArmMode)
            $("#ArmStatus").text(command);
            else
            $("#BaseStatus").text(command);

            // Make the display look cooler
            addCssToStatus(command);
        }
    }
    window.requestAnimationFrame(update);
}
window.requestAnimationFrame(update);

/*
References:
* Controller.js: https://samiare.github.io/Controller.js/
* Implementing controls using the Gamepad API - Game development | MDN: https://developer.mozilla.org/en-US/docs/Games/Techniques/Controls_Gamepad_API
* (109) How to Connect a Gamepad to the Browser [ HTML5 Gamepad API ] - YouTube: https://www.youtube.com/watch?v=T8vi1JZyjhs
* HTML5 Gamepad Tester - For Developers: https://html5gamepad.com/for-developers
* Using the Gamepad API - Web APIs | MDN: https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API
* Gamepad API - Web APIs | MDN: https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API
* luser.github.io/gamepadtest/: http://luser.github.io/gamepadtest/
* gamepadtest/gamepadtest.js at master · luser/gamepadtest: https://github.com/luser/gamepadtest/blob/master/gamepadtest.js
*/