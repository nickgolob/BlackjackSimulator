import itertools

import constants

from cards.card import Card
from cards.deck import Deck

class DeckManager:
  def __init__(self):
    self.unused = Deck((Card(n, s) for n, s in itertools.product(
      constants.STANDARD_CARDS, constants.STANDARD_SUITS)))
    self.discard, self.active = Deck(), Deck()
    self.Reset()

  # moves cards between decks
  def _move(self, source, dest, card):
    source.Draw(card)
    dest.Append(card)

  def _combine(self, dest, *sources):
    for source in sources:
      while not source.Empty():
        dest.Append(source.Draw())

  # move a card from unused to active
  def Draw(self):
    card = self.unused.Draw()
    self.active.Append(card)
    return card

  # move cards from unused or active to the Discard pile.
  def Discard(self, *cards):
    for card in cards:
      if not self.active.Contains(card) and not self.unused.Contains(card):
        raise Exception('Card not in play or unused')
      if self.active.Contains(card):
        self._move(self.active, self.discard, card)
      else:
        self._move(self.unused, self.discard, card)

  def Reset(self):
    self._combine(self.unused, self.discard, self.active)
    assert self.unused.Size() == 52
    self.unused.Shuffle()

