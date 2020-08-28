from termcolor import cprint
import random


class Card:

    def __init__(self, suit, value, description, run_value):
        self.value = value  # value of card for counting
        self.suit = suit
        self.description = description  # for creating name
        self.name = "{} of {}".format(self.description, self.suit)
        self.run_value = run_value  # value for determining runs

    def __repr__(self):
        return str(self.description)

    def show(self):
        cprint(str(self.description) + " of ", "grey", end="")
        if self.suit == "Spades" or self.suit == "Clubs":
            cprint(self.suit, "blue", attrs=["dark"])
        else:
            cprint(self.suit, "red")


card_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
card_descriptions = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
card_run_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


class Deck:
    def __init__(self):
        self.cards = []
        self.generate()
        self.shuffle()
        self.the_cut = []

    def generate(self):  # generate deck of cards
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for i in range(0, 13):
                self.cards.append(Card(s, card_values[i], card_descriptions[i], card_run_values[i]))

    def shuffle(self):  # randomizes deck
        random.shuffle(self.cards)

    def draw(self):  #to add cards hands or the_cut
        return self.cards.pop()

    def cut(self):  # this card is added to hands when counting the points in that hand
        self.shuffle()
        self.the_cut.append(self.draw())
        for c in self.the_cut:
            print("The cut:")
            c.show()

    def empty_cut(self):  # returns the_cut back to the deck
        for c in self.the_cut:
            self.cards.append(c)
        self.the_cut.clear()


class Crib:  # just a holding place for the crib hand

    def __init__(self):
        self.cards = []

    def show_crib(self):  # useless functionality
        for c in self.cards:
            c.show()
