import pygame
from utils.account_manager import login_account

pygame.font.init()
FONT = pygame.font.SysFont(None, 40)

username = ""
password = ""
active = "user"


def handle_event(event):
    global username, password, active

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            active = "pass" if active == "user" else "user"

        elif event.key == pygame.K_BACKSPACE:
            if active == "user":
                username = username[:-1]
            else:
                password = password[:-1]

        elif event.key == pygame.K_RETURN:
            acc = login_account(username, password)
            if acc:
                return acc

        else:
            if active == "user":
                username += event.unicode
            else:
                password += event.unicode

    return None


def draw(screen):
    screen.fill((0, 0, 0))

    screen.blit(FONT.render("LOGIN", True, (255, 255, 255)), (380, 80))
    screen.blit(FONT.render("Usuário:", True, (255, 255, 255)), (200, 200))
    screen.blit(FONT.render(username, True, (0, 255, 0)), (350, 200))

    screen.blit(FONT.render("Senha:", True, (255, 255, 255)), (200, 260))
    screen.blit(FONT.render("*" * len(password), True, (0, 255, 0)), (350, 260))