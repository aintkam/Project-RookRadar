import cv2
from threading import Thread
from roboflow import Roboflow
import json
import numpy as np

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
        WebCam.__init__(self, exitKey, source)

    def showSource(self):
        while True:
            ret, frame = self.updateSource()
            # Convert to grayscale
            if ret:
                resized_frame = cv2.resize(frame, (640, 480)) 

                predictions = model.predict(resized_frame, confidence=33, overlap=30).json()
                
                if 'predictions' in predictions and predictions['predictions']:
                    for prediction in predictions['predictions']:
                        print(prediction)
                        # Extracting (x, y) coordinates
                        x0 = prediction['x'] - prediction['width'] / 2
                        x1 = prediction['x'] + prediction['width'] / 2
                        y0 = prediction['y'] - prediction['height'] /2
                        y1 = prediction['y'] + prediction['height'] /2

                        start_point = (int(x0), int(y0))
                        end_point = (int(x1), int(y1))

                        cv2.rectangle(resized_frame, start_point, end_point, color=(0,0,0), thickness=1)

                        cv2.putText(resized_frame, prediction['class'], 
                                    (int(x0), int(y0) - 10), 
                                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                                    fontScale = 0.6,
                                    color = (255, 255, 255),
                                    thickness=2)
                        
                # Display the original frame with detections
                cv2.imshow("Detector", resized_frame)


            if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                break
        self.capture.release()
        cv2.destroyAllWindows()

    def birdsEyeView(self):
        while True:
            # Gets the webcam
            ret, frame = self.updateSource()
            if ret:

                # Define the ROI (assuming the chessboard is in the central region of the image)
                roi = np.zeros_like(frame[:, :, 0])
                roi[30:50, 30:50] = 255  # Adjust the coordinates as needed
                # Makes the source in gayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Converts to a threshold (filters the squares to turn them white or black)
                adaptiveThreshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 10)
                cv2.imshow("Adaptive Thresh", adaptiveThreshold)

                edges = cv2.Canny(gray, 100, 300)
                cv2.imshow("Edges", edges)

                
                lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=100)

                # Draw lines on the original image
                if lines is not None:
                    for line in lines:
                        rho, theta = line[0]
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a * rho
                        y0 = b * rho
                        x1 = int(x0 + 1000 * (-b))
                        y1 = int(y0 + 1000 * (a))
                        x2 = int(x0 - 1000 * (-b))
                        y2 = int(y0 - 1000 * (a))
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                # Display the results
                cv2.imshow('Hough Lines', frame)
                


            if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                break

        self.capture.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    rf = Roboflow(api_key="znjiO7f0O4s1TucZWJd6")
    project = rf.workspace("chess-piece").project("chess-pieces-pm2qa")
    version = project.version(1)
    dataset = version.download("yolov9")
    model = project.version(1).model
    print("Loaded")

    webcam = WebCam("q",1, backend=cv2.CAP_DSHOW)  # or cv2.CAP_V4L2
    detector = DetectObject("chess-piece", "q", 1)

    # Start a separate thread for object detection
    detect_thread = Thread(target=detector.birdsEyeView())
    detect_thread.start()
    
    # Display webcam feed
    #detector.showSource()
