import pygame


class Button:
    def __init__(self, pos_center, width, height, image, text=None, sound=None):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=pos_center)
        self.text = text
        self.sound = pygame.mixer.Sound(sound) if sound else None
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        else:
            self.sound = None

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.text:
            font = pygame.font.SysFont(name='Arial', size=30, bold=True, italic=True)
            text_surf = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def press_button(self):
        p = pygame.mouse.get_pressed()
        if p[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if self.sound:
                    self.sound.play()
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
