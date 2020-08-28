
import random
import itertools
from termcolor import cprint


def find_card_name(card_list, name):
    for card in card_list:
        if card.name.lower() == name.lower():
            return card
    return None


def in_value_list(card_list, value):
    for card in card_list:
        if card.value == value:
            return card


def sort_hand_value(card_list):
    return card_list.sort(key=lambda x: x.run_value)


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

    def show_deck(self):  # displays cards in deck
        for c in self.cards:
            c.show()

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

    def number_of_cards(self):  # to make sure cards aren't being lost somewhere
        print("cards in deck:")
        print(len(self.cards))


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
            self.crib.cards.append(discard2)
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

        def discard_ai_medium():
            keep_hand_value = -10
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
            cprint(self.hand, "blue")
            cprint(keep_hand, "yellow")
            self.crib.cards.extend(c for c in self.hand if c not in keep_hand)
            self.hand = keep_hand.copy()

        def discard_ai_advanced():  # add scoring from aces and 5's
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
            cprint(self.hand, "blue")
            cprint(keep_hand, "yellow")
            self.crib.cards.extend(c for c in self.hand if c not in keep_hand)
            self.hand = keep_hand.copy()

        if self.p_type == 0:
            discard_player()

        if self.p_type == 1:
            discard_ai_easy()

        if self.p_type == 2:
            discard_ai_medium()

        if self.p_type == 3:
            discard_ai_advanced()

    def discard_phase(self):
        if self.p_type == 0:
            cprint(self.name + "'s hand:", "yellow")  # active draw and discard
        else:
            cprint(self.name + " discard", "yellow")
        self.draw_hand()  # might want to just have player1 draw/discard first every round?
        sort_hand_value(self.hand)
        #if self.p_type == 0:  @@@@@@@@@@@@@@@@@@@@@@
        self.show_hand()
        self.discard()
        print("\n")

    def empty_hand(self):  # return cards to deck and delete cards in hand
        self.deck.cards.extend(self.hand[0:4])
        self.hand.clear()

    def crib_hand(self):  # put all the cards from the crib into a players hand and count the points in hand
        for c in self.crib.cards:
            self.hand.append(c)
        self.crib.cards.clear()


class Crib:  # just a holding place for the crib hand

    def __init__(self):
        self.cards = []

    def show_crib(self):  # useless functionality
        for c in self.cards:
            c.show()


class Game:  # environment for the game, global var/objects should be available here

    def __init__(self, first_player, second_player, deck, crib):
        self.first_player = first_player  # reference for the players in the game
        self.second_player = second_player
        self.assign_active()
        self.deck = deck
        self.crib = crib
        self.active_player = None  #determines the order of the game sequence, determined below
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
            print("\n\n\n\n\n\n\n")
            self.play_card()
            self.reset_count()
        self.clean_up()
        print("\n")

    def play_card(self):  # playing card
        player = None
        if self.turn:  # self.turn = true means active player just played, false means nonactive player just played
            player = self.nonactive_player
        else:
            player = self.active_player

        player.playable_card = False  # Does player have playable card
        for card in player.hand:
            if self.count + card.value <= 31:
                player.playable_card = True

        def display():
            if player.p_type == 0:
                if not player.first_go:  # displays counting information
                    print("current count: ", end="")
                    cprint(str(self.count), "red", attrs=['bold'])
                    print("played cards:")
                    for c in self.sequence:
                        cprint("(" + str(c.description) + ") ", "cyan", end="")
                    print("\n")
                    cprint(player.name + " cards in hand:", "yellow")
                    player.show_hand()
                else:
                    cprint(player.name, "yellow")
            else:
                if not player.first_go:
                    print("current count: ", end="")
                    cprint(str(self.count), "red", attrs=['bold'])
                    print("played cards:")
                    for c in self.sequence:
                        cprint("(" + str(c.description) + ") ", "cyan", end="")
                    print("\n")
                    cprint(player.name + " cards in hand:", "yellow")
                    print(len(player.hand))
                else:
                    cprint(player.name, "yellow")

        def choose_check_play():
            if player.p_type == 0:  # human player
                play = find_card_name(player.hand, input("choose a card to play: "))
                if play:
                    if self.count + play.value > 31:  # is the chosen card a playable card?
                        print("choose a card that doesn't make the count go over 31")
                        choose_check_play()  # if not, go back to input
                        return
                else:  # player didn't input a card name correctly
                    print("input error")
                    choose_check_play()  # go back to input
                    return
            elif player.p_type == 1:  # easy_ai choosing method
                while True:
                    play = random.choice(player.hand)
                    if self.count + play.value <= 31:
                        print("Easy AI play:")
                        play.show()
                        break
            elif player.p_type == 2:  # medium_ai choosing method
                highest_value_play = -10
                play = Card(None, 0, None, 0)
                for card in player.hand:
                    if card.value + self.count <= 31:
                        play_value = 0
                        sequence_copy = self.sequence.copy()
                        count_copy = self.count
                        pair_counter_copy = self.pair_counter
                        sequence_copy.append(card)
                        count_copy += card.value
                        if count_copy == 15:
                            play_value += 2
                        if count_copy == 31:
                            play_value += 2
                        if len(sequence_copy) > 1:
                            if sequence_copy[-1].run_value == sequence_copy[-2].run_value:
                                pair_counter_copy += 1
                            if pair_counter_copy == 1:
                                play_value += 2
                            if pair_counter_copy == 2:
                                play_value += 6
                            if pair_counter_copy == 3:
                                play_value += 12

                        def calc_runs(seq):  # function for calculating runs
                            reversed_seq = []
                            run_length = 0

                            for d in reversed(seq):
                                reversed_seq.append(d.run_value)
                                if len(reversed_seq) > 2:
                                    sorted_list = reversed_seq.copy()
                                    sorted_list.sort()
                                    first_num = sorted_list[0]
                                    run = all((value - index) == first_num for index, value in enumerate(sorted_list))
                                    if run:
                                        run_length = len(sorted_list)
                            return run_length

                        countable_run = calc_runs(sequence_copy)  # scoring runs
                        if countable_run >= 3:
                            play_value += countable_run

                        if play_value > highest_value_play:
                            highest_value_play = play_value
                            play = card
                        elif play_value == highest_value_play:
                            if card.value > play.value:
                                play = card
                print("Medium AI play:")
                play.show()

            else:  # advanced ai
                if self.count == 0:
                    play = None
                    play = in_value_list(player.hand, 4)
                    if not play:
                        play = in_value_list(player.hand, 3)
                    if not play:
                        play = in_value_list(player.hand, 2)
                    if not play:
                        if in_value_list(player.hand, 9) and in_value_list(player.hand, 6):
                            play = in_value_list(player.hand, 9)
                    if not play:
                        if in_value_list(player.hand, 8) and in_value_list(player.hand, 7):
                            play = in_value_list(player.hand, 8)
                    if not play:
                        if in_value_list(player.hand, 10) and in_value_list(player.hand, 5):
                            play = in_value_list(player.hand, 10)
                    if not play:
                        play = in_value_list(player.hand, 9)
                    if not play:
                        play = in_value_list(player.hand, 8)
                    if not play:
                        play = in_value_list(player.hand, 7)
                    if not play:
                        play = in_value_list(player.hand, 6)
                    if not play:
                        play = in_value_list(player.hand, 10)
                    if not play:
                        play = in_value_list(player.hand, 1)
                    if not play:
                        play = in_value_list(player.hand, 5)

                else:
                    highest_value_play = -10
                    play = Card(None, 0, None, 0)
                    for card in player.hand:
                        cprint(card.description, "yellow")  #@@@@@@@@@@@@@2
                        if card.value + self.count <= 31:
                            play_value = 0
                            sequence_copy = self.sequence.copy()
                            count_copy = self.count
                            pair_counter_copy = self.pair_counter
                            sequence_copy.append(card)
                            count_copy += card.value
                            if count_copy == 15:
                                play_value += 2.1  # want this to be better than playing a pair
                            if count_copy == 31:
                                play_value += 2
                            if len(sequence_copy) > 1:
                                if sequence_copy[-1].run_value == sequence_copy[-2].run_value:
                                    pair_counter_copy += 1
                                if pair_counter_copy == 1:
                                    play_value += 2
                                if pair_counter_copy == 2:
                                    play_value += 6
                                if pair_counter_copy == 3:
                                    play_value += 12

                            def calc_runs(seq):  # function for calculating runs
                                reversed_seq = []
                                run_length = 0

                                for d in reversed(seq):
                                    reversed_seq.append(d.run_value)
                                    if len(reversed_seq) > 2:
                                        sorted_list = reversed_seq.copy()
                                        sorted_list.sort()
                                        first_num = sorted_list[0]
                                        run = all((value - index) == first_num for index, value in enumerate(sorted_list))
                                        if run:
                                            run_length = len(sorted_list)
                                return run_length

                            countable_run = calc_runs(sequence_copy)  # scoring runs
                            if countable_run >= 3:
                                play_value += countable_run
                            if play_value == 0:
                                if card.run_value in (self.sequence[-1].run_value + 2, self.sequence[-1].run_value + 1, self.sequence[-1].run_value -1, self.sequence[-1].run_value - 2):
                                    play_value -= 1
                                if count_copy == 21:
                                    play_value -= 1
                            cprint(play_value, "red")  # @@@@@@@@@@@@
                            if play_value > highest_value_play:
                                highest_value_play = play_value
                                play = card
                            elif play_value == highest_value_play:
                                if card.value > play.value:
                                    play = card

                print("Advanced AI play:")
                play.show()
            self.count += play.value  # what actually happens once card is chosen
            player.void.append(play)
            self.sequence.append(play)
            player.hand.remove(play)
            if self.count == 15:
                self.give_points(player, 2)
                print(player.name + " 15 for 2")
            if self.count == 31:
                self.give_points(player, 2)
                print(player.name + " 31 for 2")
            if len(self.sequence) > 1:
                if self.sequence[-1].run_value == self.sequence[-2].run_value:
                    self.pair_counter += 1
                else:
                    self.pair_counter = 0
                if self.pair_counter == 1:
                    self.give_points(player, 2)
                    print(player.name + " pair for 2")
                if self.pair_counter == 2:
                    self.give_points(player, 6)
                    print(player.name + " three of a kind for 6")
                if self.pair_counter == 3:
                    self.give_points(player, 12)
                    print(player.name + " four of a kind for 12")

            def calc_runs(seq):  # function for calculating runs
                reversed_seq = []
                run_length = 0

                for d in reversed(seq):
                    reversed_seq.append(d.run_value)
                    if len(reversed_seq) > 2:
                        sorted_list = reversed_seq.copy()
                        sorted_list.sort()
                        first_num = sorted_list[0]
                        run = all((value - index) == first_num for index, value in enumerate(sorted_list))
                        if run:
                            run_length = len(sorted_list)
                return run_length

            countable_run = calc_runs(self.sequence)  # scoring runs
            if countable_run >= 3:
                self.give_points(player, countable_run)
                print(player.name + " run of " + str(countable_run) + " for " + str(countable_run))

        display()
        if player.playable_card:  # if player has playable card, execute the play card function
            choose_check_play()

            if player == self.active_player:  # once card is played, last_play reflects the last card played
                self.last_play = True
            else:
                self.last_play = False

            if not self.turn:  # send turn to other player
                self.turn = True
            else:
                self.turn = False

        else:  # if player doesn't have a playable card, no card is played and turn is passed
            print("go")
            player.first_go = True
            if not self.turn:
                self.turn = True
            else:
                self.turn = False

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
        print("\n")

        self.active_player.discard_phase()
        self.nonactive_player.discard_phase()

        print("\n")  # get the cut and check nibs
        deck1.cut()
        self.nibs()

        self.counting_sequence()

        print("\n")
        print(self.first_player.name + " score = " + str(self.first_player.score))
        print(self.second_player.name + " score = " + str(self.second_player.score))

        sort_hand_value(self.active_player.hand)
        sort_hand_value(self.nonactive_player.hand)
        sort_hand_value(self.crib.cards)

        print("\n")  # active player show hand and count points in it
        cprint(self.active_player.name + "'s hand:", "yellow")
        self.active_player.show_hand_counting()
        self.count_hand(self.active_player)
        print(self.active_player.name + " score = " + str(self.active_player.score))

        print("\n")  # nonactive player show hand and count poitn in it
        cprint(self.nonactive_player.name + "'s hand:", "yellow")
        self.nonactive_player.show_hand_counting()
        self.count_hand(self.nonactive_player)
        print(self.nonactive_player.name + " score = " + str(self.nonactive_player.score))

        self.active_player.empty_hand()  # return hand cards to deck
        self.nonactive_player.empty_hand()

        print("\n")  # add cards from crib to nonactive player hand and count points in hand
        cprint(self.nonactive_player.name + "'s crib:", "yellow")
        self.nonactive_player.crib_hand()
        self.nonactive_player.show_hand_counting()
        self.count_hand(self.nonactive_player)
        print(self.nonactive_player.name + " score = " + str(self.nonactive_player.score))
        self.nonactive_player.empty_hand()
        print("\n")

        print("\n")
        print("End Round")
        print(self.first_player.name + " score = " + str(self.first_player.score))
        print(self.second_player.name + " score = " + str(self.second_player.score))

        self.deck.empty_cut()  # return cut to deck
        self.deck.shuffle()

        if self.first_player.active:  # switch active and nonactive player/mb make this a function?
            self.first_player.active = False
            self.second_player.active = True
        else:
            self.first_player.active = True
            self.second_player.active = False


deck1 = Deck()

crib1 = Crib()


player_1 = Player("Intermediate Computer 1", deck1, 0, crib1, 2, None)
player_2 = Player("Expert Computer 2", deck1, 0, crib1, 3, None)
game1 = Game(player_1, player_2, deck1, crib1)

player_1_wins = 0
player_2_wins = 0

i = 0
while i < 100:
    print("deck1 cards number")
    print(len(deck1.cards))
    game1.winner = None
    game1.first_player.score = 0
    game1.second_player.score = 0
    while game1.winner is None:
        game1.round()
    if game1.winner == player_1:
        player_1_wins += 1
    if game1.winner == player_2:
        player_2_wins += 1
    print("expert computer wins: ")
    print(player_2_wins)
    print("intermediate computer wins: ")
    print(player_1_wins)
    i += 1

print("expert computer wins: ")
print(player_2_wins)
print("intermediate computer wins: ")
print(player_1_wins)

sort_hand_value(deck1.cards)
for card in deck1.cards:
    print(card.name)




