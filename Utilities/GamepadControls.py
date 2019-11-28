from Utilities.GenerateCodeWord import GenerateCodeword
gcw = GenerateCodeword()
commandsCodeWord = {
    # Base
    "Forward": gcw.parseBase("F"),
    "STOP Forward": gcw.parseBase("S"),
    "Backward": gcw.parseBase("B"),
    "STOP Backward": gcw.parseBase("S"),
    "Left": gcw.parseBase("L"),
    "STOP Left": gcw.parseBase("S"),
    "Right": gcw.parseBase("R"),
    "STOP Right": gcw.parseBase("S"),
    # ARM Base
    "ARM Base Left": gcw.parseArm("L"),
    "STOP ARM Base Left": gcw.parseArm("S"),
    "ARM Base Right": gcw.parseArm("R"),
    "STOP ARM Base Right": gcw.parseArm("S"),
    # Actuator 1
    "Actuator 1 EXTEND": gcw.parseActuator1("E"),
    "STOP Actuator 1 EXTEND": gcw.parseActuator1("S"),
    "Actuator 1 RETRACT": gcw.parseActuator1("R"),
    "STOP Actuator 1 RETRACT": gcw.parseActuator1("S"),
    # Actuator 2
    "Actuator 2 EXTEND": gcw.parseActuator2("E"),
    "STOP Actuator 2 EXTEND": gcw.parseActuator2("S"),
    "Actuator 2 RETRACT": gcw.parseActuator2("R"),
    "STOP Actuator 2 RETRACT": gcw.parseActuator2("S"),
    # Actuator 3
    "Actuator 3 EXTEND": gcw.parseActuator3("E"),
    "STOP Actuator 3 EXTEND": gcw.parseActuator3("S"),
    "Actuator 3 RETRACT": gcw.parseActuator3("R"),
    "STOP Actuator 3 RETRACT": gcw.parseActuator3("S"),
    #  Gripper Direction
    "Gripper Rotate LEFT": gcw.parseGripperDir("L"),
    "STOP Gripper Rotate LEFT": gcw.parseGripperDir("S"),
    "Gripper Rotate RIGHT": gcw.parseGripperDir("R"),
    "STOP Gripper Rotate RIGHT": gcw.parseGripperDir("S"),
    # Gripper State
    "Gripper OPEN": gcw.parseGripperState("O"),
    "STOP Gripper OPEN": gcw.parseGripperState("S"),
    "Gripper CLOSE": gcw.parseGripperState("C"),
    "STOP Gripper CLOSE": gcw.parseGripperState("S"),
    # Modify PWM
    "Increase PWM": gcw.parsePWM("U"),
    "STOP Increase PWM": gcw.parsePWM("S"),
    "Decrease PWM": gcw.parsePWM("D"),
    "STOP Decrease PWM": gcw.parsePWM("S"),
    # Random
    "Null":-1,
    "STOP Null":-1,
    "STOP gOF":-1,
    "STOP tm":-1,    
}

class GamepadControls:
    """
    A Class to convert the commands received from the front-end\n
    via the Gamepad into code word to be sent to the Rover
    """
    def __init__(self):
        pass


    def getCodeWord(self,command):
        try:
            return commandsCodeWord[command]
        except:
            print("Invalid Command in getCodeWord in GamepadControls.py")
