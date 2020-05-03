import pygame
import ctypes
import brain
import sys

def game():
    global event
    pygame.init()

    window = (600, 600)
    screen = pygame.display.set_mode(window)
    pygame.display.set_caption("number guesser")
    clock = pygame.time.Clock()

    # defining colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (130, 130, 130)

    screen.fill(black)
    background = pygame.Surface((470, 470))
    background.fill(white)
    screen.blit(background, (65, 30))
    pygame.display.flip()

    def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    # buttons
    class button():
        def __init__(self, color, x, y, width, height, text=''):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self, win):
            # Call this method to draw the button on the screen
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

            if self.text != '':
                font = pygame.font.SysFont('comicsansms', 28)
                text = font.render(self.text, 1, (0, 0, 0))
                win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        def isOver(self, pos):
            # Pos is the mouse position or a tuple of (x,y) coordinates
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True

            return False

    # defining our buttons
    clearButton = button(grey, 50, 525, 100, 50, text='Clear')
    predButton = button(grey, 450, 525, 100, 50, text='Guess')

    # defining drawing area
    rect = pygame.Rect(65, 30, 470, 470)

    game_loop = True
    neural = False

    while game_loop:
        # draw buttons onto screen with .draw function
        clearButton.draw(screen)
        predButton.draw(screen)
        while not neural:
            robot = brain.Robot()
            neural = True

        try:
            # pygame.mouse.set_visible(False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False
                    pygame.quit()
                    sys.exit(0)

            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed() == (1, 0, 0):
                pygame.draw.rect(screen, black, (pos[0], pos[1], 30, 30))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if clearButton.isOver(pos):
                    background.fill(white)
                    screen.blit(background, (65, 30))
                    pygame.display.update()
                    # rect = pygame.draw.rect(screen,white,(65, 25, 470, 470))
                elif predButton.isOver(pos):
                    # color_image = pygame.surfarray.array3d(background)
                    sub = screen.subsurface(rect)
                    pygame.image.save(sub, "screenshot.jpg")
                    robot.process_data()
                    robot.predict()
                    Mbox('Result', f'The number is {robot.reveal()}',0)


            pygame.display.update()
            clock.tick(1000)
        except Exception as e:
            print(e)
            pygame.quit()

    pygame.quit()

game()