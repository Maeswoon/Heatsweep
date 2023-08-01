import math
elo1 = 1200
elo2 = 1000
k = 30 # some contant gain/loss vlaue

winner = 2

player_one_ratio = (1 / (1 + pow(10, ((elo2-elo1) / 400)))) 
player_two_ratio = (1 / (1 + pow(10, ((elo1-elo2) / 400))))
if winner == 1:
    newElo1 = math.floor(elo1 + k*(1 - player_one_ratio))
    newElo2 =  math.floor(elo2 + k*(0 - player_two_ratio))
else:
    newElo1 = math.floor(elo1 + k*(0 - player_one_ratio))
    newElo2 =  math.floor(elo2 + k*(1 - player_two_ratio))

print(f"Elo1 == {elo1}")
print(f"Elo2 == {elo2}")
print(f"NewElo1 == {newElo1}")
print(f"NewElo2 == {newElo2}")