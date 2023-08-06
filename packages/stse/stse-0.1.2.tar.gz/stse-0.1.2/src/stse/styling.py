import random


def random_hex_color(seed=42):
    if seed:
        random.seed(seed)
        
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))
