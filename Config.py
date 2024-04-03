import cv2

#Creates a class for turning on the webcam
class WebCam(object):

    #By default, the resolution is 720p (1280 x 720) and the source is 0 (default webcam)
    def __init__(self, exitKey, width=1280, height=720, source=0) -> None:
        self.width = width
        self.height = height
        self.source = source
        self.exitKey = exitKey

        #Sets the capture device
        self.capture = cv2.VideoCapture(self.source)

    def updateSource(self):
        ret, frame = self.capture.read()
        return ret, frame
    
    def showSource(self):
        while True:
            ret, frame = self.updateSource()
            cv2.imshow("Webcam", frame)
        
            #When the user presses "q", webcam turns off
            if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                break
        
        #After loop is done, releases capture and closes all windows
        self.capture.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    webcam = WebCam("q")
    webcam.showSource()



