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
