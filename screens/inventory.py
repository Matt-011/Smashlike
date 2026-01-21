import pygame
from utils.account_manager import load_accounts, save_accounts

tab = "skins"

def handle_event(event, account):
    global tab

    if not account:
        return None

    # garante equipped
    if "equipped" not in account:
        account["equipped"] = {"avatar": None, "banner": None}

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        # voltar
        if 20 < x < 70 and 20 < y < 70:
            return "main_menu"

        # trocar aba
        if 200 < x < 300 and 120 < y < 160:
            tab = "skins"
        elif 310 < x < 410 and 120 < y < 160:
            tab = "banners"
        elif 420 < x < 520 and 120 < y < 160:
            tab = "avatars"

        # clicar nos itens (equipar)
        items = account["inventory"].get(tab, [])
        for i, item in enumerate(items):
            rect = pygame.Rect(
                200 + (i % 4) * 120,
                200 + (i // 4) * 120,
                100,
                100
            )
            if rect.collidepoint(event.pos):
                if tab == "avatars":
                    account["equipped"]["avatar"] = item
                elif tab == "banners":
                    account["equipped"]["banner"] = item

                save_account(account)

    return None


def save_account(account):
    accounts = load_accounts()
    for i, acc in enumerate(accounts):
        if acc["username"] == account["username"]:
            accounts[i] = account
            break
    save_accounts(accounts)


def draw(screen, account):
    FONT = pygame.font.SysFont(None, 30)
    BIG  = pygame.font.SysFont(None, 50)

    screen.fill((30, 30, 30))

    if not account:
        return

    # segurança
    if "inventory" not in account:
        account["inventory"] = {"skins": [], "banners": [], "avatars": []}
    if "equipped" not in account:
        account["equipped"] = {"avatar": None, "banner": None}

    # voltar
    pygame.draw.rect(screen, (200, 0, 0), (20, 20, 50, 50))
    screen.blit(BIG.render("X", True, (255, 255, 255)), (32, 18))

    # abas
    pygame.draw.rect(screen, (120,120,120), (200,120,100,40))
    pygame.draw.rect(screen, (120,120,120), (310,120,100,40))
    pygame.draw.rect(screen, (120,120,120), (420,120,100,40))

    screen.blit(FONT.render("Skins", True, (0,0,0)), (225,130))
    screen.blit(FONT.render("Banners", True, (0,0,0)), (320,130))
    screen.blit(FONT.render("Fotinhas", True, (0,0,0)), (430,130))

    items = account["inventory"].get(tab, [])

    if not items:
        screen.blit(FONT.render("Nenhum item nessa aba", True, (200,200,200)), (320,260))

    for i, item in enumerate(items):
        rect = pygame.Rect(
            200 + (i % 4) * 120,
            200 + (i // 4) * 120,
            100,
            100
        )

        equipped = (
            (tab == "avatars" and account["equipped"]["avatar"] == item) or
            (tab == "banners" and account["equipped"]["banner"] == item)
        )

        color = (0,0,0) if equipped else (180,180,180)
        pygame.draw.rect(screen, color, rect, 3)

        img = load_item_image(tab, item)
        if img:
            screen.blit(img, (rect.x+5, rect.y+5))
        else:
            screen.blit(FONT.render(item, True, (255,255,255)), (rect.x+5, rect.y+40))


def load_item_image(item_type, item_id):
    try:
        path = f"assets/items/{item_type}/{item_id}.png"
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (90, 90))
    except:
        return None
