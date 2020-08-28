
import itertools
from termcolor import cprint
from deck import Deck

deck1 = Deck()

hand = []

active = True


def find_card_name(card_list, name):
    for card in card_list:
        if card.name.lower() == name.lower():
            return card
    return None


def add_card(cards):
    while True:
        card = find_card_name(cards, input("enter a card: "))
        if card:
            hand.append(card)
            cards.remove(card)
            break
        else:
            print("input a valid card: ")


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
    if len(card_list) > 4:
        flush = all(c == first_suit for c in ([d.suit for d in card_list[0:5]]))
        if flush:
            hand_total += 5
    if len(card_list) > 3 and not flush:
        flush = all(c == first_suit for c in ([d.suit for d in card_list[0:4]]))
        if flush:
            hand_total += 4
    return hand_total


def discard_ai_advanced():  # add scoring from aces and 5's
    keep_hand_value = -10
    keep_hand = []
    proxy_deck = Deck()
    deck_minus_hand = [c for c in proxy_deck.cards if c.name not in [c.name for c in hand]]  # this isn't doing anything
    for seq in itertools.combinations(hand, 4):
        potential_values = []
        cprint(seq, "yellow")
        discarded_cards = [c for c in hand if c not in seq]
        cprint(discarded_cards, "blue")
        for c in deck_minus_hand:
            if active:
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
        cprint("keep potential values", "yellow")
        cprint(potential_values, "red")
        expected_value = sum(potential_values)/46
        cprint("keep EV:", "yellow")
        cprint(expected_value, "red")
        print("\n")
        if expected_value > keep_hand_value:
            keep_hand_value = expected_value
            keep_hand = list(seq)
        elif expected_value == keep_hand_value:
            if sum(e.value for e in seq) < sum(e.value for e in keep_hand):
                keep_hand = list(seq)
    cprint(hand, "blue")
    cprint(keep_hand, "yellow")


for i in range(6):
    add_card(deck1.cards)

discard_ai_advanced()
