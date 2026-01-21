import pygame

def handle_event(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.Rect(300, 260, 300, 60).collidepoint(event.pos):
            return "login"
        if pygame.Rect(300, 340, 300, 60).collidepoint(event.pos):
            return "create"
    return None

def draw(screen):
    FONT = pygame.font.SysFont(None, 50)
    BIG  = pygame.font.SysFont(None, 70)

    screen.fill((0, 0, 0))

    screen.blit(BIG.render("BEM-VINDO", True, (255,255,255)), (320, 150))

    pygame.draw.rect(screen, (0,200,0), (300,260,300,60))
    pygame.draw.rect(screen, (0,100,200), (300,340,300,60))

    screen.blit(FONT.render("LOGIN", True, (0,0,0)), (400,275))
    screen.blit(FONT.render("CRIAR CONTA", True, (0,0,0)), (350,355))