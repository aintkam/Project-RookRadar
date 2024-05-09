import cv2
from threading import Thread
from roboflow import Roboflow
import json
import numpy as np

# This class represents a webcam device.
class WebCam(object):
    def __init__(self, exitKey, source=0) -> None:
        # Stores the exit key used to terminate the webcam display.
        self.exitKey = exitKey
        # Stores the source index of the webcam device.
        self.source = source

        # Opens the webcam capture device 
        self.capture = cv2.VideoCapture(self.source)

        # Retrieves the width of the captured frame.
        self.width = int(self.capture.get(3))

        # Retrieves the height of the captured frame.
        self.height = int(self.capture.get(4))
    
    # Method to update the captured frame from the webcam.
    def updateSource(self):
        # Reads a frame from the webcam capture device.
        ret, frame = self.capture.read()
        return ret, frame
    
    # Method to continuously display the webcam feed until the exit key is pressed.
    def showSource(self):
        while True:

            # Updates the captured frame from the webcam.
            ret, frame = self.updateSource()
            if ret:

                # Displays the captured frame in a window named "Webcam".
                cv2.imshow("Webcam", frame)

                # Waits for a key press event. If the exit key is pressed, the loop breaks.
                if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                    break

        # Releases the webcam capture device.
        self.capture.release()
        # Closes all OpenCV windows.
        cv2.destroyAllWindows()

class DetectObject(WebCam):
    def __init__(self, givenObject, exitKey, source=0) -> None:
        self.givenObject = givenObject
        WebCam.__init__(self, exitKey, source)

    # This method extracts the corner coordinates from the predictions of a corner detection model.
    def getCorners(self, predictions):
        # Initialize an empty list to store the corner coordinates.
        corners = []
        # Check if predictions contain the 'predictions' key and if it is not empty.
        if 'predictions' in predictions and predictions['predictions']:
            # Iterate over each prediction in the 'predictions' list.
            for prediction in predictions['predictions']:
                # Extract the class label of the prediction.
                objectName = prediction['class']

                # Extracting (x, y) coordinates of the prediction box.
                x0 = prediction['x'] - prediction['width'] / 2
                x1 = prediction['x'] + prediction['width'] / 2
                y0 = prediction['y'] - prediction['height'] / 2
                y1 = prediction['y'] + prediction['height'] / 2

                # Determine the corner type and append the coordinates accordingly.
                if objectName == "Top-Left":

                    # Append coordinates of the top-left corner.
                    corners.append((int(x0), int(y0)))

                elif objectName == "Top-Right":
                    # Append coordinates of the top-right corner.
                    corners.append((int(x1), int(y0)))

                elif objectName == "Bottom-Left":
                    # Append coordinates of the bottom-left corner.
                    corners.append((int(x0), int(y1)))

                elif objectName == "Bottom-Right":

                    # Append coordinates of the bottom-right corner.
                    corners.append((int(x1), int(y1)))

                # Return the list of corner coordinates.
                return corners

            # If no valid corners are detected, return default coordinates.
            return [(0,0),(0,0),(0,0),(0,0)]
    
    # This method orders the corner points in a consistent manner to define a rectangle.
    def orderPoints(self, corners):
        # Convert the list of corners to a NumPy array for easier manipulation.
        corner_array = np.array(corners)

        # Initialize an array to store the ordered points.
        rect = np.zeros((4, 2), dtype=np.int32)

        # Calculate the sum and difference of x and y coordinates for each corner.
        s = corner_array.sum(axis=1)
        diff = np.diff(corner_array, axis=1)

        # Determine the order of points based on the sum and difference values.
        rect[0] = corner_array[np.argmin(s)]
        rect[2] = corner_array[np.argmax(s)]
        rect[1] = corner_array[np.argmin(diff)]
        rect[3] = corner_array[np.argmax(diff)]

        # Return the ordered points.
        return rect

    # This method computes the perspective transform matrix to map the chessboard corners to a rectangle.
    def perspectiveTransform(self, chessboard_corners, width, height):
        # Define the coordinates of the destination points (a rectangle)
        dst_pts  = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

        # Convert the coordinates of the chessboard corners to a numpy array
        src_pts = np.array(chessboard_corners, dtype=np.float32)

        # Compute the perspective transform matrix using OpenCV function.
        perspectiveMatrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # Return the computed perspective transform matrix.
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
        # Set the width and height of the captured frame
        width = 640
        height = 480

        # Continuous loop for capturing frames and detecting objects
        while True:
            # Capture frame from the webcam
            ret, source = self.updateSource()
            if ret:
                # Resize the captured frame to the specified width and height
                resizedFrame = cv2.resize(source, (width, height))

                # Predict chessboard corner locations
                cornerPredictions = cornerModel.predict(resizedFrame, confidence=15, overlap=30).json()

                # Get corner points and order them
                points = self.getCorners(cornerPredictions)
                orderedPoints = self.orderPoints(points)

                # Compute perspective transformation matrix
                transformMatrix = self.perspectiveTransform(orderedPoints, width, height)

                # Apply perspective transformation to the frame
                transformedImage = cv2.warpPerspective(resizedFrame, transformMatrix, (width, height))

                # Generate squares on the chessboard for visualization
                squares = self.getSquares(width, height)

                # Get board position for each square
                getSquarePosition = self.getBoardPosition(squares)

                # Predict positions of chess pieces
                piecePredictions = model.predict(transformedImage, confidence=32, overlap=30).json()
                piecePositions = self.getPiecePosition(piecePredictions)

                # Print squares and piece positions for debugging
                print(squares)
                print(piecePositions)

                # Draw squares on the transformed image
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

            # Display the transformed image with detected pieces
            cv2.imshow("ChessBoard", transformedImage)

            # Exit if the exit key is pressed
            if cv2.waitKey(1) & 0xFF == ord(self.exitKey):
                break

        # Release the webcam and close OpenCV windows
        self.capture.release()
        cv2.destroyAllWindows()

    # This method extracts the positions of predicted chess pieces.
    def getPiecePosition(self, piecePredictions):
        piecePositions = []

        # Check if there are predictions and iterate through them
        if 'predictions' in piecePredictions and piecePredictions['predictions']:
            for prediction in piecePredictions['predictions']:
                
                # Extract class name, x-position, and y-position of the piece
                objectName = prediction['class']
                xPos = prediction['x']
                yPos = prediction['y'] / 10

                # Append the piece name and its position to the list
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
