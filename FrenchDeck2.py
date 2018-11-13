import collections
Cards = collections.namedtuple('Cards', ['rank', 'suit'])

class FrenchDeck(collections.MutabelSequence):
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
    def __delitem__(self, pos):
        del self._cards[pos]
    def insert(self, pos, card):
        self._cards.insert(pos, card)

deck = FrenchDeck()
print(len(deck))
print(deck[0])
