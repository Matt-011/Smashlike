import pygame
import sys

from screens import (
    menu_start,
    login,
    create_account,
    main_menu,
    store,
    inventory,
    character_select
)

# ======================
# CONFIGURAÇÃO BÁSICA
# ======================
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smash Like Game")

clock = pygame.time.Clock()

# ======================
# CONTROLE DE TELAS
# ======================
screen_state = "menu_start"
current_account = None

# ======================
# LOOP PRINCIPAL
# ======================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------- MENU INICIAL --------
        if screen_state == "menu_start":
            result = menu_start.handle_event(event)
            if result == "login":
                screen_state = "login"
            elif result == "create":
                screen_state = "create_account"

        # -------- CRIAR CONTA --------
        elif screen_state == "create_account":
            result = create_account.handle_event(event)
            if isinstance(result, dict):
                current_account = result
                screen_state = "main_menu"

        # -------- LOGIN --------
        elif screen_state == "login":
            result = login.handle_event(event)
            if isinstance(result, dict):
                current_account = result
                screen_state = "main_menu"

        # -------- MENU PRINCIPAL --------
        elif screen_state == "main_menu":
            result = main_menu.handle_event(event)
            if result == "store":
                screen_state = "store"
            elif result == "inventory":
                screen_state = "inventory"
            elif result == "character_select":
                screen_state = "character_select"

        # -------- SELEÇÃO DE PERSONAGEM --------
        elif screen_state == "character_select":
            character_select.handle_event(event)

        # -------- LOJA --------
        elif screen_state == "store":
            result = store.handle_event(event, current_account)
            if result == "main_menu":
                screen_state = "main_menu"

        # -------- INVENTÁRIO --------
        elif screen_state == "inventory":
            result = inventory.handle_event(event, current_account)
            if result == "main_menu":
                screen_state = "main_menu"

    # ======================
    # DESENHO DAS TELAS
    # ======================
    if screen_state == "menu_start":
        menu_start.draw(screen)

    elif screen_state == "create_account":
        create_account.draw(screen)

    elif screen_state == "login":
        login.draw(screen)

    elif screen_state == "main_menu":
        main_menu.draw(screen, current_account)

    elif screen_state == "character_select":
        character_select.draw(screen)

    elif screen_state == "store":
        store.draw(screen, current_account)

    elif screen_state == "inventory":
        inventory.draw(screen, current_account)

    pygame.display.flip()
    clock.tick(60)

