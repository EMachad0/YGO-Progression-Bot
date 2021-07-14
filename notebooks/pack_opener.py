from random import choice, choices


def get_common_type():
    rarity = ['Common', 'Short Print', 'Super Short Print']
    odds = [57, 2, 1]
    return choices(rarity, weights=odds, k=1)[0]


def get_foil_type():
    rarity = ['Super Rare', 'Ultra Rare', 'Secret Rare']
    odds = [9, 2, 1]
    return choices(rarity, weights=odds, k=1)[0]


def get_pack_rarities():
    return [get_common_type() for _ in range(7)] + ["Rare"] + [get_foil_type()]


def get_random_pack(card_pool):
    pack = [choice(card_pool[rarity]) for rarity in get_pack_rarities()]
    return pack


def get_card_pool(set_cards):
    card_pool = {}
    for c in set_cards:
        if c.rarity not in card_pool:
            card_pool[c.rarity] = []
        card_pool[c.rarity].append(c)
    return card_pool