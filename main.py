import pygame as py
py.init()

# class for mainApplication passed the object from game settings
class mainApplication :
    def __init__(self, config ):
        self.screen = py.display.set_mode( config.size )

# class for setting config
class gameStateConfig :
    def __init__(self, setting_file):
        # self.cfg = setting_file -- eventually add json setting data e.g screen size ect.
        self.width = 700
        self.half_w = int( 0.5*self.width )
        self.height = 500
        self.half_h = int( 0.5*self.height )
        self.size = (self.width,self.height)

# instatiate
config = gameStateConfig("settings.json")
mainApp = mainApplication(config)
clock = py.time.Clock()

# Just some colours
BLACK = (255,255,255)
RED = (255, 0, 0)

# Mainloop
done = False
while not done:
    for event in py.event.get():
        if event.type == py.QUIT:
            done = True

    # write hello world to the screen
    font = py.font.SysFont('Calibri', 15, True, False)
    text = font.render("Hello World", True, RED)
    # this blits the top right of text to slightly up and to the right
    mainApp.screen.blit(text, [config.half_w- 50, config.half_h - 50])
 
    # lock frame rate and update the display
    py.display.flip()
    clock.tick(60)
 
# Close the window and quit.
py.quit()