import cv2
from threading import Thread
from roboflow import Roboflow

# Modify the WebCam class to use a different backend
class WebCam(object):
    def __init__(self, exitKey, source=0, backend=cv2.CAP_DSHOW) -> None:
        self.exitKey = exitKey
        self.source = source
        self.capture = cv2.VideoCapture(self.source, backend)
        self.width = int(self.capture.get(3))
        self.height = int(self.capture.get(4))
        cv2.namedWindow("Webcam", cv2.WND_PROP_FULLSCREEN)


    def updateSource(self):
        ret, frame = self.capture.read()
        return ret, frame

    def showSource(self):
        while True:
            ret, frame = self.updateSource()
            if ret:
                cv2.imshow("Webcam", frame)
                if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                    break
        self.capture.release()
        cv2.destroyAllWindows()

class DetectObject(WebCam):
    def __init__(self, givenObject, exitKey, source=0) -> None:
        self.givenObject = givenObject
        super().__init__(exitKey, source)

    def detect_and_display(self):
        while True:
            ret, frame = self.updateSource()
            if ret:
                # Resize frame to a smaller resolution
                resized_frame = cv2.resize(frame, (640, 480))  # Adjust dimensions as needed

                # Perform object detection on the resized frame
                predictions = model.predict(resized_frame, confidence=40, overlap=30).json()

                if predictions:
                    print(predictions)


                # Display the original frame with detections
                cv2.imshow("Webcam", frame)


            if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                break
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    rf = Roboflow(api_key="znjiO7f0O4s1TucZWJd6")
    project = rf.workspace("chess-piece").project("chess-full-ssuq4")
    version = project.version(1)
    dataset = version.download("yolov9")
    model = project.version(1).model

    webcam = WebCam("q", backend=cv2.CAP_DSHOW)  # or cv2.CAP_V4L2
    detector = DetectObject("chess-piece", "q")

    # Start a separate thread for object detection
    detect_thread = Thread(target=detector.detect_and_display)
    detect_thread.start()
    
    # Display webcam feed
    webcam.showSource()
