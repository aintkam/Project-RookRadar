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
    
    def getPoints(self, prediction):
        x0 = prediction['x'] - prediction['width'] / 2
        x1 = prediction['x'] + prediction['width'] / 2
        y0 = prediction['y'] - prediction['height'] / 2
        y1 = prediction['y'] + prediction['height'] / 2

        return x0, x1, y0, y1

    def getCorners(self, predictions):
        corners = []
        if 'predictions' in predictions and predictions['predictions']:
            for prediction in predictions['predictions']:

                objectName = prediction['class']

                # Extracting (x, y) coordinates
                x0 = prediction['x'] - prediction['width'] / 2
                x1 = prediction['x'] + prediction['width'] / 2
                y0 = prediction['y'] - prediction['height'] / 2
                y1 = prediction['y'] + prediction['height'] / 2

                if objectName == "Top-Left":
                    # Gets top left corner
                    corners.append((int(x0), int(y0)))
                
                elif objectName == "Top-Right":
                    # Gets top right corner
                    corners.append((int(x1), int(y0)))
                
                elif objectName == "Bottom-Left":
                    # Gets bottom left corner
                    corners.append((int(x0), int(y1)))
                
                elif objectName == "Bottom-Right":
                    # Gets bottom right corner
                    corners.append((int(x1), int(y1)))
        
            return corners
        
        return [(0,0),(0,0),(0,0),(0,0)]
    
    def orderPoints(self, corners):
        # Convert the list of corners to a NumPy array
        corner_array = np.array(corners)

        rect = np.zeros((4, 2), dtype=np.int32)

        s = corner_array.sum(axis=1)
        rect[0] = corner_array[np.argmin(s)]
        rect[2] = corner_array[np.argmax(s)]

        diff = np.diff(corner_array, axis=1)
        rect[1] = corner_array[np.argmin(diff)]
        rect[3] = corner_array[np.argmax(diff)]

        return rect

    def perspectiveTransform(self, chessboard_corners, width, height):
        # Define the coordinates of the destination points (a rectangle)
        dst_pts  = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)
    
        # Convert the coordinates of the chessboard corners to numpy array
        src_pts = np.array(chessboard_corners, dtype=np.float32)

         # Compute the perspective transform matrix
        perspectiveMatrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    
        return perspectiveMatrix
    
    def getSquares(self, width, height):
        # Calculate the spacing between horizontal and vertical lines
        horizontal_spacing = width // 8
        vertical_spacing = height // 8
    
        squares = []
    
        # Iterate through each row
        for i in range(8):
            # Calculate the y-coordinate of the current row
            y = i * vertical_spacing
    
            row_points = []
            
            # Iterate through each column
            for j in range(8):
                # Calculate the x-coordinate of the current column
                x = j * horizontal_spacing
    
                # Add the point to the list of row points
                row_points.append((x, y))
    
            # Add the list of row points to the list of squares
            squares.append(row_points)
    
        # No need to transpose the list of squares to iterate through columns
    
        return squares
    
    def getBoardPosition(self, squares):
        boardPositions = []
        for i, sublist in enumerate(squares):

            # Create a temporary list to store modified elements
            temp_list = []

            # Loop through each element in the sublist
            for j, element in enumerate(sublist):

                # Concatenate the row and column indices with the element value
                temp_list.append(f"{chr(97+j)}{i+1}")

            # Append the modified sublist to the output list
            boardPositions.append(temp_list)
        
        return boardPositions
    
    def detectChessBoard(self):
        width = 640
        height = 480

        while True:
            ret, source = self.updateSource()
            if ret:
                resizedFrame = cv2.resize(source, (width, height))
                cornerPredictions = cornerModel.predict(resizedFrame, confidence=15, overlap=30).json()

                points = self.getCorners(cornerPredictions)
                orderedPoints = self.orderPoints(points)

                transformMatrix = self.perspectiveTransform(orderedPoints, width, height)
                transformedImage = cv2.warpPerspective(resizedFrame, transformMatrix, (width, height))

                squares = self.getSquares(width, height)

                getSquarePosition = self.getBoardPosition(squares)

                piecePredictions = model.predict(transformedImage, confidence=32, overlap=30).json()
                piecePositions = self.getPiecePosition(piecePredictions)

                print(squares)
                print(piecePositions)

                # Draw squares on the resized frame for visualization
                for row in squares:
                    for square in row:
                        cv2.rectangle(transformedImage, square, (square[0] + width // 8, square[1] + height // 8), (255, 0, 0), 2)

                # Associate detected pieces with squares and draw them
                for piece in piecePositions:
                    for row_index, row in enumerate(squares):
                        for col_index, square in enumerate(row):
                            if square[0] <= piece[1][0] <= square[0] + width // 8 and square[1] <= piece[1][1] <= square[1] + height // 8:
                                cv2.putText(transformedImage, piece[0], square, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                break

            cv2.imshow("ChessBoard", transformedImage)

            if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                break

        self.capture.release()
        cv2.destroyAllWindows()

    def getPiecePosition(self, piecePredictions):
        piecePositions = []
        if 'predictions' in piecePredictions and piecePredictions['predictions']:
            for prediction in piecePredictions['predictions']:
                objectName = prediction['class']
                xPos = prediction['x']
                yPos = prediction['y'] / 10

                piecePositions.append([objectName, (xPos, yPos)])

        return piecePositions


        



if __name__ == '__main__':
    print("Generating Piece Model")
    rf = Roboflow(api_key="QClgG9OAXgWnJOxQuASr")

    project = rf.workspace("chess-piece").project("chess-pieces-pm2qa")
    version = project.version(1)
    dataset = version.download("yolov9")
    model = version.model
    print("Pieces Loaded")

    print("Corner Model")
    cornerProject = rf.workspace("chess-piece").project("chessboard-corners-isqda")
    cornerVersion = cornerProject.version(1)
    cornerDataset = cornerVersion.download("yolov9")
    cornerModel = cornerVersion.model
    print("Corners Loaded")

    detector = DetectObject("chess-piece", "q", 1)

    # Start a separate thread for object detection
    detect_thread = Thread(target=detector.detectChessBoard)
    detect_thread.start()
