class StationRoverSocket:
    """
    A class that makes the process of sending and receiving the messages to and from
    the Rover easier.
    NOTE: receive() should be called once before calling send(msg), bcoz send uses
    address of the receiver which is initialized first in receive().
    """
    def __init__(self,port=9750,ip=''):
        """
        Constructor for the StationRoverSocket Class.\n
        Parameters: port(int)=9750 and ip(str)=''
        """
        import socket     # Wifi Xbee is using raw feed, hence a raw socket protocol
        self.PORT = port
        self.IP = ip
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        # self.sock.bind((self.IP,self.PORT))
        self.sock.connect((self.IP,self.PORT))
        self.addrAvailable = False


    def __del__(self):
        """Destructor for the StationRoverSocket Class."""
        self.addrAvailable = False
        self.sock.close()
    

    def receiveEncoded(self,BUFFER_SIZE):
        """
        Calls sock.recvfrom(BUFFER_SIZE) and saves the sender's address.\n
        Parameters: BUFFER_SIZE(int)\n
        Returns: msg(byte)
        """
        msg, addr = self.sock.recvfrom(BUFFER_SIZE)
        self.xbeeAddr = addr
        self.addrAvailable = True
        return msg


    def receive(self,BUFFER_SIZE=1024):
        """
        Official Receive Function for the class. It will receive from all the senders.\n
        Parameters: BUFFER_SIZE(int) Default=1024\n
        Returns: Received message in string
        """
        return self.receiveEncoded(BUFFER_SIZE).decode()


    def send(self,msg):
        """Calls sock.sendto(msg.encode(),self.xbeeAddr).\n
        Parameters: message=>msg(str)
        """
        self.sock.sendto(msg.encode(),self.xbeeAddr)
    

    def testSend(self, msg):
        """
        Test Send made for testing the rover for last Minute Jugaad
        Made for base as Client
        """
        self.sock.sendto(msg.to_bytes(3,'little'),(self.IP,self.PORT))
    
