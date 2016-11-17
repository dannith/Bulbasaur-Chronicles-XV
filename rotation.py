import pygame
pygame.init()
running = True
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

class Bulbasaur(pygame.sprite.Sprite):

    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.rotation = 180
        self.spriteSheet = pygame.image.load("grafix/bulba-sprite.png").convert_alpha()
        self.frames = {
            "forward" : {
                "front": [
                    self.spriteSheet.subsurface(4, 0, 21, 22),
                    self.spriteSheet.subsurface(4, 26, 21, 22),
                    self.spriteSheet.subsurface(4, 50, 21, 22),
                    self.spriteSheet.subsurface(4, 76, 21, 22)
                ],
                "sideFront": [
                    self.spriteSheet.subsurface(42, 0, 26, 22),
                    self.spriteSheet.subsurface(42, 26, 26, 22),
                    self.spriteSheet.subsurface(42, 50, 26, 22),
                    self.spriteSheet.subsurface(42, 76, 26, 22)
                ],
                "side": [
                    self.spriteSheet.subsurface(80, 0, 24, 22),
                    self.spriteSheet.subsurface(80, 26, 24, 22),
                    self.spriteSheet.subsurface(80, 50, 24, 22),
                    self.spriteSheet.subsurface(80, 76, 24, 22)
                ],
                "sideBack": [
                    self.spriteSheet.subsurface(120, 0, 26, 22),
                    self.spriteSheet.subsurface(120, 26, 26, 22),
                    self.spriteSheet.subsurface(120, 50, 26, 22),
                    self.spriteSheet.subsurface(120, 76, 26, 22)
                ],
                "back": [
                    self.spriteSheet.subsurface(159, 0, 17, 22),
                    self.spriteSheet.subsurface(159, 26, 17, 22),
                    self.spriteSheet.subsurface(159, 50, 17, 22),
                    self.spriteSheet.subsurface(159, 76, 17, 22)
                ]
            },
            "backward" : {
                "front": [
                    self.spriteSheet.subsurface(4, 125, 21, 22),
                    self.spriteSheet.subsurface(4, 150, 21, 22)
                ],
                "sideFront": [
                    self.spriteSheet.subsurface(42, 125, 26, 22),
                    self.spriteSheet.subsurface(42, 150, 26, 22)
                ],
                "side": [
                    self.spriteSheet.subsurface(80, 125, 24, 22),
                    self.spriteSheet.subsurface(80, 150, 24, 22)
                ],
                "sideBack": [
                    self.spriteSheet.subsurface(120, 125, 26, 22),
                    self.spriteSheet.subsurface(120, 150, 26, 22)
                ],
                "back": [
                    self.spriteSheet.subsurface(159, 125, 17, 22),
                    self.spriteSheet.subsurface(159, 150, 17, 22)
                ]
            }
        }
        self.getSprite()

    def rotate(self, deg):
        self.rotation += deg
        if self.rotation > 360:
            self.rotation = self.rotation - 360
        self.getSprite()

    def getSprite(self):
        if self.rotation > 338 or self.rotation <= 23: self.sprite = self.frames["forward"]["back"]
        elif self.rotation > 23 and self.rotation <= 68: self.sprite = pygame.transform.flip(self.frames["forward"]["sideBack"], True, False)
        elif self.rotation > 68 and self.rotation <= 113: self.sprite = pygame.transform.flip(self.frames["forward"]["side"], True, False)
        elif self.rotation > 113 and self.rotation <= 158: self.sprite = pygame.transform.flip(self.frames["forward"]["sideFront"], True, False)
        elif self.rotation > 158 and self.rotation <= 203: self.sprite = self.frames["forward"]["front"]
        elif self.rotation > 203 and self.rotation <= 248: self.sprite = self.frames["forward"]["sideFront"]
        elif self.rotation > 248 and self.rotation <= 293: self.sprite = self.frames["forward"]["side"]
        elif self.rotation > 293 and self.rotation <= 338: self.sprite = self.frames["forward"]["sideBack"]



b = Bulbasaur("bulby")


counter = 0
counterus = 0
loc = -22

print (b.rotation)
b.rotate(190)
print(b.rotation)
while running:
    event = pygame.event.poll()
    clock.tick(60)
    screen.fill((0, 100, 0))
    screen.blit(b.frames["backward"]["back"][counter], (10, loc))
    loc += 0.5
    if loc == 600:
        loc = -22
    counterus += 1
    if counterus == 10:
        counter += 1
        counterus = 0
        if counter == 2:
            counter = 0
    if counter == 4:
        counter = 0

    if event.type == pygame.QUIT:
        running = False
        pygame.QUIT
    pygame.display.update()