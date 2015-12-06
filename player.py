from constants import *

class Player:
  def __init__(self):
    self.hands = {}
    self.soft_hand = False

  def Reset(self):
    assert not self.hands
    self.soft_hand = False

  def Receive(self, hand_id, *cards):
    if not hand_id in self.hands:
      self.hands[hand_id] = []
    for card in cards:
      self.hands[hand_id].append(card)

  def GetHandIDs(self):
    return self.hands.keys()

  def PopHand(self, hand_id):
    return self.hands.pop(hand_id)

  def ReclaimCards(self):
    for hand_id in self.hands:
      for card in self.hands[hand_id]:
        yield card
    self.hands = {}

  # Return the total of the players. Sets the soft_hand attribute
  def Total(self, hand_id):
    hand = self.hands[hand_id]
    sum = 0
    self.soft_hand = True
    for card in hand:
      if card.Name() == ACE:
        if self.soft_hand:
          sum += 1
        else:
          sum += 11
          self.soft_hand = True
      else:
        sum += BLACKJACK_VALUES[card.Name()]
    if self.soft_hand:
      if sum > 21:
        sum -= 10
        self.soft_hand = False
    return sum


class HousePlayer(Player):

  def Showing(self):
    assert len(self.hands) == 1
    for hand_id in self.hands:
      assert len(self.hands[hand_id]) == 2
      return self.hands[hand_id][1]

class BlackJackPlayer(Player):

  def __init__(self):
    super().__init__()
    self.money = 0

  def IsSplittable(self, hand_id):
    hand = self.hands[hand_id]
    if len(hand) != 2:
      return False
    return hand[0].Name() == hand[1].Name()

  def BuyInsurance(self):
    return False

  def SetInitialBet(self):
    self.money -= 1
    self.bet = 1
  def GetBet(self):
    return self.bet

  def Act(self, hand_id, dealerCard):  # returns an action
    dealer_total = BLACKJACK_VALUES[dealerCard.Name()]
    card_total = self.Total(hand_id)
    if self.soft_hand:
      if card_total in range(13, 18):
        return HIT
      if card_total in range(19, 21):
        return STAND
      if card_total == 18:
        if dealer_total in range(9, 11):
          return HIT
        else:
          return STAND
    if self.IsSplittable(hand_id):
      if self.hands[hand_id][0].Name() == ACE:
        return SPLIT
      elif card_total == 20:
        return STAND
      elif card_total == 18:
        if dealerCard.Name() in [SEVEN, *TENS, ACE]:
          return STAND
        return SPLIT
      elif card_total == 16:
        if not dealerCard.Name() in [*TENS, ACE]:
          return SPLIT
      elif card_total == 14:
        if dealerCard.Name() in [*TENS]:
          return STAND
        if not dealerCard.Name() in [EIGHT, NINE, ACE]:
          return SPLIT
      elif card_total == 12:
        if dealer_total in range(2, 7):
          return SPLIT
      elif card_total == 10:
        if dealer_total in range(2, 10):
          return DOUBLEDOWN
      elif card_total == 6:
        if dealer_total in range(4, 8):
          return SPLIT
      elif card_total == 4:
        if dealer_total in range(3, 8):
          return SPLIT
    else:
      if card_total >= 17:
        return STAND
      if card_total in range(13, 17):
        if dealer_total in range(2, 7):
          return STAND
      if card_total == 12:
        if card_total in range(4, 7):
          return STAND
      if card_total in range(10, 12):
        if dealer_total in range(2, 10):
          return DOUBLEDOWN
      if card_total == 9:
        if dealer_total in range(2, 7):
          return DOUBLEDOWN

    return HIT

  def GiveWinnings(self, winnings):
    self.money += winnings
