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

    #Compares two given hands and returns the winning Hand or None if they are equal
    def compare_hands(self, hand1, hand2):
        if hand1 == hand2:
            return None

        if hand1[0].value > hand2[0].value:
            return hand1
        elif hand1[0].value < hand2[0].value:
            return hand2
        else: #Same hands, got to compare the cards
            cards1, cards2 = hand1[1], hand2[1]
            if cards1[0][0] > cards2[0][0]: #Compare first elements
                if cards2[0][0] != 1:
                    return hand1 #hand1 wins
                else:
                    return hand2 #hand2 wins
            elif cards1[0][0] < cards2[0][0]:
                if cards1[0][0] != 1: #Handles case of Ace
                    return hand2
                else:
                    return hand1
            else:
                ranks1, ranks2 = zip(*cards1)[0], zip(*cards2)[0] #Get the ranks of each hand
                diff = sorted(list(set(ranks1).symmetric_difference(set(ranks2))), reverse=True)

                if hand1[0] == Hand.two_pair: #got two pair
                    if ranks1[2] > ranks2[2]:
                        return hand1
                    elif ranks1[2] < ranks2[2]:
                        return hand2

                if len(diff) == 0:
                    return None

                elif diff[-1] == 1:
                    return hand1 if diff[-1] in ranks1 else hand2
                else:
                    max_card = diff[0]
                    return hand1 if max_card in ranks1 else hand2


    #Returns the hand which the cards represent (type, cards) generally, cards always has 5 cards
    def get_hand(self, cards):
        dup = self.is_duplicate(cards)
        flush = self.is_flush(cards)
        straight = self.is_straight(cards)

        if flush[0]: #Royal_Flush, Straight_flush, Flush
            return flush[1], flush[2]
        elif straight[0]: #Straight
            return Hand.straight, straight[1]
        elif dup[0]: #Pair, two
            complete_hand = self.complete_duplicate_hand(cards, dup[2])
            return dup[1], complete_hand
        else:
            sorted_cards = sorted(cards, key=lambda x: x[0], reverse=True)
            if sorted_cards[-1][0] == 1:
                sorted_cards = [sorted_cards[-1]] + sorted_cards[0:min(len(sorted_cards)-1, 4)]
            else:
                sorted_cards = sorted_cards[0:5]

            return Hand.high_card, sorted_cards

    #Completes pairs, two_pairs, three_of_a_kind, four_of_a_kind to a hand of 5 cards (size of hand)
    def complete_duplicate_hand(self, cards, duplicate):
        if len(duplicate) == 5 or len(cards) < 5: #Case of a full house
            return duplicate
        else:
            missing = 5 - len(duplicate)
            rest = sorted([card for card in cards if card not in duplicate], key=lambda x:x[0], reverse=True) # reverse sort of cards not involved in hand
            if rest[-1][0] == 1: #Takes care of aces
                rest = rest[-1:] + rest[0:-1]
            return duplicate + rest[0: missing]


    #This function classifies the flush (flush, Straight Flush and royal flush)
    #Problems are when to differentiate when an ace is a 1 or an ace
    def classify_flush(self, flush_cards, flush_suit):
        consecutive_cards = [flush_cards[0]]
        for card in flush_cards[1:]:
            if card[0] == consecutive_cards[-1][0] - 1:
                consecutive_cards.append(card)
            else:
                if len(consecutive_cards) < 4:
                    consecutive_cards = [card]

        if consecutive_cards[0] == (13, flush_suit) and (1, flush_suit) in flush_cards:  # Royal flush
            return Hand.royal_flush, [(1, flush_suit)] + consecutive_cards[0:4]
        elif len(consecutive_cards) >= 5:  # Straight flush
            return Hand.straight_flush, consecutive_cards[0:5]
        else:  # Flush
            return Hand.flush, flush_cards[0:5]

    #Return (True, type, cards) if the current hand contains a duplicate hand (pair, two pair, 3 of a kind, 4 of a kind, full House)
    #Cards is reverse sorted (Highest pair before)
    def is_duplicate(self, cards):
        #Returns a list and each element is a list of duplicates
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

        duplicates = sorted(get_duplicates(cards), key=lambda x: x[0][0]) #Alwas sorted from lowest card to highest
        #print duplicates

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

            if low[0][0] == 1: #Handles case of Aces
                tmp = high
                high = low
                low = tmp

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

            if low[0][0] == 1: #Handles case of Aces
                tmp2 = med
                med = high
                high = low
                low = tmp2

            if len(low) + len(med) + len(high) == 6: #Case where there are 3 pairs
                return True, Hand.two_pair, high + med
            else: #Case where there is 1 three of a kind and 2 pairs => Full-House
                if len(low) == 3:
                    return True, Hand.full_house, low + high
                elif len(med) == 3:
                    return True, Hand.full_house, med + high
                else:
                    return True, Hand.full_house, high + med

    #Returns (True, type,  cards) if the current hand contains a flush in the given suit and (False, None, None) else
    #Cards is reverse sorted (High to low)
    def is_flush(self, cards):
        flush_cards = []
        if len(cards) < 5:
            return False, None, None

        #Groups cards in suits
        for suit in deck_suits:
            tmp = [card for card in cards if card[1] == suit]
            if len(tmp) >= 5:
                flush_cards = sorted(tmp, key=lambda x: x[0], reverse=True)
                break


        if not flush_cards: #Equivalent to flush_cards == []
            return False, None, None
        else:
            flush_suit = flush_cards[0][1]
            type = self.classify_flush(flush_cards, flush_suit)

            return True, type[0], type[1]


    #Returns (True, straight) if the current hand contains a straight up to the given rank
    #card_ranks is reverse sorted (High to low)
    def is_straight(self, cards):
        #print cards
        if len(cards) < 5:
            return False, None

        cards_by_rank = dict(cards)
        ranks = cards_by_rank.keys()

        ordered_set_ranks = sorted(list(set(ranks)), reverse=True)
        if len(ordered_set_ranks) < 5:
            return False, None
        else:
            consecutive_cards = [ordered_set_ranks[0]]
            for i in xrange(1, len(ordered_set_ranks)):

                if consecutive_cards == [13, 12, 11, 10] and 1 in ordered_set_ranks: #Handles straight to Ace
                    return True, [(1, cards_by_rank[1])] + [(rank, cards_by_rank[rank]) for rank in consecutive_cards[0:4]]

                if ordered_set_ranks[i] == (consecutive_cards[-1] - 1):
                    consecutive_cards.append(ordered_set_ranks[i])
                else:
                    if len(consecutive_cards) < 5:
                        consecutive_cards = [ordered_set_ranks[i]]

            if len(consecutive_cards) >= 5:
                return True, [(rank, cards_by_rank[rank]) for rank in consecutive_cards[0:5]]
            else:
                return False, None


'''d = HandComparator()
deck = Deck.Deck()

cards2 = [(9,"Diamonds"), (9, "Spades")]
cards = [(11,"Spades"), (3,"Hearts")]
comm = [(13,"Hearts"), (13,"Diamonds"), (6,"Clubs"), (10,"Hearts"), (10, "Spades")]
h1 = d.get_hand(cards + comm)
h2 = d.get_hand(cards2 + comm)
print h1
print h2
print d.compare_hands(h1,h2)

for i in range(0,10):
    e = deck.get(7)
    f = deck.get(7)
    deck.restart()
    print e
    print f
    print d.compare_hands(e, f)
    print '\n'''

