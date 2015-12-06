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
