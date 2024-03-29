import pygame


string_to_display = "χρυσοποιία"

pygame.init()
run = True
screen = pygame.display.set_mode((400, 300), pygame.SCALED)
text_font = pygame.font.SysFont("Papyrus", size=40)


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    text_surface = text_font.render(string_to_display, False, (255, 255, 255))

    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
pygame.quit()

