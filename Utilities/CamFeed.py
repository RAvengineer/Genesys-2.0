import cv2

class CamFeed:
    def __init__(self):
        """
        Constructor for CamFeed Class.
        VideoCapture object of cv2 is created here.
        """
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        """Destructor for CamFeed Class"""
        self.video.release()
    
    def get_frame(self):
        """Reads the frames from the Camera and returns them jped in bytes."""
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        # image_np = cv2.resize(image, (528,396))
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def gen(self):
        """An infinite loop function to be passed in the Response section for the Feed"""
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
