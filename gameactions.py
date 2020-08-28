
from termcolor import cprint
import random
from deck import Card


def find_card_name(card_list, name):
    for card in card_list:
        if card.name.lower() == name.lower():
            return card
    return None


def in_value_list(card_list, value):
    for card in card_list:
        if card.value == value:
            return card


def calc_runs(seq):
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


def play_card(self):
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
                    print("Easy Computer play:")
                    play.show()
                    break
        elif player.p_type == 2:  # intermediate_ai choosing method
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

                    countable_run = calc_runs(sequence_copy)  # scoring runs
                    if countable_run >= 3:
                        play_value += countable_run

                    if play_value > highest_value_play:
                        highest_value_play = play_value
                        play = card
                    elif play_value == highest_value_play:
                        if card.value > play.value:
                            play = card
            print("Intermediate Computer play:")
            play.show()

        else:  # expert ai
            if self.count == 0:
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

                        countable_run = calc_runs(sequence_copy)  # scoring runs
                        if countable_run >= 3:
                            play_value += countable_run
                        if play_value == 0:
                            if card.run_value in (self.sequence[-1].run_value + 2, self.sequence[-1].run_value + 1,
                                                  self.sequence[-1].run_value - 1, self.sequence[-1].run_value - 2):
                                play_value -= 1
                            if count_copy == 21:
                                play_value -= 1
                        if play_value > highest_value_play:
                            highest_value_play = play_value
                            play = card
                        elif play_value == highest_value_play:
                            if card.value > play.value:
                                play = card

            print("Expert Computer play:")
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


