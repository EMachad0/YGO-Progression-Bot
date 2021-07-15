from random import choice, choices


def get_random_rarity(rarities):
    return choices(list(rarities.keys()), weights=rarities.values(), k=1)[0]


def get_random_pack(card_pool, set_type):
    for c in set_type:
        for rar in c:
            if card_pool.get(rar) is None:
                c[rar] = 0
    pack = [choice(card_pool[get_random_rarity(rs)]) for rs in set_type]
    return pack


def get_card_pool(set_cards):
    card_pool = {}
    for c in set_cards:
        if c.rarity not in card_pool:
            card_pool[c.rarity] = []
        card_pool[c.rarity].append(c)
    return card_pool
