# Yunabot Dice roller

## Features
- Create attack sets defining To-Hit and Damage
    - Like {"id":"uuid", "name": "arrow"(unique), "to-hit-mod": 8, "dmg": "1d10[necrotic]+4d6+11[piercing]"}
- Use attack combos for multiattack
    - `!multiattack arrow 2 claw 3` Will attack with 2 arrows and 3 claws
    - `!multiattack arrow 2 claw 3 -dc=15` will check to-hit against the DC
    - `!multiattack arrow 1 adv arrow 1 claw 2 adv claw 1` to hit 2 claws and 1 arrow at advantage, rest normally
- Use normal Iter attacks
    - `!atk 3 "1d20+15 adv" "1d10[necrotic]+1d5[fire]"`
    - This should give 3 things
        - Consolidated values per attack: `7[necrotic]+3[fire]`
        - Dice rolls per attack: `1d10(7)[necrotic]+1d5(3)[fire]`
        - Total of all attacks: `21[necrotic]+15[fire]`
- Handle crits
    - In case of any to-hit rolling a crit, double all damage dice for that attack and roll
    - Able to configure Crits
        - By default Crits land on a 20 on a 1d20 dice
        - For certain enemies the threshold might change
        - can add to the multiattack conf like
        ```json
        {"id":"uuid", "name": "arrow"(unique), "to-hit-mod": 8, "dmg": "1d10[necrotic]+4d6+11[piercing]", "crit": [18,19,20]}
        ```
        - can add to attack rolls as well
        `!atk 3 "1d20+15 adv" "1d10[necrotic]+1d5[fire]" -crit="19,20"`
    - User Context Crit Behaviour, Users can set contexts on what kind of crit they are using
        - Base (Default), doubles damage dice: 1d10+1d6 -> 2d10+2d6
        - Perkins, maxes die as mod: 1d10+1d6 -> 1d10+10+1d6+6
        - Double, doubles the base roll: 1d10+1d6 -> 2*(1d10+1d6)

**Use the D20 library whose documentation is defined here: https://d20.readthedocs.io/en/latest/start.html#documentation**