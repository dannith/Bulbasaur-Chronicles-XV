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
        self.setAnimations()

    def setAnimations(self):
        self.front = [
            self.spriteSheet.subsurface(4, 0, 21, 22),
            self.spriteSheet.subsurface(4, 26, 21, 22),
            self.spriteSheet.subsurface(4, 50, 21, 22),
            self.spriteSheet.subsurface(4, 76, 21, 22)
        ]

b = Bulbasaur("bulby")



counter = 0
counterus = 0
while running:
    event = pygame.event.poll()
    clock.tick(60)
    screen.fill((0, 100, 0))
    screen.blit(b.front[counter], (10, 10))
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