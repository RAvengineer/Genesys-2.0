from Utilities.GenerateCodeWord import GenerateCodeword
gcw = GenerateCodeword()
commandsCodeWord = {
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


    def getCodeWord(command):
        try:
            return commandsCodeWord(command)
        except:
            print("Invalid Command in getCodeWord in GamepadControls.py")
