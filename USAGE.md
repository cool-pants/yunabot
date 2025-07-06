# Yunabot Dice Roller Usage

## Basic Dice Rolls
Use the bot to roll any Avrae-style dice string:

```
!roll 2d20+5
```
Returns the result, e.g.:
```
2d20 (5, 7) + 5 = `17`
```

## Attack Sets
Define attacks with to-hit and damage:
```
!define_attack arrow --to-hit-mod=8 --dmg="1d10[necrotic]+4d6+11[piercing]"
```

## Multiattack
Attack with multiple weapons/attacks:
```
!multiattack arrow 2 claw 3
!multiattack arrow 2 claw 3 -dc=15
!multiattack arrow 1 adv arrow 1 claw 2 adv claw 1
```

## Iterative Attacks
Roll multiple attacks with advantage/disadvantage:
```
!atk 3 "1d20+15 adv" "1d10[necrotic]+1d5[fire]"
```

## Crits
- By default, crits land on a 20 on a 1d20.
- You can configure crit thresholds per attack or roll:
```
!define_attack arrow --crit="18,19,20"
!atk 3 "1d20+15 adv" "1d10[necrotic]+1d5[fire]" -crit="19,20"
```
- User context can set crit behavior (Base, Perkins, Double).

## Advanced Dice Expressions
Supports all Avrae/d20 syntax, e.g.:
```
!roll 4d6kh3
!roll 2d6ro<3
!roll 8d6mi2
!roll (1d4+1,3,2d6kl1)kh1
```

For more, see the [d20 documentation](https://d20.readthedocs.io/en/latest/start.html#documentation). 