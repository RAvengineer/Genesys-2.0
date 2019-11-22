from importlib import reload
import signal
from time import sleep

def handler(signum, frame):
    """Handler for the signal"""
    raise Exception("Time-out!")


class GamepadControls:
    """
    A Class to get Inputs using a Gamepad
    """
    def __init__(self):
        self.armMode = False
        self.gamepadActive = False
    
    
    def getGamepad(self):
        import inputs
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(2)
        try:
            event = inputs.get_gamepad()[0]
            signal.alarm(0)
            # This 'if' avoids STOP being executed thrice instead of once
            if(event.code=="SYN_REPORT"):
                return ('NULL',)
            return (event.ev_type, event.code, event.state)
        except Exception as e:
            if(str(e).find("No gamepad found.")!=-1 or str(e).find("[Errno 19] No such device")!=-1):
                signal.alarm(0)
                reload(inputs)
                sleep(2)
                return ('No Gamepad',)
            elif(str(e)=="Time-out!"):
                signal.alarm(0)
                return ('NULL',)
    

    def parseControls(self):
        """
        Parse the commands received from the gamepad and map them to 
        fit the users need.
        Returns a Tuple (value, status) => value(int), status(str)
        """
        command = self.getGamepad()
        if(command[0]=="No Gamepad"):
            self.armMode = False
            self.gamepadActive = False
            return ("Gamepad Disconnected",)
        elif(command[0]=="NULL"):
            return command
        else:
            # BTN_START 1 => START Button
            if(command[1]=="BTN_START" and command[2]==1):
                self.armMode = False
                self.gamepadActive = not self.gamepadActive
                return ("Gamepad Activity Toggled",)
            elif(self.gamepadActive==False):
                return ("Gamepad Inactive",)
            # BTN_SELECT 1 => Back Button
            elif(command[1]=="BTN_SELECT" and command[2]==1):
                self.armMode = not self.armMode
                return ("Mode Changed",)
            elif(self.armMode==True): # If in Arm Mode
                return(self.parseArmCommand(command))
            else:             # If in Motor wheels mode
                return(self.parseWheelCommand(command))
        """ 
        NOTE: BTN_START 0 and BTN_START 0 will cause the next elif states to be
        executed, which will result in STOP being executed
        """
    
    
    def parseArmCommand(self,command):
        """
        Parse commands specific to Arm controls.
        Parameter: command(Tuple)
        Returns a Tuple (value, status) => value(int), status(str)
        """
        e_code  = command[1] # e_code = event code (string)
        e_state = command[2] # e_state = event state (int)
        val = -1
        
        # Stop => e_state = 0
        if(e_state == 0):
            val = 27
            status = "STOP"
        
        # Actuator 1 high => ABS_HAT0Y -1
        elif (e_code=='ABS_HAT0Y' and e_state==-1):
            val = 51
            status = "Actuator 1 HIGH"
        # Actuator 1 Low => ABS_HAT0Y 1
        elif (e_code=='ABS_HAT0Y' and e_state==1):
            val = 52
            status = "Actuator 1 LOW"
        # Actuator 2 High => BTN_WEST 1
        elif e_code=='BTN_WEST':
            val = 53
            status = "Actuator 2 HIGH"
        # Actuator 2 Low => BTN_SOUTH 1
        elif e_code=='BTN_SOUTH':
            val = 54
            status = "Actuator 2 LOW"
        # Actuator 3 High => BTN_NORTH 1
        elif e_code=='BTN_NORTH':
            val = 55
            status = "Actuator 3 HIGH"
        # Actuator 3 Low => BTN_EAST 1
        elif e_code=='BTN_EAST':
            val = 56
            status = "Actuator 3 LOW"
        # Base Clock => ABS_HAT0X 1
        elif (e_code=='ABS_HAT0X' and e_state==1):
            val = 49
            status = "Base Clockwise"
        # Base Anticlock => ABS_HAT0X -1
        elif (e_code=='ABS_HAT0X' and e_state==-1):
            val = 50
            status = "Base Anti-clockwise"

        # Gripper motor clock - Gripper Close => ABS_RZ 255
        elif e_code=='ABS_RZ':
            val = 84
            status = "Gripper motor Clockwise"
        # Gripper motor anticlock - Gripper Open => ABS_Z 255
        elif e_code=='ABS_Z':
            val = 71
            status = "Gripper motor Anti-clockwise"
        # Gripper rotate clock => BTN_TL 1
        elif e_code=='BTN_TL':
            val = 73
            status = "Gripper rotate Clockwise"
        # Gripper rotate anticlock => BTN_TR 1
        elif e_code=='BTN_TR':
            val = 75
            status = "Gripper rotate Anti-clockwise"
        
        # None of the Above
        else:
            return ('NULL',)
        
        return (status, val)


    def parseWheelCommand(self,command):
        """
        Parse commands specific to Motor Wheel controls.
        Parameter: command(Tuple)
        Returns a Tuple (value, status) => value(int), status(str)
        """
        e_code  = command[1] # e_code = event code (string)
        e_state = command[2] # e_state = event state (int)
        val = -1

        # Stop => e_state = 0
        if(e_state == 0):
            val = 27
            status = "STOP"
        
        # Forward => BTN_WEST 1
        elif e_code=='BTN_WEST':
            val = 53
            status = "Forward"
        # Backward => BTN_SOUTH 1
        elif e_code=='BTN_SOUTH':
            val = 54
            status = "Backward"
        # Left => BTN_NORTH 1
        elif e_code=='BTN_NORTH':
            val = 55
            status = "Left"
        # Right => BTN_EAST 1
        elif e_code=='BTN_EAST':
            val = 56
            status = "Right"
        
        # TODO: The values (val) in the if structure are to be configured, discuss with
        #       Shreyansh and Saswat

        # None of the Above
        else:
            return ('NULL',)
        
        return (status, val)

"""
Reference: 
* https://stackoverflow.com/questions/492519/timeout-on-a-function-call
* https://justus.science/blog/2015/04/19/sys.modules-is-dangerous.html
"""

