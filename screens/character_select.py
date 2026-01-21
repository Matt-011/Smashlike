import pygame

# ======================
# CONFIG
# ======================
BG = (10, 20, 45)
CARD = (220, 220, 220)
BORDER = (0, 200, 140)
TEXT = (255, 255, 255)

CHARACTERS = [
    {"id": "char1", "name": "Personagem 1"},
    {"id": "char2", "name": "Personagem 2"},
    {"id": "char3", "name": "Personagem 3"},
    {"id": "char4", "name": "Personagem 4"},
    {"id": "char5", "name": "Personagem 5"},
]

hovered = None
selected = None


# ======================
# EVENTS
# ======================
def handle_event(event):
    global selected

    if event.type == pygame.MOUSEBUTTONDOWN:
        for i, rect in enumerate(character_rects()):
            if rect.collidepoint(event.pos):
                selected = i


# ======================
# LAYOUT
# ======================
def character_rects():
    start_x = 100
    gap = 150
    y = 220
    return [pygame.Rect(start_x + i * gap, y, 120, 160) for i in range(5)]


# ======================
# DRAW
# ======================
def draw(screen):
    global hovered

    FONT = pygame.font.SysFont(None, 26)
    TITLE = pygame.font.SysFont(None, 48)
    BIG = pygame.font.SysFont(None, 36)

    screen.fill(BG)
    hovered = None

    screen.blit(TITLE.render("ESCOLHA SEU PERSONAGEM", True, TEXT), (220, 50))

    mouse = pygame.mouse.get_pos()

    for i, char in enumerate(CHARACTERS):
        rect = character_rects()[i]

        is_hover = rect.collidepoint(mouse)
        is_selected = selected == i

        if is_hover:
            hovered = i

        pygame.draw.rect(
            screen,
            CARD,
            rect,
            border_radius=14
        )

        if is_hover or is_selected:
            pygame.draw.rect(
                screen,
                BORDER,
                rect,
                4,
                border_radius=14
            )

        # "Imagem" provisória
        color = (100 + i * 20, 100, 150)
        pygame.draw.rect(screen, color, (rect.x + 20, rect.y + 20, 80, 80))

        name = FONT.render(char["name"], True, (0, 0, 0))
        screen.blit(name, (rect.centerx - name.get_width() // 2, rect.y + 115))

    if selected is not None:
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        text = BIG.render("PERSONAGEM ESCOLHIDO", True, TEXT)
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 160))
