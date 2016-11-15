import pygame

class Bulbasaur(pygame.sprite.Sprite):

    def __init__(self, name, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface(image);
        self.rect = self.image.get_rect()