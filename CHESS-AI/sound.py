import pygame

class Sound:

    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)


if __name__ == "__main__":
    pygame.init()
    sound = Sound("CHESS-AI/assets/sounds/move.wav")
    sound.play()
    sound2 = Sound("CHESS-AI/assets/sounds/capture.wav")
    sound2.play()\
    
    for i in range(1000):
        sound.play()
        sound2.play()