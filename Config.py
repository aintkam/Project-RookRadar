import cv2

#Creates a class for turning on the webcam
class WebCam(object):

    #By default, the resolution is 720p (1280 x 720) and the source is 0 (default webcam)
    def __init__(self, exitKey, source=0) -> None:
        self.exitKey = exitKey
        self.source = source
        
        #Sets the capture device
        self.capture = cv2.VideoCapture(self.source)
        self.width = int(self.capture.get(3))
        self.height = int(self.capture.get(4))

        #Allows the webcam to fullscreen and fill the window
        cv2.namedWindow("Webcam", cv2.WND_PROP_FULLSCREEN)

    #Returns if the camera is on and the curernt frame
    def updateSource(self):
        ret, frame = self.capture.read()
        return ret, frame
    
    def showSource(self):
        while True:
            ret, frame = self.updateSource()
            if ret:

                cv2.imshow("Webcam", frame)
            
                #When the user presses the exitKey, webcam turns off
                if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                    break
        
        #After loop is done, releases capture and closes all windows
        self.capture.release()
        cv2.destroyAllWindows()

#Creates a class for detectig a given object using the webcam
class DetectObject(WebCam):
    def __init__(self, givenObject, exitKey, source=0) -> None:
        self.givenObject = givenObject
        super().__init__(exitKey, source)

if __name__ == '__main__':
    webcam = WebCam("q")
    webcam.showSource()