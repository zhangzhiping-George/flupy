import collections
Cards = collections.namedtuple('Cards', ['rank', 'suit'])
class FrenchDeck:
    ranks = list(range(2, 11)) + list('JQKA')
    suits = 'Diamonds Hearts Clubs Spades'.split()
    def __init__(self): #
        self._cards = [Cards(rank, suit) for rank in self.ranks
                                  for suit in self.suits]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, pos):
        return self._cards[pos]
    def __setitem__(self, pos, card):
        self._cards[pos] = card 

deck = FrenchDeck()
print(len(deck))
print(deck[0])
