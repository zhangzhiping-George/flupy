import collections
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JKQA')
    suits = 'spades diamonds clubs hearts'.split()
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, position):       
        return self._cards[position]
    
#deck = FrenchDeck()
#print 'len(deck): ', len(deck)

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
def spades_hight(card):
    return FrenchDeck.ranks.index(card.rank)*len(suit_values) + suit_values[card.suit]

card = FrenchDeck()
for card in sorted(card, key=spades_hight):
    print card
