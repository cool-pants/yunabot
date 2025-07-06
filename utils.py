import re
from dataclasses import dataclass
from typing import List

@dataclass
class Damage:
    num: int           # number of dice
    dice_size: int     # size of dice
    modifier: int      # flat modifier (typically 0 unless added separately)
    dmg_type: str      # type of damage (can be '' if unspecified)

def parse_damage_string(dmg_str: str) -> List[Damage]:
    pattern = re.compile(
        r"(?P<num>\d+)d(?P<dice>\d+)(?:\+(?P<mod>\d+))?(?:\[(?P<type>[a-zA-Z]+)\])?"
        r"|(?P<flatmod>\d+)\[(?P<flatmodtype>[a-zA-Z]+)\]"
    )

    damages = []

    for match in pattern.finditer(dmg_str):
        if match.group("flatmod"):
            # Flat modifier damage with a type (e.g., +2[necrotic])
            dmg = Damage(
                num=0,
                dice_size=0,
                modifier=int(match.group("flatmod")),
                dmg_type=match.group("flatmodtype")
            )
        else:
            dmg = Damage(
                num=int(match.group("num")),
                dice_size=int(match.group("dice")),
                modifier=int(match.group("mod") or 0),
                dmg_type=match.group("type") or ""
            )
        damages.append(dmg)

    return damages

def compute_crit(damages: List[Damage]) -> str:
    parts = []
    for d in damages:
        if d.num > 0:
            crit_num = d.num * 2
            part = f"{crit_num}d{d.dice_size}"
            if d.modifier:
                part += f"+{d.modifier}"
            if d.dmg_type:
                part += f"[{d.dmg_type}]"
        else:
            # Flat modifier damage with type (e.g., 2[necrotic])
            part = f"{d.modifier}[{d.dmg_type}]"
        parts.append(part)
    return '+'.join(parts)
