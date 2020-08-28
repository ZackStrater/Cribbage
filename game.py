import random
import itertools
from termcolor import cprint
from gameactions import play_card


def sort_hand_value(card_list):
    return card_list.sort(key=lambda x: x.run_value)


class Game:  # environment for the game, global var/objects should be available here

    def __init__(self, first_player, second_player, deck, crib):
        self.first_player = first_player  # reference for the players in the game
        self.second_player = second_player
        self.assign_active()
        self.deck = deck
        self.crib = crib
        self.active_player = None  # determines the order of the game sequence, determined below
        self.nonactive_player = None
        self.turn = None
        self.sequence = []
        self.count = 0
        self.last_play = None  # True mean first_player played last, False is second_player played last
        self.pair_counter = 0  # for counting how many pairs are in the sequence
        self.winner = None

    def assign_active(self):
        self.first_player.active = random.choice([True, False])
        if self.first_player.active:
            self.second_player.active = False
        else:
            self.second_player.active = True

    def give_points(self, player, points):
        player.score += points
        if player.score > 121 and self.winner is None:
            self.winner = player

    def counting_sequence(self):
        self.turn = False  # starts as false, so active player always plays first
        while self.active_player.hand != [] or self.nonactive_player.hand != []:  # play until hands are empty
            input(". . .")
            print("\n\n\n\n\n\n\n")
            play_card(self)
            self.reset_count()
        self.clean_up()
        input(". . .")
        print("\n")

    def reset_vars(self):
        self.count = 0
        self.sequence = []
        self.pair_counter = 0
        self.active_player.first_go = False
        self.nonactive_player.first_go = False
        self.active_player.playable_card = True
        self.nonactive_player.playable_card = True
        # if active_player has no cards in hand after a reset_count, it will assume nonactive player has no playable-
        # cards even if they do.  Setting both playable_card to True after reset_count prevents this

    def reset_count(self):
        if self.count == 31:
            self.reset_vars()
        elif not self.active_player.playable_card and not self.nonactive_player.playable_card:
            self.reset_vars()
            if self.last_play:
                self.give_points(self.active_player, 1)
                print(self.active_player.name + " gets 1 point for last card")
            else:
                self.give_points(self.nonactive_player, 1)
                print(self.nonactive_player.name + " gets 1 point for last card")

    def clean_up(self):
        if self.count != 31:
            if self.last_play:
                self.give_points(self.active_player, 1)
                print(self.active_player.name + " gets 1 point for last card")
            else:
                self.give_points(self.nonactive_player, 1)
                print(self.nonactive_player.name + " gets 1 point for last card")
        self.active_player.hand = self.active_player.void.copy()
        self.nonactive_player.hand = self.nonactive_player.void.copy()
        self.active_player.void.clear()
        self.nonactive_player.void.clear()
        self.reset_vars()

    def determine_active(self):  # assigns players to either active or nonactive, all subsequent events reference these
        if self.first_player.active:  # checks the active argument of the player
            self.active_player = self.first_player
            self.nonactive_player = self.second_player
        else:
            self.active_player = self.second_player
            self.nonactive_player = self.first_player

    def nibs(self):
        for c in self.deck.the_cut:
            if c.description == "Jack":
                self.give_points(self.nonactive_player, 2)
                print(self.nonactive_player.name + " gets 2 points for nibs")

    def count_hand(self, player):  # determine number of points in hand
        hand_total = 0  # this local variable will display the amount of point in the hand
        player.hand.extend(self.deck.the_cut)  # adding cut to hand for counting

        def sum_card_values(cards):
            return sum(e.value for e in cards)

        def is_run(cards):
            if all((card.run_value - index) == cards[0].run_value for index, card in enumerate(cards)):
                return True

        def is_pair(cards):
            if cards[0].run_value == cards[1].run_value:
                return True

        for c in range(len(player.hand)):  # determining all 15's in hand
            for seq in itertools.combinations(player.hand, c + 1):
                if sum_card_values(seq) == 15:
                    self.give_points(player, 2)
                    hand_total += 2
                    cprint("15 for " + str(hand_total) + ":", "cyan")
                    print(seq)
        run = False  # this parameter helps not runs of 3 if run of 4 exists, or run of 4 if run of 5 exists
        run_hand = player.hand.copy()
        run_hand.sort(key=lambda x: x.run_value)
        for seq in itertools.combinations(run_hand, 5):  # check if there is a run of five first
            if is_run(seq):
                self.give_points(player, 5)
                hand_total += 5
                cprint("run of 5 for " + str(hand_total) + ":", "cyan")
                print(seq)
                run = True
        if not run:
            for seq in itertools.combinations(run_hand, 4):  # check for runs of 4
                if is_run(seq):
                    self.give_points(player, 4)
                    hand_total += 4
                    cprint("run of 4 for " + str(hand_total) + ":", "cyan")
                    print(seq)
                    run = True
        if not run:
            for seq in itertools.combinations(run_hand, 3):  # check for runs of 3
                if is_run(seq):
                    self.give_points(player, 3)
                    hand_total += 3
                    cprint("run of 3 for " + str(hand_total) + ":", "cyan")
                    print(seq)
        for seq in itertools.combinations(player.hand, 2):  # check for pairs
            if is_pair(seq):
                self.give_points(player, 2)
                hand_total += 2
                cprint("pair for " + str(hand_total) + ":", "cyan")
                print(seq)
        first_suit = player.hand[0].suit
        flush_five = all(c == first_suit for c in ([d.suit for d in player.hand]))
        if flush_five:
            self.give_points(player, 5)
            hand_total += 5
            cprint("flush of 5 " + first_suit + " for " + str(hand_total), "cyan")
        flush_four = all(c == first_suit for c in ([d.suit for d in player.hand[0:4]]))
        if flush_four and not flush_five:
            self.give_points(player, 4)
            hand_total += 4
            cprint("flush of " + first_suit + " for " + str(hand_total), "cyan")
        for c in player.hand[0:4]:  # check to see if there is a jack in hand and if it's the same suit as the cut
            if c.run_value == 11 and c.suit == player.hand[4].suit:
                self.give_points(player, 1)
                hand_total += 1
                cprint("right Jack for " + str(hand_total), "cyan")
        print("hand total = " + str(hand_total))

    def round(self):  # sequence for a round of the game
        self.determine_active()  # determine active player

        print("\n")
        cprint(self.nonactive_player.name + "'s deal", "yellow")
        cprint(self.nonactive_player.name + "'s crib", "yellow")
        cprint(self.active_player.name + " plays and counts first", "yellow")
        input(". . .")
        print("\n")

        self.active_player.discard_phase()
        self.nonactive_player.discard_phase()

        print("\n")  # get the cut and check nibs
        self.deck.cut()
        self.nibs()

        self.counting_sequence()

        print("\n")
        print(self.first_player.name + " score = " + str(self.first_player.score))
        print(self.second_player.name + " score = " + str(self.second_player.score))
        input(". . .")

        sort_hand_value(self.active_player.hand)
        sort_hand_value(self.nonactive_player.hand)
        sort_hand_value(self.crib.cards)

        print("\n")  # active player show hand and count points in it
        cprint(self.active_player.name + "'s hand:", "yellow")
        self.active_player.show_hand_counting()
        self.count_hand(self.active_player)
        print(self.active_player.name + " score = " + str(self.active_player.score))
        input(". . .")

        print("\n")  # nonactive player show hand and count point in it
        cprint(self.nonactive_player.name + "'s hand:", "yellow")
        self.nonactive_player.show_hand_counting()
        self.count_hand(self.nonactive_player)
        print(self.nonactive_player.name + " score = " + str(self.nonactive_player.score))
        input(". . .")

        self.active_player.empty_hand()  # return hand cards to deck
        self.nonactive_player.empty_hand()

        print("\n")  # add cards from crib to nonactive player hand and count points in hand
        cprint(self.nonactive_player.name + "'s crib:", "yellow")
        self.nonactive_player.crib_hand()
        self.nonactive_player.show_hand_counting()
        self.count_hand(self.nonactive_player)
        print(self.nonactive_player.name + " score = " + str(self.nonactive_player.score))
        self.nonactive_player.empty_hand()
        input(". . .")
        print("\n")

        print("\n")
        print("End Round")
        print(self.first_player.name + " score = " + str(self.first_player.score))
        print(self.second_player.name + " score = " + str(self.second_player.score))
        input(". . .")

        self.deck.empty_cut()  # return cut to deck
        self.deck.shuffle()

        if self.first_player.active:  # switch active and nonactive player
            self.first_player.active = False
            self.second_player.active = True
        else:
            self.first_player.active = True
            self.second_player.active = False
