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
gpsLocations = []

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

    socket.testSend(codeWord)
    
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

@app.route('/addGPS', methods=['POST'])
def addGPS():
    addLat = request.json["addGpsLat"]
    addLon = request.json["addGpsLon"]
    print(addLat,addLon) # Debugging

    global gpsLocations
    gpsLocations.append([addLat,addLon,False])
    return jsonify(gpsData=gpsLocations)

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

@app.route('/getSensorValues', methods=['POST'])
def getSensorValues():
    # Get Checked Soil Sensors
    soilSensorsChecked = request.json['SoilSensorsChecked']
    print(soilSensorsChecked) # Debugging
    sensorValues = ["Null" for i in range(8)]

    socket = StationRoverSocket(ip='127.0.0.1')
    gcw = GenerateCodeword()

    for index,check in enumerate(soilSensorsChecked):
        if(check):
            codeWord = gcw.parseSoil(index+1)
            socket.testSend(codeWord)
            sensorValues[index] = round(uniform(0.0,5.0),1) # TODO: Replace with receive function

    return jsonify(
        atmPressure = sensorValues[0],
        atmTemp=sensorValues[1],
        atmHum=sensorValues[2],
        CH4=sensorValues[3],
        UV=sensorValues[4],
        soilTemp=sensorValues[5],
        soilpH=sensorValues[6],
        soilMoisture=sensorValues[7],
    )
"""
TODO: Fail Safe for Gamepad
        Also, add a code for controlling the rover through keyboard
"""


@app.route('/user/<username>')
def profile(username):
    print(f'The username is {username}')
    return f'<h1>{username}<h1>'
