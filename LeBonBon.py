import cv2
from pygame import mixer

mixer.init()

file_name = "LeBonBon/TotallyRealVideo.mp4"
window_name = "Press Q to Exit"
interframe_wait_ms = 30

cap = cv2.VideoCapture(file_name)

if __name__ == "__main__":

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
        
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    mixer.music.load("LeBonBon/TotallyRealAudio.mp3")
    mixer.music.play()

    while (True):
        ret, frame = cap.read()
        if not ret:
            print("Reached end of video, exiting.")
            break

        cv2.imshow(window_name, frame)
        if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
            print("Exit requested.")
            break

    cap.release()
    cv2.destroyAllWindows()