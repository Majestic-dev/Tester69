import json
import os

def calculate_required_xp(level):
    return ((level ** 2) + (level ** 2)) * 7

def generate_levels(max_level):
    levels = {"levels": {}}
    total_xp = 0
    for level in range(1, max_level + 1):
        total_xp += calculate_required_xp(level)
        levels["levels"][str(level)] = {"requiredXP": total_xp}
    return levels

def write_levels_to_file(levels, filename):
    with open(filename, 'w') as f:
        json.dump(levels, f, indent=4)

levels = generate_levels(50)
filename = 'data/mine/levels.json'
os.makedirs(os.path.dirname(filename), exist_ok=True)
write_levels_to_file(levels, filename)