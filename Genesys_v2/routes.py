from flask import render_template, request, Response,jsonify
from Genesys_v2 import app
from Utilities.CamFeed import CamFeed
from Utilities.GamepadControls import GamepadControls
from Utilities.GenerateCodeWord import GenerateCodeword
from Utilities.StationRoverSocket import StationRoverSocket

# Variables
cameraNumber = 0
gp = GamepadControls()
motorCommand = "Null"

# TODO: Remove later
from random import uniform


# Routes for Templates
@app.route('/')
@app.route('/Genesys_v2')
def genesys_v2():
    return render_template('base.html')


@app.route('/autonomous')
def autonomous():
    return render_template('autonomous.html')


@app.route('/manual')
def manual():
    return render_template('manual.html')


@app.route('/science')
def science():
    return render_template('science.html')


# Routes for Responsive WebPages
@app.route('/video_feed')
def video_feed():
    camera = CamFeed()
    return Response(camera.gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/changeCamera',methods=['POST'])
def changeCamera():
    global cameraNumber
    # method = GET
    # request.args returns ImmutableMultiDict type
    # print(request.args) gives ImmutableMultiDict([('{"cameraNumber":"2"}', '')])
    # print(request.args.to_dict()) gives {'{"cameraNumber":"2"}': ''}
    # print(list(request.args.to_dict().keys()))
    # method = POST
    # print(request.json['cameraNumber']) gives '2'
    # print(request.get_json()) gives {'cameraNumber': '2'}
    
    cameraNumber = request.json['cameraNumber'] # type(cameraNumber): <class 'str'>
    print("Camera Number Selected:",cameraNumber) # Debugging

    socket = StationRoverSocket(ip='127.0.0.1')
    gwc = GenerateCodeword()
    codeWord = gwc.parseCamera(int(cameraNumber))

    socket.testSend(codeWord.to_bytes(3,'little'))
    
    return jsonify(status="changed")

@app.route('/gamepadKeys',methods=['POST'])
def gamepadKeys():
    global motorCommand
    motorCommand = request.json['command']
    print(motorCommand) # Debugging

    socket = StationRoverSocket(ip='127.0.0.1')
    gpc = GamepadControls()
    codeWord = gpc.getCodeWord(motorCommand)

    if(codeWord!=-1):
        socket.testSend(codeWord)
    return jsonify(status="Motor Command Received")

@app.route('/addGPS')
def addGPS():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/getElectricalGpsValues', methods=['POST'])
def getElectricalGpsValues():
    # Get Checked Electrical Sensors
    electricalSensorsChecked = request.json['ElectricalSensorsChecked']
    print(electricalSensorsChecked) # Debugging
    sensorValues = ["Null" for i in range(8)]

    socket = StationRoverSocket(ip='127.0.0.1')
    gcw = GenerateCodeword()

    for index,check in enumerate(electricalSensorsChecked):
        if(check):
            codeWord = gcw.parseElectrical(index+1)
            socket.testSend(codeWord)
            sensorValues[index] = round(uniform(0.0,5.0),1)

    # Request GPS,receive it and send it to front-end
    codeWord = gcw.parseGpsRequest()
    socket.testSend(codeWord)
    current_gps = "CURRENT_GPS" # TODO: add recieve function here

    return jsonify(
        current_gps = current_gps,
        battery1=sensorValues[0],
        battery2=sensorValues[1],
        motor1=sensorValues[2],
        motor2=sensorValues[3],
        motor3=sensorValues[4],
        motor4=sensorValues[5],
        motor5=sensorValues[6],
        motor6=sensorValues[7]
    )

@app.route('/getSensorValues')
def getSensorValues():
    atmPressure = round(uniform(1004.79,1004.90),2)
    atmTemp = round(uniform(27.00,29.00),2)
    atmHum = round(uniform(55.00,60.00),2)
    CH4 = round(uniform(1.850,1.854),3)
    UV = round(uniform(0,3),0)
    soilTemp = round(uniform(26.00,30.00),2)
    soilpH = round(uniform(5,7),0)
    soilMoisture = round(uniform(50,65),2)
    return jsonify(
        atmPressure = atmPressure,
        atmTemp=atmTemp,
        atmHum=atmHum,
        CH4=CH4,
        UV=UV,
        soilTemp=soilTemp,
        soilpH=soilpH,
        soilMoisture=soilMoisture,
    )
"""
TODO 1: Take gamepad values
        SetInterval for calling the route '/gamepadEvents'
        Create a class in Utilities for Gamepad Events
        Distinguish the controls using if case, ex. ('base','forward'), ('arm','AC1')
        Jsonify and send it to the client and display in the motors status
TODO 2: update values periodically
        Socket
TODO 3: addGPS
TODO 4: Autonomous --DONE
        Detection Status(left arrow, right arrow, ball) --Done
        Status Button For Autonomous --Done
TODO 5: Hotkey Commands for Science(0-9) --DONE
TODO 6: Fail Safe for Gamepad
        Also, add a code for controlling the rover through keyboard
"""


@app.route('/user/<username>')
def profile(username):
    print(f'The username is {username}')
    return f'<h1>{username}<h1>'
