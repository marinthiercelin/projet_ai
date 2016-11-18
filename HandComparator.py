
import Deck

deck_suits = Deck.suits

class HandComparator(object):

    def get_hand(self, cards):
        unzipped = zip(*cards)
        ranks = unzipped[0]
        suits = unzipped[1]

    #Returns (True, Suit) if the current hand contains a flush in the given suit and (False, 0) else
    def is_flush(self, suits):
        for i in deck_suits:
            if suits.count(i) >= 5:
                return (True, i)

        return (False, 0)

    #Returns (True, Rank) if the current hand contains a straight up to the given rank
    def is_straight(self, ordered_set_ranks):
        if len(ordered_set_ranks) < 5:
            return (False, 0)
        else:
            consecutive_cards = [ordered_set_ranks[0]]
            for i in xrange(1, len(ordered_set_ranks)):
                if ordered_set_ranks[i] == consecutive_cards[-1] + 1:
                    consecutive_cards.append(ordered_set_ranks[i])
            if len(consecutive_cards) >= 5:
                return (True, consecutive_cards[-1])
            else:
                return (False,0)



