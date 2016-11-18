import pygame, math
pygame.init()
running = True
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

class Bulbasaur(pygame.sprite.Sprite):

    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.rotation = 180
        self.locX = 100
        self.locY = 100
        self.loc = (self.locX, self.locY)
        self.x = 0
        self.y = 0
        self.frame = 0
        self.animInterval = 0
        self.animIntervalMax = 10
        self.moving = 1
        self.spriteSheet = pygame.image.load("grafix/bulba-sprite.png").convert_alpha()
        self.frames = {
            "forward" : {
                "front": [
                    self.spriteSheet.subsurface(0, 0, 26, 22),
                    self.spriteSheet.subsurface(0, 26, 26, 22),
                    self.spriteSheet.subsurface(0, 50, 26, 22),
                    self.spriteSheet.subsurface(0, 76, 26, 22)
                ],
                "sideFront": [
                    self.spriteSheet.subsurface(41, 0, 26, 22),
                    self.spriteSheet.subsurface(41, 26, 26, 22),
                    self.spriteSheet.subsurface(41, 50, 26, 22),
                    self.spriteSheet.subsurface(41, 76, 26, 22)
                ],
                "side": [
                    self.spriteSheet.subsurface(80, 0, 26, 22),
                    self.spriteSheet.subsurface(80, 26, 26, 22),
                    self.spriteSheet.subsurface(80, 50, 26, 22),
                    self.spriteSheet.subsurface(80, 76, 26, 22)
                ],
                "sideBack": [
                    self.spriteSheet.subsurface(117, 0, 26, 22),
                    self.spriteSheet.subsurface(117, 26, 26, 22),
                    self.spriteSheet.subsurface(117, 50, 26, 22),
                    self.spriteSheet.subsurface(117, 76, 26, 22)
                ],
                "back": [
                    self.spriteSheet.subsurface(153, 0, 26, 22),
                    self.spriteSheet.subsurface(153, 26, 26, 22),
                    self.spriteSheet.subsurface(153, 50, 26, 22),
                    self.spriteSheet.subsurface(153, 76, 26, 22)
                ]
            },
            "backward" : {
                "front": [
                    self.spriteSheet.subsurface(0, 125, 26, 22),
                    self.spriteSheet.subsurface(0, 150, 26, 22)
                ],
                "sideFront": [
                    self.spriteSheet.subsurface(41, 125, 26, 22),
                    self.spriteSheet.subsurface(41, 150, 26, 22)
                ],
                "side": [
                    self.spriteSheet.subsurface(79, 125, 26, 22),
                    self.spriteSheet.subsurface(79, 150, 26, 22)
                ],
                "sideBack": [
                    self.spriteSheet.subsurface(117, 125, 26, 22),
                    self.spriteSheet.subsurface(117, 150, 26, 22)
                ],
                "back": [
                    self.spriteSheet.subsurface(153, 125, 26, 22),
                    self.spriteSheet.subsurface(153, 150, 26, 22)
                ]
            }
        }
        self.render = self.getSprite()[self.frame]

    def move(self):
        # Key handling
        key = pygame.key.get_pressed()
        self.up = key[pygame.K_UP]
        self.down = key[pygame.K_DOWN]
        self.left = key[pygame.K_LEFT]
        self.right = key[pygame.K_RIGHT]

        if key[pygame.K_UP]:
            self.getXY()
            self.moving = True
        elif key[pygame.K_DOWN]:
            pass
        if key[pygame.K_LEFT]:
            print(self.rotation)
            self.rotate(-5)
        elif key[pygame.K_RIGHT]:
            self.rotate(5)

    def getXY(self):
        angle = math.radians(self.rotation)
        self.x = 1 * math.cos(angle)
        self.y = 1 * math.sin(angle)

        self.locX += self.x
        self.locY += self.y
        self.loc = (self.locX, self.locY)

    def rotate(self, deg):
        self.rotation += deg
        if self.rotation > 360:
            self.rotation = self.rotation - 360
        elif self.rotation < 0:
            self.rotation = 360 - self.rotation
        self.getSprite()

    def animate(self):
        self.render = self.image[self.frame]
        if self.rotation < 90 or self.rotation > 270:
            self.render = pygame.transform.flip(self.render, True, False)


        if self.moving == 1:
            self.animInterval += 1
            if self.animInterval == self.animIntervalMax:
                self.animInterval = 0
                self.frame += 1
                if self.frame == 4:
                    self.frame = 0
                    self.moving = 0
        elif self.moving == -1:
            if self.frame == 2:
                self.frame = 0


    def getSprite(self):
        if self.rotation > 338 or self.rotation <= 23: self.image = self.frames["forward"]["side"]
        elif self.rotation > 23 and self.rotation <= 68: self.image = self.frames["forward"]["sideFront"]
        elif self.rotation > 68 and self.rotation <= 113: self.image = self.frames["forward"]["front"]
        elif self.rotation > 113 and self.rotation <= 158: self.image = self.frames["forward"]["sideFront"]
        elif self.rotation > 158 and self.rotation <= 203: self.image = self.frames["forward"]["side"]
        elif self.rotation > 203 and self.rotation <= 248: self.image = self.frames["forward"]["sideBack"]
        elif self.rotation > 248 and self.rotation <= 293: self.image = self.frames["forward"]["back"]
        elif self.rotation > 293 and self.rotation <= 338: self.image = self.frames["forward"]["sideBack"]
        return self.image



b = Bulbasaur("bulby")


counter = 0
counterus = 0
loc = -22

while running:
    event = pygame.event.poll()
    clock.tick(60)
    screen.fill((0, 100, 0))
    screen.blit(b.render, b.loc)
    b.animate()
    b.move()
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