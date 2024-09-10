import re

# this is the logic to interpet user inputted combos
# and translating them into a visual representation


# combo notation
# 2MK > 236P - cancel 2MK into fireball
# LP~MP - chain MP after LP (target combos or additional inputs)
# 5MP, 2MP - link 2MP after 5MP
# [2] - charge input 2
# j. - jump
# dl. - delay

# command normals might have these
# 2 - ↓ (crouching)
# 4 - ←
# 6 - →

# drive meter moves
# DR - drive rush
# DI - drive impact

# motion inputs
# 214 - QCB
# 236 - QCF
# 623 - DP

# coutner states
# CH - counter hit
# PC - punish counter

def convert_combo(notation):
    # Mapping for move notations with patterns to ensure exact matching
    move_map = {
        r'\bj.': 'jumping ',
        r'\b5': 'standing ',
        r'\b2': 'crouching ',
        r'\b3': 'fwd_diag_down ',
        r'\b8': 'jumping ',
        r'\b4': 'back ',
        r'\b6': 'forward ',
        r'\bLP\b': 'LightPunch',
        r'\bMP\b': 'MediumPunch',
        r'\bHP\b': 'HeavyPunch',
        r'\bLK\b': 'LightKick',
        r'\bMK\b': 'MediumKick',
        r'\bHK\b': 'HeavyKick',
        r'\bP\b': 'Punch',
        r'\bK\b': 'Kick',
        r'\bPP\b': 'PP',
        r'\bPPP\b': 'PPP',
        r'\bKK\b': 'KK',
        r'\bKKK\b': 'KKK',
        r'\bLPLK\b': 'throw',
        r'\bDI\b': 'DI ',
        r'\bDRC\b': 'DRC ',
        r'\bDR\b': 'DR '
    }

    # Mapping for special notations
    special_map = {
        ',': ' link ',
        '>': ' cancel ',
        r'\[2\]8': 'charge_down_up ',
        r'\[4\]646': 'charge_back_forward_back_forward ',
        r'\[4\]6': 'charge_back_forward ',
        r'LP~LP~6LK~HP': 'demon ',
        r'214214': 'qcb2 ',
        r'236236': 'qcf2 ',
        r'41236': ' hcf ',
        r'63214': ' hcb ',
        r'214': ' qcb ',
        r'236': ' qcf ',
        r'623': ' dp ',
        r'421': ' reverse_dp ',
        r'360': ' spd ',
        r'720': ' double_spd ',
        '~': ' chain '
    }

    def translate_move(move):
        # Replace special notations first using regular expressions
        for key, value in special_map.items():
            move = re.sub(key, value, move)
        # Replace move notations using regular expressions
        for key, value in move_map.items():
            move = re.sub(key, value, move)
        return move

    # Split by 'link' notation
    parts = notation.split(',')
    converted_combo = []

    for part in parts:
        # Split by 'cancel' notation
        moves = part.split('>')
        converted_moves = [translate_move(move) for move in moves]
        # Join parts by 'cancel'
        converted_combo.append(' cancel '.join(converted_moves))

    # Join all parts by 'link'
    return ' link '.join(converted_combo)


# Example usage
# combo = 'j.MK, 5MP, 2MP > [2]8MK'
combo = "j.MK > 5LP, 2MP ~ [2]8K, 5P"
result = convert_combo(combo)
print(result)
