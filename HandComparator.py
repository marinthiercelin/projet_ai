from enum import Enum
import Deck

class Hand(Enum):
    high_card = 1
    pair = 2
    two_pair = 3
    three_of_a_kind = 4
    straight = 5
    flush = 6
    full_house = 7
    four_of_a_kind = 8
    straight_flush = 9
    royal_flush = 10

deck_suits = Deck.suits

class HandComparator(object):

    def get_hand(self, cards):
        unzipped = zip(*cards)
        ranks = unzipped[0]
        suits = unzipped[1]
        dup = self.is_duplicate(cards)
        flush = self.is_flush(cards)
        straight = self.is_straight(ranks)





    def is_duplicate(self, cards):
        def get_duplicates(c):
            tmp = dict()
            for card in c:
                rank = card[0]
                if rank in tmp:
                    tmp[rank].append(card)
                else:
                    tmp[rank] = [card]
            duplicates = dict()
            for i in tmp:
                if len(tmp[i]) > 1:
                    duplicates[i] = tmp[i]

            return duplicates.values()

        duplicates = get_duplicates(cards) #Alwas sorted from lowest card to highest
        #Case where there a no duplicates
        if len(duplicates) == 0:
            return False, None, None

        #Case where there is only one group of duplicates
        elif len(duplicates) == 1:
            tmp = duplicates[0]
            if len(tmp) == 2:
                return True, Hand.pair, tmp
            elif len(tmp) == 3:
                return True, Hand.three_of_a_kind, tmp
            else:
                return True, Hand.four_of_a_kind, tmp

        #Case where there are two groups of duplicates
        elif len(duplicates) == 2:
            low, high = duplicates[0], duplicates[1]

            if len(high) + len(low) > 5: #Handles 4 of a kinds, or double three of a kind (Very improbable)
                if len(high) == 3 and len(low) == 3:
                    return True, Hand.full_house, high + low[0:2]
                elif len(high) == 4:
                    return True, Hand.four_of_a_kind, high
                else: #Case where low is a four of a kind
                    return True, Hand.four_of_a_kind, low
            else:
                if len(high) == 2 and len(low) == 2: #Two Pair
                    return True, Hand.two_pair, high + low
                elif len(high) == 3 and len(low) == 2: #Full house with the higher cards
                    return True, Hand.full_house, high + low
                else: #Full house with the lower cards
                    return True, Hand.full_house, low + high

        #Case where there are 3 duplicates (Improbable)
        else:
            low, med, high = duplicates[0], duplicates[1], duplicates[2]
            if len(low) + len(med) + len(high) == 6: #Case where there are 3 pairs
                return True, Hand.two_pair, high + med
            else: #Case where there is 1 three of a kind and 2 pairs => Full-House
                if len(low) == 3:
                    return True, Hand.full_house, low + high
                elif len(med) == 3:
                    return True, Hand.full_house, med + high
                else:
                    return True, Hand.full_house, high + med

    #Returns (True, Suit, cards) if the current hand contains a flush in the given suit and (False, None, None) else
    def is_flush(self, cards):
        flush_cards = []
        for suit in deck_suits:
            tmp = [card for card in cards if card[1] == suit]
            if len(cards) >= 5:
                flush_cards = sorted(tmp, key=lambda x: x[0], reverse=True)[0:5]
                break

        if not flush_cards: #Equivalent to flush_cards == []
            return False, None, None
        else:
            return True, flush_cards[0][1], flush_cards

    #Returns (True, card_ranks) if the current hand contains a straight up to the given rank
    def is_straight(self, ranks):
        ordered_set_ranks = sorted(list(set(ranks)), reverse=True)
        if len(ordered_set_ranks) < 5:
            return False, None
        else:
            consecutive_cards = [ordered_set_ranks[0]]
            for i in xrange(1, len(ordered_set_ranks)):

                if ordered_set_ranks[i] == (consecutive_cards[-1] - 1):
                    consecutive_cards.append(ordered_set_ranks[i])
                else:
                    if len(consecutive_cards) < 5:
                        consecutive_cards = [ordered_set_ranks[i]]

            if len(consecutive_cards) >= 5:
                return True, consecutive_cards[0:5]
            else:
                return False, None


d = HandComparator()
e = [(13,"Spades"), (1, "clubs"), (2,"Hearts"), (2, "Spades"), (5,"Diamonds"), (13, "Spades"), (1,"Hearts")]
print d.is_duplicate(e)

