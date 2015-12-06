import random

class Deck:
  def __init__(self, cards = ()):
    self.deck = [card for card in cards]

  def Contains(self, card):
    return card in self.deck

  def Size(self):
    return len(self.deck)

  def Empty(self):
    return self.Size() == 0

  # Removes a card off the top or a specific card, and returns it.
  def Draw(self, card = None):
    if self.Empty():
      raise Exception('Cannot draw. Deck is empty.')
    if not card:
      return self.deck.pop(0)
    if not self.Contains(card):
      raise Exception('Cannot draw specific card. Deck does not contain.')
    self.deck.remove(card)
    return card

  # put cards on end of deck
  def Append(self, *cards):
    for card in cards:
      self.deck.append(card)

  def Shuffle(self):
    random.seed()
    random.shuffle(self.deck)
