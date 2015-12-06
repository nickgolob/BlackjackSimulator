from players.player import Player

class HousePlayer(Player):
  def Showing(self):
    assert len(self.hands) == 1
    for hand_id in self.hands:
      assert len(self.hands[hand_id]) == 2
      return self.hands[hand_id][1]

