import pygame
import layer

FPS = 60
screen = (480,360)
screen_name = "game"

class background(layer):
    def __init__(self) -> None:
        super().__init__()
    def draw(self) -> None:
        screen.fill((255,255,255))

class plane(layer.layer):
    def __init__(self,site:tuple) -> None:
        super().__init__()
        self.site = site
    def draw(self):
        pygame.draw.circle(screen,(255,0,0),(50,50),20)
    def behavior(self):
        self.site = (self.site[0],self.site[1]+1)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(screen)
pygame.display.set_caption(screen_name)
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #绘制
    pygame.display.update()

pygame.quit()