import itertools
import random

import cards.constants

class Card:
  def __init__(self, name, suit):
    self.name = name
    self.suit = suit
    self.Hide()

  def Reveal(self):
    self.hidden = False
  def Hide(self):
    self.hidden = True

  def Name(self):
    return self.name
  def Suit(self):
    return self.suit

  # Returns name and suit if card is revealed. Else return None.
  def Check(self):
    if self.hidden:
      return None
    return self.name, self.suit

  def ToString(self):
    return '{} of {}'.format(self.name, self.suit)


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


class DeckManager:
  def __init__(self):
    self.unused = Deck((Card(n, s) for n, s in itertools.product(
      cards.constants.STANDARD_CARDS, cards.constants.STANDARD_SUITS)))
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
