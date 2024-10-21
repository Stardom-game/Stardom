import os, math, random, pymunk, pygame
from variables_functions import physics, variables

class Planet:
    def __init__(self, x, y, radius, image):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.body.position = (x, y)
        self.shape = None
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.friction = 2
        self.shape.color = (255, 0, 0, 100)
        variables.space.add(self.body, self.shape)

        self.rect = pygame.rect.Rect((0, 0), (radius, radius))
        self.rect.x, self.rect.y = x, y
        self.image = variables.images[image]
        self.radius = radius
    def update(self):
        pygame.draw.circle(variables.screen, variables.white, (self.rect.x, self.rect.y), self.radius)
        variables.screen.blit(pygame.transform.scale(self.image, (self.radius*2, self.radius*2)), (self.rect.x - self.radius, self.rect.y - self.radius))