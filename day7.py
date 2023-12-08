import sys


class HandBid:
    def __init__(self, cards, bid):
        self.hand = Hand(cards)
        self.bid = int(bid)

    def __lt__(self, other):
        return self.hand < other.hand

    def __eq__(self, other):
        return self.hand == other.hand

    def __str__(self):
        return f'{self.hand} bid: {self.bid}'

    def __repr__(self):
        return self.__str__()


class Hand:
    hand_types = ['5 of a kind', '4 of a kind', 'full house', '3 of a kind', '2 pair', '1 pair', 'high card']

    def __init__(self, cards):
        self.original_cards = None
        self.cards = list(cards)
        self.checks = [self.check_five_of_a_kind, self.check_four_of_a_kind, self.check_full_house,
                       self.check_three_of_a_kind, self.check_two_pair, self.check_one_pair, self.check_high_card]

    def get_type(self):
        for i, check in enumerate(self.checks):
            if check():
                return i
        print(f"should not happen. cards: {self.cards}")
        sys.exit()

    def check_five_of_a_kind(self):
        cards = self.cards
        return cards[0] == cards[1] == cards[2] == cards[3] == cards[4]

    def check_four_of_a_kind(self):
        cards = sorted(self.cards)
        return (cards[0] == cards[1] == cards[2] == cards[3]) or (cards[1] == cards[2] == cards[3] == cards[4])

    def check_full_house(self):
        cards = sorted(self.cards)
        return (cards[0] == cards[1]) and (cards[2] == cards[3] == cards[4]) \
            or (cards[0] == cards[1] == cards[2]) and (cards[3] == cards[4])

    def check_three_of_a_kind(self):
        cards = sorted(self.cards)
        return (cards[0] == cards[1] == cards[2]) \
            or (cards[1] == cards[2] == cards[3]) \
            or (cards[2] == cards[3] == cards[4])

    def check_two_pair(self):
        cards = sorted(self.cards)
        return ((cards[0] == cards[1]) and ((cards[2] == cards[3]) or (cards[3] == cards[4]))) \
            or ((cards[1] == cards[2]) and (cards[3] == cards[4]))

    def check_one_pair(self):
        cards = sorted(self.cards)
        return (cards[0] == cards[1]) \
            or (cards[1] == cards[2]) \
            or (cards[2] == cards[3]) \
            or (cards[3] == cards[4])

    def check_high_card(self):
        return True

    def upgrade_js(self):
        '''
        remove Js from cards
        create new Hands using same values as other cards in Hand or 'A'
        find best Hand
        replace cards with cards from best Hand
        '''
        self.original_cards = self.cards[:]
        if 'J' in self.cards:
            non_j_cards = set([c for c in self.cards if c != 'J'])
            non_j_cards.add('A')
            best_hand = None
            for non_j_card in non_j_cards:
                test_cards = [c if c != 'J' else non_j_card for c in self.cards]
                test_hand = Hand(test_cards)
                if best_hand:
                    if test_hand > best_hand:
                        best_hand = test_hand
                else:
                    best_hand = test_hand
            self.cards = best_hand.cards

    def __lt__(self, other):
        if not Hand.jwild:
            self.original_cards = self.cards
            other.original_cards = other.cards
        else:
            if not self.original_cards:
                self.upgrade_js()
            if not other.original_cards:
                other.upgrade_js()

        # a lower type is actually a higher rank
        self_type = self.get_type()
        other_type = other.get_type()
        if self_type > other_type:
            return True
        if self_type < other_type:
            return False
        if self_type == other_type:
            self_cards = self.original_cards
            other_cards = other.original_cards
            for i in range(len(self_cards)):
                if Hand.card_labels.find(self_cards[i]) > Hand.card_labels.find(other_cards[i]):
                    return True
                if Hand.card_labels.find(self_cards[i]) < Hand.card_labels.find(other_cards[i]):
                    return False
        print(f'cards {self_cards} are same!')
        sys.exit()

    def __str__(self):
        return f'{self.cards} {Hand.hand_types[self.get_type()]}'

    def __repr__(self):
        return self.__str__()


with open('day7.txt', 'rt') as f:
    lines = [line.strip() for line in f.readlines()]

for jwild in [False, True]:
    Hand.jwild = jwild
    Hand.card_labels = 'AKQT98765432J' if Hand.jwild else 'AKQJT98765432'

    hand_bids = []
    for line in lines:
        hand_bids.append(HandBid(line.split()[0].strip(), line.split()[1].strip()))
    hand_bids.sort()

    total = 0
    for i, hand_bid in enumerate(hand_bids):
        total += (i+1) * hand_bid.bid
    print(total)