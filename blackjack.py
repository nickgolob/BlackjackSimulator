from constants import *

from cards.deck_manager import DeckManager
import player

class BlackJack:

  INITIAL_HAND_ID = 0

  def __init__(self):
    self.deck_manager = DeckManager()
    self.players = [player.BlackJackPlayer() for i in range(NUMBER_PLAYERS)]
    self.house = player.HousePlayer()

  def PrintResults(self):
    print('RESULTS:')
    for i, player in enumerate(self.players):
      print('Player {}: {}'.format(i, player.money))

  def GiveCard(self, player, hand_id):
    player.Receive(hand_id, self.deck_manager.Draw())
  def TakeCards(self, player):
    self.deck_manager.Discard(*player.ReclaimCards())

  def PlayTurn(self, player, hand_id):
    while player.Total(hand_id) <= 21:
      action = player.Act(hand_id, self.house.Showing())
      if action == HIT:
        self.GiveCard(player, hand_id)
      if action == STAND:
        return
      if action == SPLIT:
        hand = player.PopHand(hand_id)
        assert hand[0].Name() == hand[1].Name()
        player.Receive(hand_id, hand[0])
        self.PlayTurn(player, hand_id)
        while hand_id in player.GetHandIDs():
          hand_id += 1
        player.Receive(hand_id, hand[1])
        self.PlayTurn(player, hand_id)
        return
      if action == DOUBLEDOWN:
        self.GiveCard(player, hand_id)
        return

  def ReturnWinnings(self, player):
    house_total = self.house.Total(self.INITIAL_HAND_ID)
    for hand_id in player.GetHandIDs():
      hand_total = player.Total(hand_id)
      if hand_total <= 21:
        if house_total > 21 or house_total < hand_total:
          player.GiveWinnings(player.GetBet() * 2.0)
        elif house_total == hand_total:
          player.GiveWinnings(player.GetBet())

  def PlayRound(self):

    self.deck_manager.Reset()

    # reset / Get bets
    self.house.Reset()
    for player in self.players:
      player.Reset()
      player.SetInitialBet()

    # burn card
    self.deck_manager.Discard(self.deck_manager.Draw())

    # deal
    for i in range(2):
      for player in self.players:
        self.GiveCard(player, self.INITIAL_HAND_ID)
      self.GiveCard(self.house, self.INITIAL_HAND_ID)

    # check for dealer blackjack
    if self.house.Showing().Name() == ACE:
      for player in self.players:
        if player.BuyInsurance():
          # TODO implement
          pass
    if not self.house.Total(self.INITIAL_HAND_ID) == 21:
      # players go
      for player in self.players:
        if player.Total(self.INITIAL_HAND_ID) == 21:
          player.GiveWinnings(player.GetBet() * 2.5)
          self.TakeCards(player)
        else:
          self.PlayTurn(player, self.INITIAL_HAND_ID)
      # dealer go
      while self.house.Total(self.INITIAL_HAND_ID) < 17:
        self.GiveCard(self.house, self.INITIAL_HAND_ID)

    # distribute winnings, reclaim cards to discard
    for player in self.players:
      self.ReturnWinnings(player)
      self.TakeCards(player)
    self.TakeCards(self.house)

    return