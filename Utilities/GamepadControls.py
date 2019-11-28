from Utilities.GenerateCodeWord import GenerateCodeword
gcw = GenerateCodeword()
commandsCodeWord = {
    "Forward": gcw.parseBase("F"),
    "STOP Forward": gcw.parseBase("S"),
    "Backward": gcw.parseBase("B"),
    "STOP Backward": gcw.parseBase("S"),
    "Left": gcw.parseBase("L"),
    "STOP Left": gcw.parseBase("S"),
    "Right": gcw.parseBase("R"),
    "STOP Right": gcw.parseBase("S"),
    "0": gcw.parseCamera(1),
    "1": gcw.parseCamera(1),
    "2": gcw.parseCamera(2),
    "3": gcw.parseCamera(3),
    "4": gcw.parseCamera(4),
    "ARM Base Left": gcw.parseArm("L"),
    "STOP ARM Base Left": gcw.parseArm("S"),
    "ARM Base Right": gcw.parseArm("R"),
    "STOP ARM Base Right": gcw.parseArm("S"),
    "command": gcw.parseActuator1("E"),
    "STOP command": gcw.parseActuator1("S"),
    "command": gcw.parseActuator1("R"),
    "STOP command": gcw.parseActuator1("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    "command": gcw.parseBase("F"),
    "STOP command": gcw.parseBase("S"),
    
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
