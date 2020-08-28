
from termcolor import cprint
import random
import itertools
from deck import Deck


def find_card_name(card_list, name):
    for card in card_list:
        if card.name.lower() == name.lower():
            return card
    return None


def sort_hand_value(card_list):
    return card_list.sort(key=lambda x: x.run_value)


class Player:

    def __init__(self, name, deck, score, crib, p_type, active):
        self.hand = []
        self.name = name  # can change this to a __str__ or __repr__
        self.deck = deck
        self.score = score
        self.crib = crib
        self.p_type = p_type  # 0 = human, 1 = easy AI, 2 = intermediate AI, 3 = Expert AI
        self.active = active
        self.void = []
        self.playable_card = None
        self.first_go = False

    def draw_hand(self):  # draw initial hand
        for c in range(6):
            self.hand.append(self.deck.draw())

    def show_hand(self):  # shows the cards in hand
        for c in self.hand:
            c.show()

    def show_hand_counting(self):  # shows the cards in hand for counting points
        for c in self.hand[0:4]:
            c.show()
        print("the cut:")  # cut shown separately for clarity
        self.deck.the_cut[0].show()

    def discard(self):

        def discard_player():  # discarded hands create crib hand
            while True:
                discard1 = find_card_name(self.hand, input("choose a card to discard: "))
                if discard1:
                    self.crib.cards.append(discard1)
                    self.hand.remove(discard1)
                    break
                else:
                    print("input error. Enter a valid card to discard: ")
            while True:
                discard2 = find_card_name(self.hand, input("choose another card to discard: "))
                if discard2:
                    self.crib.cards.append(discard2)
                    self.hand.remove(discard2)
                    break
                else:
                    print("input error. Enter a valid card to discard: ")

        def discard_ai_easy():
            discard1 = random.choice(self.hand)
            self.crib.cards.append(discard1)
            self.hand.remove(discard1)
            discard2 = random.choice(self.hand)
            self.crib.cards.append(discard1)
            self.hand.remove(discard2)

        def abbr_count_hand(card_list):  # determine number of points in hand
            hand_total = 0  # this local variable will display the amount of point in the hand

            def sum_card_values(cards):
                return sum(e.value for e in cards)

            def is_run(cards):
                if all((card.run_value - index) == cards[0].run_value for index, card in enumerate(cards)):
                    return True

            def is_pair(cards):
                if cards[0].run_value == cards[1].run_value:
                    return True

            for c in range(len(card_list)):  # determining all 15's in hand
                for seq in itertools.combinations(card_list, c + 1):
                    if sum_card_values(seq) == 15:
                        hand_total += 2
            run = False  # this parameter helps not runs of 3 if run of 4 exists, or run of 4 if run of 5 exists
            run_hand = list(card_list)
            run_hand.sort(key=lambda x: x.run_value)
            for seq in itertools.combinations(run_hand, 5):  # check if there is a run of five first
                if is_run(seq):
                    hand_total += 5
                    run = True
            if not run:
                for seq in itertools.combinations(run_hand, 4):  # check for runs of 4
                    if is_run(seq):
                        hand_total += 4
                        run = True
            if not run:
                for seq in itertools.combinations(run_hand, 3):  # check for runs of 3
                    if is_run(seq):
                        hand_total += 3
            for seq in itertools.combinations(card_list, 2):  # check for pairs
                if is_pair(seq):
                    hand_total += 2
            first_suit = card_list[0].suit
            flush = False
            if len(card_list) > 4:    #@@@@@ make sure works with medium and adv
                flush = all(c == first_suit for c in ([d.suit for d in card_list[0:5]]))
                if flush:
                    hand_total += 5
            if len(card_list) > 3 and not flush:
                flush = all(c == first_suit for c in ([d.suit for d in card_list[0:4]]))
                if flush:
                    hand_total += 4
            return hand_total

        def discard_ai_intermediate():
            keep_hand_value = 0
            keep_hand = []
            for seq in itertools.combinations(self.hand, 4):
                discarded_cards = [c for c in self.hand if c not in seq]
                if self.active:
                    total_points = abbr_count_hand(seq) - abbr_count_hand(discarded_cards)
                else:
                    total_points = abbr_count_hand(seq) + abbr_count_hand(discarded_cards)
                if total_points > keep_hand_value:
                    keep_hand_value = total_points
                    keep_hand = list(seq)
                elif total_points == keep_hand_value:
                    if sum(e.value for e in seq) < sum(e.value for e in keep_hand):
                        keep_hand = list(seq)
            self.crib.cards.extend(c for c in self.hand if c not in keep_hand)
            self.hand = keep_hand.copy()

        def discard_ai_expert():  # add scoring from aces and 5's
            keep_hand_value = -10
            keep_hand = []
            proxy_deck = Deck()
            deck_minus_hand = [c for c in proxy_deck.cards if c.name not in [c.name for c in self.hand]]  # this isn't doing anything
            for seq in itertools.combinations(self.hand, 4):
                potential_values = []
                discarded_cards = [c for c in self.hand if c not in seq]
                for c in deck_minus_hand:
                    if self.active:
                        potential_value = abbr_count_hand(seq + (c,)) - abbr_count_hand(discarded_cards + [c])
                        for d in discarded_cards:
                            if d.run_value == 5:
                                potential_value -= 1.2
                    else:
                        potential_value = abbr_count_hand(seq + (c,)) + abbr_count_hand(discarded_cards + [c])
                    for e in seq:
                        if e.run_value == 1:
                            potential_value += 1
                    potential_values.append(potential_value)
                expected_value = sum(potential_values)/46
                if expected_value > keep_hand_value:
                    keep_hand_value = expected_value
                    keep_hand = list(seq)
                elif expected_value == keep_hand_value:
                    if sum(e.value for e in seq) < sum(e.value for e in keep_hand):
                        keep_hand = list(seq)
            self.crib.cards.extend(c for c in self.hand if c not in keep_hand)
            self.hand = keep_hand.copy()

        if self.p_type == 0:
            discard_player()

        if self.p_type == 1:
            discard_ai_easy()

        if self.p_type == 2:
            discard_ai_intermediate()

        if self.p_type == 3:
            discard_ai_expert()

    def discard_phase(self):
        if self.p_type == 0:
            cprint(self.name + "'s hand:", "yellow")  # active draw and discard
        else:
            cprint(self.name + " discard", "yellow")
        self.draw_hand()  # might want to just have player1 draw/discard first every round?
        sort_hand_value(self.hand)
        if self.p_type == 0:
            self.show_hand()
        self.discard()
        input(". . .")
        print("\n")

    def empty_hand(self):  # return cards to deck and delete cards in hand
        self.deck.cards.extend(self.hand[0:4])
        self.hand.clear()

    def crib_hand(self):  # put all the cards from the crib into a players hand and count the points in hand
        for c in self.crib.cards:
            self.hand.append(c)
        self.crib.cards.clear()
