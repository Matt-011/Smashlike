import pygame

def handle_event(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        # Botão JOGAR → SELEÇÃO DE PERSONAGEM
        if pygame.Rect(300, 260, 300, 80).collidepoint(x, y):
            return "character_select"

        # Botão LOJA
        if pygame.Rect(650, 230, 180, 60).collidepoint(x, y):
            return "store"

        # Botão INVENTÁRIO
        if pygame.Rect(650, 310, 180, 60).collidepoint(x, y):
            return "inventory"

    return None


def draw(screen, account):
    FONT = pygame.font.SysFont(None, 30)
    BIG  = pygame.font.SysFont(None, 60)

    screen.fill((0, 120, 0))

    # =========================
    # GARANTE CAMPOS
    # =========================
    if "equipped" not in account:
        account["equipped"] = {
            "avatar": None,
            "banner": None
        }

    # =========================
    # PERFIL
    # =========================
    photo_rect  = pygame.Rect(20, 20, 70, 70)
    banner_rect = pygame.Rect(100, 20, 320, 70)

    # BANNER
    if account["equipped"]["banner"]:
        banner_img = load_image("banners", account["equipped"]["banner"], (320, 70))
        if banner_img:
            screen.blit(banner_img, banner_rect.topleft)
        else:
            pygame.draw.rect(screen, (40, 40, 40), banner_rect)
    else:
        pygame.draw.rect(screen, (40, 40, 40), banner_rect)

    # AVATAR
    if account["equipped"]["avatar"]:
        avatar_img = load_image("avatars", account["equipped"]["avatar"], (70, 70))
        if avatar_img:
            screen.blit(avatar_img, photo_rect.topleft)
        else:
            pygame.draw.rect(screen, (200, 200, 200), photo_rect)
    else:
        pygame.draw.rect(screen, (200, 200, 200), photo_rect)

    # Nome e ID
    name_text = FONT.render(account["username"], True, (255, 255, 255))
    id_text   = FONT.render(f"ID: {account['id']}", True, (200, 200, 200))
    screen.blit(name_text, (110, 28))
    screen.blit(id_text, (110, 55))

    # =========================
    # BOTÃO JOGAR
    # =========================
    jogar_rect = pygame.Rect(300, 260, 300, 80)
    pygame.draw.rect(screen, (0, 200, 0), jogar_rect, border_radius=12)
    screen.blit(BIG.render("JOGAR", True, (0, 0, 0)), (385, 282))

    # =========================
    # BOTÕES LATERAIS
    # =========================
    loja_rect = pygame.Rect(650, 230, 180, 60)
    pygame.draw.rect(screen, (0, 100, 200), loja_rect, border_radius=10)
    screen.blit(FONT.render("LOJA", True, (255,255,255)), (710, 248))

    inv_rect = pygame.Rect(650, 310, 180, 60)
    pygame.draw.rect(screen, (120, 120, 120), inv_rect, border_radius=10)
    screen.blit(FONT.render("INVENTÁRIO", True, (255,255,255)), (680, 328))


def load_image(item_type, item_id, size):
    try:
        path = f"assets/items/{item_type}/{item_id}.png"
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        return None
