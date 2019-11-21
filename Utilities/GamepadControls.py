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
    
    
    def getGamepad(self):
        import inputs
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(2)
        try:
            event = inputs.get_gamepad()[0]
            signal.alarm(0)
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



"""
Reference: 
* https://stackoverflow.com/questions/492519/timeout-on-a-function-call
* https://justus.science/blog/2015/04/19/sys.modules-is-dangerous.html
"""

