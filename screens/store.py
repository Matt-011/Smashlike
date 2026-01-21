# screens/store.py

import pygame
import datetime
from utils.account_manager import load_accounts, save_accounts
from utils.items_database import ITEMS_DATABASE

# =========================
# RARIDADE
# =========================
RARITY_COLORS = {
    "common":   (170, 170, 170),
    "uncommon": (0, 200, 140),
    "rare":     (80, 120, 255),
    "limited":  (255, 180, 60)
}

# =========================
# ROTAÇÃO DA LOJA (0 a 6)
# =========================
SHOP_ROTATIONS = {
    0: ["avatar_validation", "banner_padrao", "skin_padrao"],
    1: ["skin_gold", "banner_padrao", "avatar_validation"],
    2: ["avatar_validation", "skin_padrao", "banner_padrao"],
    3: ["banner_padrao", "skin_gold", "avatar_validation"],
    4: ["skin_padrao", "avatar_validation", "banner_padrao"],
    5: ["skin_gold", "skin_padrao", "avatar_validation"],
    6: ["banner_padrao", "skin_gold", "skin_padrao"],
}

# =========================
# CORES
# =========================
BG = (10, 20, 45)
CARD = (235, 235, 235)
CARD_OWNED = (190, 190, 190)
RED = (200, 60, 60)
TEXT = (20, 20, 20)

selected_item = None
confirming = False


# =========================
# UTIL
# =========================
def get_today_items():
    today = datetime.datetime.now().weekday()
    return [ITEMS_DATABASE[i] for i in SHOP_ROTATIONS[today]]


def seconds_to_midnight():
    now = datetime.datetime.now()
    midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
    return int((midnight - now).total_seconds())


# =========================
# EVENTS
# =========================
def handle_event(event, account):
    global selected_item, confirming

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        if pygame.Rect(20, 20, 44, 44).collidepoint(x, y):
            confirming = False
            selected_item = None
            return "main_menu"

        if confirming:
            if pygame.Rect(330, 360, 140, 50).collidepoint(x, y):
                confirming = False
                selected_item = None
            elif pygame.Rect(490, 360, 140, 50).collidepoint(x, y):
                buy_item(account)
                confirming = False
                selected_item = None
            return None

        for i, rect in enumerate(item_rects()):
            item = get_today_items()[i]
            if rect.collidepoint(x, y):
                if item["id"] in account["inventory"][item["type"]]:
                    return None
                selected_item = item
                confirming = True
                return None

    return None


# =========================
# BUY
# =========================
def buy_item(account):
    global selected_item

    t = selected_item["type"]
    i = selected_item["id"]

    if i in account["inventory"][t]:
        return

    account["inventory"][t].append(i)

    accounts = load_accounts()
    for idx, acc in enumerate(accounts):
        if acc["username"] == account["username"]:
            accounts[idx] = account
            break
    save_accounts(accounts)


# =========================
# LAYOUT
# =========================
def item_rects():
    start_x = 170
    gap = 200
    return [pygame.Rect(start_x + i * gap, 210, 170, 220) for i in range(3)]


# =========================
# DRAW
# =========================
def draw(screen, account):
    FONT = pygame.font.SysFont(None, 26)
    BIG = pygame.font.SysFont(None, 60)
    TITLE = pygame.font.SysFont(None, 64)

    screen.fill(BG)

    screen.blit(TITLE.render("LOJA", True, (220, 220, 220)), (385, 40))

    pygame.draw.rect(screen, RED, (20, 20, 44, 44), border_radius=10)
    screen.blit(BIG.render("×", True, (255, 255, 255)), (30, 14))

    timer = seconds_to_midnight()
    mins = timer // 60
    secs = timer % 60
    screen.blit(FONT.render(f"Atualiza em {mins:02d}:{secs:02d}", True, (200, 200, 200)), (20, 80))

    items = get_today_items()

    for i, item in enumerate(items):
        rect = item_rects()[i]
        owned = item["id"] in account["inventory"][item["type"]]

        pygame.draw.rect(screen, CARD_OWNED if owned else CARD, rect, border_radius=18)

        pygame.draw.rect(
            screen,
            RARITY_COLORS[item["rarity"]],
            rect,
            3,
            border_radius=18
        )

        img = load_item_image(item["type"], item["id"])
        if img:
            screen.blit(img, (rect.centerx - 45, rect.y + 25))

        name = FONT.render(item["name"], True, TEXT)
        screen.blit(name, (rect.centerx - name.get_width() // 2, rect.y + 135))

        rarity_text = item["rarity"].upper() if item["rarity"] != "limited" else "LIMITED"
        rarity = FONT.render(rarity_text, True, RARITY_COLORS[item["rarity"]])
        screen.blit(rarity, (rect.centerx - rarity.get_width() // 2, rect.y + 165))

    if confirming and selected_item:
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(280, 230, 340, 240)
        pygame.draw.rect(screen, (245, 245, 245), box, border_radius=18)

        img = load_item_image(selected_item["type"], selected_item["id"])
        if img:
            screen.blit(img, (box.centerx - 45, box.y + 20))

        txt = FONT.render(f"Comprar {selected_item['name']}?", True, TEXT)
        screen.blit(txt, (box.centerx - txt.get_width() // 2, box.y + 120))

        pygame.draw.rect(screen, RED, (330, 360, 140, 50), border_radius=12)
        pygame.draw.rect(screen, RARITY_COLORS[selected_item["rarity"]], (490, 360, 140, 50), border_radius=12)

        screen.blit(FONT.render("NÃO", True, (255, 255, 255)), (380, 375))
        screen.blit(FONT.render("SIM", True, (0, 0, 0)), (545, 375))


# =========================
# IMAGE
# =========================
def load_item_image(item_type, item_id):
    try:
        img = pygame.image.load(f"assets/items/{item_type}/{item_id}.png").convert_alpha()
        return pygame.transform.scale(img, (90, 90))
    except:
        return None
