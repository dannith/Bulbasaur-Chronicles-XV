import pygame
pygame.init()
running = True
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

class Bulbasaur(pygame.sprite.Sprite):

    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.spriteSheet = pygame.image.load("grafix/bulba-sprite.png").convert_alpha()
        self.frames = {
            "front" : [
                self.spriteSheet.subsurface(4, 0, 21, 22),
                self.spriteSheet.subsurface(4, 26, 21, 22),
                self.spriteSheet.subsurface(4, 50, 21, 22),
                self.spriteSheet.subsurface(4, 76, 21, 22)
            ],
            "sideFront" : [
                self.spriteSheet.subsurface(42, 0, 26, 22),
                self.spriteSheet.subsurface(42, 26, 26, 22),
                self.spriteSheet.subsurface(42, 50, 26, 22),
                self.spriteSheet.subsurface(42, 76, 26, 22)
            ],
            "side" : [
                self.spriteSheet.subsurface(80, 0, 24, 22),
                self.spriteSheet.subsurface(80, 26, 24, 22),
                self.spriteSheet.subsurface(80, 50, 24, 22),
                self.spriteSheet.subsurface(80, 76, 24, 22)
            ],
            "sideBack" : [
                self.spriteSheet.subsurface(120, 0, 26, 22),
                self.spriteSheet.subsurface(120, 26, 26, 22),
                self.spriteSheet.subsurface(120, 50, 26, 22),
                self.spriteSheet.subsurface(120, 76, 26, 22)
            ],
            "back" : [
                self.spriteSheet.subsurface(159, 0, 17, 22),
                self.spriteSheet.subsurface(159, 26, 17, 22),
                self.spriteSheet.subsurface(159, 50, 17, 22),
                self.spriteSheet.subsurface(159, 76, 17, 22)
            ]
        }


b = Bulbasaur("bulby")


counter = 0
counterus = 0
loc = -22
while running:
    event = pygame.event.poll()
    clock.tick(60)
    screen.fill((0, 100, 0))
    screen.blit(b.frames["back"][counter], (10, loc))
    loc += 1
    if loc == 600:
        loc = -22
    counterus += 1
    if counterus == 10:
        counter += 1
        counterus = 0
        if counter == 4:
            counter = 0
    if counter == 4:
        counter = 0

    if event.type == pygame.QUIT:
        running = False
        pygame.QUIT
    pygame.display.update()