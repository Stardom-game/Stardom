import pygame, os
import pygame.freetype
from variables_functions import variables

pygame.freetype.init()
class Button:
    def __init__(self, screen, x, y, width, height,
                 color, textcolor, font, fontsize, roundedness, text,
                 image, name, assigned_function, hide_fill = False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5):
        pygame.font.init()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonrect = pygame.rect.Rect((x, y), (width, height))
        # self.buttonrect.center = (x,y)
        self.font = pygame.freetype.SysFont(font, fontsize)
        self.textrect = pygame.rect.Rect((0, 0), (width, height / 2))
        self.textcolor = textcolor
        self.textpos = pygame.rect.Rect((0, 0), (1, 1))
        self.textstring = text
        self.roundedness = roundedness
        self.color = color
        root_dir = (os.path.abspath(os.path.join(os.getcwd())))
        self.image = pygame.image.load(os.path.join(root_dir, "images", "blank.png"))
        self.image = image
        self.imagerect = self.image.get_rect()
        self.outline = outline
        self.outlinecolor = outlinecolor
        self.outlinethickness = outlinethickness
        self.name = name
        self.assigned_function = assigned_function
        self.just_pressed = False
        self.hide_fill = hide_fill

        if self.textstring != "":
            self.font = pygame.font.SysFont(font, fontsize)
            self.text = self.font.render(self.textstring, 1, self.textcolor)
            screen.blit(self.text, (self.x + (self.width / 2 - self.text.get_width() / 2),
                                    self.y + (self.height / 2 - self.text.get_height() / 2)))

        if not self.image == None:
            screen.blit(self.image, (self.x + (self.width / 2 - self.imagerect.width / 2),
                                     self.y + (self.height / 2 - self.imagerect.height / 2)))

    def update(self, screen):
        if not self.hide_fill:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, self.roundedness)
            if self.outline:
                pygame.draw.rect(screen, self.outlinecolor, (self.x, self.y, self.width, self.height),
                                 self.outlinethickness, self.roundedness)

        if self.textstring != "":
            screen.blit(self.text, (self.x + (self.width / 2 - self.text.get_width() / 2),
                                    self.y + (self.height / 2 - self.text.get_height() / 2)))
        if not self.image == None:
            screen.blit(self.image, (self.x + (self.width / 2 - self.imagerect.width / 2),
                                     self.y + (self.height / 2 - self.imagerect.height / 2)))

        if variables.mouseRect.colliderect(self.buttonrect) and variables.leftclick:

            if not self.just_pressed:
                self.just_pressed = True
                self.assigned_function()
        else:
            #print(variables.mouseRect.colliderect(self.buttonrect))
            self.just_pressed = False

    def changetext(self, screen, new_text):

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, self.roundedness)
        self.text = self.font.render(new_text, 1, self.textcolor)
        screen.blit(self.text, (
        self.x + (self.width / 2 - self.text.get_width() / 2), self.y + (self.height / 2 - self.text.get_height() / 2)))