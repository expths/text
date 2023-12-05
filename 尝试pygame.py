import pygame

class Game(pygame.sprite.Sprite):
    pass

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((480,360))
pygame.display.set_caption("Game")

keep_going = True
while keep_going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False
    screen.fill((0,255,0))
    pygame.draw.circle(screen,(255,0,0),(50,50),20)
    pygame.draw.circle(screen,(255,0,0),(100,50),20)
    pygame.display.update()

pygame.quit()