import serial

class xbeeCom:
    def __init__(self,port="/dev/xbee"):
        '''
        Constructor for XbeeCommunications Class.
        PORT : serial_Port to which xbee is connected i.e. /dev/ttyUSB*.
        NOTE : DO NOT CHANGE THE BAUDRATE. XBEE'S BAUDRATE IS FIXED 
               AT 9600. 
        '''
        self.PORT = port
        self.BAUD = 9600
        self.ser = serial.Serial(port=self.PORT,baudrate=self.BAUD)
    
    def __del__(self):
        """Destructor for the XbeeCommunications Class."""
        self.ser.close()

    def receive_data(self,return_length):
        '''
        return_length : Expected length of the return message or BUFFER_SIZE as 
        you may know.
        '''
        data = self.ser.read(return_length)
        data = data.decode()
        return data

    def send_data(self,command):
        '''
        command : command to be sent to rover ; type of "command" can be str or int.
        NOTE : This function will send the command and close.
        '''
        self.ser.write(command.to_bytes(3,byteorder='little',signed=False))
        # sleep(1)