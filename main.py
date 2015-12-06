import blackjack

from constants import *

def main():
  game = blackjack.BlackJack()
  for i in range(TOTAL_ROUNDS):
    game.PlayRound()
  game.PrintResults()

if __name__ == '__main__':
  main()