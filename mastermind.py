
from os import system, name
from random import seed, sample, choices
from termcolor import colored


class Game:
    def __init__(self):
        self.color_dict = {
            "r": "red",
            "g": "green",
            "b": "blue",
            "p": "magenta",
            "y": "yellow",
            "w": "white"
        }
        self.colors = list(self.color_dict.keys())
        self.round = 9
        self.answer = []
        self.guess_board = self.init_guess_board()
        self.score_board = self.init_score_board()

    # decoding_board[round #][col #]
    def init_guess_board(self) -> list[list]:
        return [["-" for col in range(4)] for row in range(10)]
    
    # key_board[round #][black_peg, white_peg]
    def init_score_board(self) -> list[list]:
        return [["-" for col in range(2)] for row in range(10)]

    def set_guess(self, guess):
        self.guess_board[self.round] = list(guess)

    def set_score(self, black, white):
        self.score_board[self.round] = [black, white]

    def in_colors(self, guess) -> bool:
        for i in guess:
            if i not in self.colors:
                return False
        return True

    def won(self) -> bool:
        try:
            return self.score_board[self.round + 1][0] == 4
        except IndexError:
            return False


def clear_screen():
    if name == 'nt': 
        _ = system('cls')
    else:
        _ = system('clear')


def select_gamemode(game):
    while True:
        print("Select a gamemode.")
        print("Press 1 for no repeating colors.")
        print("Press 2 to allow repeating colors.")
        print("Type 'quit' to exit.")
        choice = input()

        seed()
        if choice == "1":
            game.answer = sample(game.colors, 4)
            break  
        elif choice == "2":
            game.answer = choices(game.colors, k=4)           
            break
        elif choice == "quit":
            quit()


def get_input(game):
    while True:
        guess = input().lower().replace(' ', '')

        if len(guess) == 4 and game.in_colors(guess):
            game.set_guess(guess)
            break
        else:
            print("Pick 4 colors from list.")


def check_ans(game):
    black_peg = 0
    white_peg = 0
    ans = game.answer.copy()
    guess = game.guess_board[game.round].copy()

    # check for correct color correct spot
    for index, _ in enumerate(ans):
        if ans[index] == guess[index]:
            ans[index] = ""
            guess[index] = ""
            black_peg += 1

    # check for correct color incorrect spot
    for i in guess:
        if i != "" and i in ans:
            ans.remove(i)
            white_peg += 1

    game.set_score(black_peg, white_peg)


def add_color(game, text_list) -> list:
        if text_list[0].isalpha():
            return [colored(letter, game.color_dict[letter]) for letter in text_list]
        else:
            return text_list


def draw_screen(game):
    # draw the board
    for i, row in enumerate(game.guess_board):
        print("|", end="   ")
        print(*add_color(game, row), sep="  ", end="   ")
        print("|   Bl:", game.score_board[i][0], " W:", game.score_board[i][1])
        print()

    # draw the text
    print("Guess 4 colors: ")
    print("Colors:", *add_color(game, game.colors))


def main():
    while True:
        clear_screen()
        game = Game()
        select_gamemode(game)

        while game.round >= -1:
            clear_screen()
            draw_screen(game)

            if game.won():
                print("Winner!")
                break

            if game.round == -1:
                print("Loser!")
                print("The answer was:", *add_color(game, game.answer))
                break
            
            get_input(game)
            check_ans(game)
            game.round -= 1

        input("Press Enter")


main()
