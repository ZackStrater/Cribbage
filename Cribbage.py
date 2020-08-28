
from deck import Deck, Crib
from player import Player
from game import Game


deck1 = Deck()

crib1 = Crib()


player_types = ("Human Player", "Easy Computer", "Intermediate Computer", "Expert Computer")
for p in player_types:
    print(p)
player_types = [player_type.lower() for player_type in player_types]

player_1 = None
player_2 = None
player_1_type = input("Choose Player 1 type:").lower()
while player_1_type not in player_types:
    player_1_type = input("Choose a valid player type:").lower()
if player_1_type == "human player":
    player_1_name = input("Choose Player 1 name:")
    player_1 = Player(player_1_name, deck1, 0, crib1, 0, None)
if player_1_type == "easy computer":
    player_1 = Player("Easy Computer", deck1, 0, crib1, 1, None)
if player_1_type == "intermediate computer":
    player_1 = Player("Intermediate Computer", deck1, 0, crib1, 2, None)
if player_1_type == "expert computer":
    player_1 = Player("Expert Computer", deck1, 0, crib1, 3, None)

player_2_type = input("Choose Player 2 type:").lower()
while player_2_type not in player_types:
    player_2_type = input("Choose a valid player type:").lower()
if player_2_type == "human player":
    player_2_name = input("Choose Player 2 name:")
    player_2 = Player(player_2_name, deck1, 0, crib1, 0, None)
if player_2_type == "easy computer":
    player_2 = Player("Easy Computer", deck1, 0, crib1, 1, None)
if player_2_type == "intermediate computer":
    player_2 = Player("Intermediate Computer", deck1, 0, crib1, 2, None)
if player_2_type == "expert computer":
    player_2 = Player("Expert Computer", deck1, 0, crib1, 3, None)


game1 = Game(player_1, player_2, deck1, crib1)


while game1.winner is None:
    game1.round()


print(str(game1.winner.name) + " wins!")
