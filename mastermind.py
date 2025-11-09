from os import system, name
from random import sample, choices
from termcolor import colored


class Game:
    def __init__(self):
        self.round = 9
        self.answer = []
        self.decoding_board = self.init_decoding_board()
        self.score_board = self.init_score_board()

    # decoding_board[round #][col #]
    def init_decoding_board(self) -> list[list]:
        return [["-" for _col in range(4)] for _row in range(10)]

    # key_board[round #][black_peg, white_peg]
    def init_score_board(self) -> list[list]:
        return [["-" for _col in range(2)] for _row in range(10)]

    def generate_answer(self, repeat):
        if repeat:
            self.answer = choices(Pegs().valid_colors, k=4)
        else:
            self.answer = sample(Pegs().valid_colors, 4)

    def set_guess(self, guess):
        self.decoding_board[self.round] = list(guess)

    def set_score(self, black, white):
        self.score_board[self.round] = [black, white]

    def won(self) -> bool:
        try:
            return self.score_board[self.round + 1][0] == 4
        except IndexError:
            return False

    def lost(self) -> bool:
        return self.round < 0


class Pegs:
    def __init__(self):
        self.termcolor_lookup = {
            "r": "red",
            "g": "green",
            "b": "blue",
            "p": "magenta",
            "y": "yellow",
            "w": "white",
        }
        self.valid_colors = list(self.termcolor_lookup.keys())


def handle_input(game):
    while True:
        guess = input().lower().replace(" ", "")
        if len(guess) == 4 and all(color in Pegs().valid_colors for color in guess):
            game.set_guess(guess)
            break
        elif guess == "quit" or guess == "q":
            quit()
        else:
            print("Pick 4 colors from list.")


def check_ans(game):
    black_peg = 0
    white_peg = 0
    ans = game.answer.copy()
    guess = game.decoding_board[game.round].copy()

    # check for correct color correct spot
    for i, _ in enumerate(ans):
        if ans[i] == guess[i]:
            ans[i] = ""
            guess[i] = ""
            black_peg += 1

    # check for correct color incorrect spot
    for color in guess:
        if color != "" and color in ans:
            ans.remove(color)
            white_peg += 1

    game.set_score(black_peg, white_peg)


def color_text(text_list) -> list:
    if all(letter.isalpha() and letter in Pegs().valid_colors for letter in text_list):
        return [
            colored(letter, Pegs().termcolor_lookup[letter]) for letter in text_list
        ]
    else:
        return text_list


def menu_screen(game):
    while True:
        print("Select a gamemode.")
        print("Press 1 for no repeating colors.")
        print("Press 2 to allow repeating colors.")
        print("Type 'quit' to exit.")
        choice = input()

        if choice == "1":
            game.generate_answer(False)
            break
        elif choice == "2":
            game.generate_answer(True)
            break
        elif choice == "quit" or choice == "q":
            quit()


def game_screen(game):
    # draw the board
    print("      Guess            Score     ")
    for i, row in enumerate(game.decoding_board):
        print("|", end="   ")
        print(*color_text(row), sep="  ", end="   ")
        print("|   Bl:", game.score_board[i][0], " W:", game.score_board[i][1])
        print()

    # draw the text
    print("Guess 4 colors: ")
    print("Color Options:", *color_text(Pegs().valid_colors))
    print("Bl: # of correct colors in correct spot")
    print("W: # of correct colors in incorrect spot")
    # print(game.answer) # debug


def clear_screen():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def main():
    clear_screen()
    game = Game()
    menu_screen(game)

    while game.round >= -1:
        clear_screen()
        game_screen(game)

        if game.won():
            print("Winner!")
            break

        if game.lost():
            print("Loser!")
            print("The answer was:", *color_text(game.answer))
            break

        handle_input(game)
        check_ans(game)
        game.round -= 1

    input("Press Enter")


while True:
    main()
