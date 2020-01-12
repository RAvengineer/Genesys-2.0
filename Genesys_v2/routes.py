from flask import render_template, request, Response,jsonify
from Genesys_v2 import app
from Utilities.CamFeed import CamFeed
from AutonomousDarknet.AutoDarknet import AutoDarknet
from Utilities.GamepadControls import GamepadControls
from Utilities.GenerateCodeWord import GenerateCodeword
from Utilities.XBeeCommunications import xbeeCom

import struct

# Variables
cameraNumber = 0
gp = GamepadControls()
motorCommand = "Null"
gpsLocations = []
serial_port = '/dev/xbee'
cameraDevicePortNumber = 0
autoDarknet = None
sensorCalc = [
   #[Integer, slice, function],
    [True,lambda x:x[0], lambda x: 100-(x*100)/255],   # Moisture
    [True,lambda x:x[1], lambda x: x], # UV Index
    [True,lambda x:x[2], lambda x: x*5*3.5/255],   # pH
    [True,lambda x:x[3], lambda x: log(((10/x*11.82)*(255-x))-1.33)/(-0.318)], # Methane # log(((10/x*r0)*(255-x))-b)/m
    [True,lambda x:x[4:6], lambda x: x],    # Temperature
    [True,lambda x:x[6], lambda x: (x*4.0)/(256*0.2)], # Battery 1
    [True,lambda x:x[7], lambda x: (x*4.0)/(256*0.2)], # Battery 2
    [False,lambda x:x[8:12], lambda x: x],    # Pressure
    [False,lambda x:x[12:16], lambda x: x],    # Atm Temperature
    [False, lambda x:x[16:20], lambda x: x],    # Humidity
]

# Objects/ Instances
xbee_com = xbeeCom(serial_port)


# TODO: Remove later
from random import uniform


# Routes for Templates
@app.route('/')
@app.route('/Genesys_v2')
def genesys_v2():
    global autoDarknet
    if(autoDarknet):
        del(autoDarknet)
        autoDarknet = None
    return render_template('base.html')


@app.route('/autonomous')
def autonomous():
    global autoDarknet
    if(autoDarknet):
        del(autoDarknet)
        autoDarknet = None
    return render_template('autonomous.html')


@app.route('/manual')
def manual():
    global autoDarknet
    if(autoDarknet):
        del(autoDarknet)
        autoDarknet = None
    return render_template('manual.html')


@app.route('/science')
def science():
    global autoDarknet
    if(autoDarknet):
        del(autoDarknet)
        autoDarknet = None
    return render_template('science.html')


# Routes for Responsive WebPages
@app.route('/video_feed')
def video_feed():
    global cameraDevicePortNumber
    camera = CamFeed(cameraDevicePortNumber)
    return Response(camera.gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/darknet_video_feed')
def darknet_video_feed():
    global autoDarknet, cameraDevicePortNumber
    autoDarknet = AutoDarknet(cameraDevicePortNumber)
    return Response(autoDarknet.gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/getDetObj')
def getDetObj():
    global autoDarknet
    if(autoDarknet):
        print(autoDarknet.object_detected)  # Debugging
        return jsonify(detected_object=autoDarknet.object_detected)
    else:
        print("No AutoDarknet Object found!")
        return jsonify(detected_object="Null")


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

    # global serial_port # TODO: Uncomment this
    # xbee_com = xbeeCom(serial_port) # TODO: Uncomment this
    gwc = GenerateCodeword()
    codeWord = gwc.parseCamera(int(cameraNumber))

    # xbee_com.send_data(codeWord) # TODO: Uncomment this
    
    return jsonify(status="changed")

@app.route('/gamepadKeys',methods=['POST'])
def gamepadKeys():
    global motorCommand
    motorCommand = request.json['command']
    print(motorCommand) # Debugging

    global xbee_com
    # xbee_com = xbeeCom(serial_port)
    gpc = GamepadControls()
    codeWord = gpc.getCodeWord(motorCommand)

    if(codeWord!=-1):
        xbee_com.send_data(codeWord)
    return jsonify(status="Motor Command Received")

@app.route('/addGPS', methods=['POST'])
def addGPS():
    addLat = request.json["addGpsLat"]
    addLon = request.json["addGpsLon"]
    print(addLat,addLon) # Debugging

    global gpsLocations
    gpsLocations.append([addLat,addLon,False])
    return jsonify(gpsData=gpsLocations)

@app.route('/getSensorValues')
def getSensorsValues():
    print("get Sensor Values") # Debugging
    sensorValues = ["Null" for i in range(10)]

    # global serial_port # TODO: Uncomment this
    # xbee_com = xbeeCom(serial_port) # TODO: Uncomment this
    gcw = GenerateCodeword()

    codeWord = gcw.parseSensors()
    # xbee_com.send_data(codeWord) # TODO: Uncomment this
    # received_data = xcom.receive_data(20)

    # Remove this 'for' as this gives only dummy data
    for index in range(10):
        sensorValues[index] = round(uniform(0.0,5.0),1)
    # Actual value calculations
    """global sensorCalc
    for i in range(10):
        if(sensorCalc[i][0]):
            data = sensorCalc[i][1](received_data)
            if(str(type(data))=="<class 'int'>"):
                data = data.to_bytes(4,byteorder="little")
            data = int.from_bytes(
                data,
                byteorder="little",
                signed=False
            )
        else:
            data = struct.unpack('f',sensorCalc[i][1](received_data))
        
        print(i,sensorCalc[i][1](received_data))
        sensorValues[i] = sensorCalc[i][2](data)"""

    return jsonify(
        soilMoisture=sensorValues[0],
        soilpH=sensorValues[1],
        UV=sensorValues[2],
        CH4=sensorValues[3],
        soilTemp=sensorValues[4],
        battery1=sensorValues[5],
        battery2=sensorValues[6],
        atmPressure=sensorValues[7],
        atmTemp=sensorValues[8],
        atmHum=sensorValues[9]
    )

@app.route('/getGpsValues')
def getGpsValues():
    print("get GPS Values") # Debugging

    # global serial_port # TODO: Uncomment this
    # xbee_com = xbeeCom(serial_port) # TODO: Uncomment this
    gcw = GenerateCodeword()

    # Request GPS,receive it and send it to front-end
    codeWord = gcw.parseGpsRequest()
    # xbee_com.send_data(codeWord) # TODO: Uncomment this
    current_gps = "CURRENT_GPS" # TODO: add recieve function here

    return jsonify(
        current_gps = current_gps
    )
"""
TODO 1: Fail Safe for Gamepad
        Also, add a code for controlling the rover through keyboard
TODO 2: Add Check to analyze Current GPS and Next GPS
"""


@app.route('/user/<username>')
def profile(username):
    print(f'The username is {username}')
    return f'<h1>{username}<h1>'
