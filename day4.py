def process_card(card):
    card_number, winning_numbers, elf_numbers = card
    points = 0
    count = 0
    for elf_number in elf_numbers:
        if elf_number in winning_numbers:
            if points == 0:
                points = 1
            else:
                points *= 2
            count += 1
    return count, points


def score_cards(free_cards):
    total = 0
    cards_remaining = len(cards)
    card_index = 0
    while cards_remaining > 0:
        card = cards[card_index]
        count, points = process_card(card)
        total += points
        if free_cards:
            for i in range(card[0], card[0] + count):
                cards.append(cards[i])
                cards_remaining += 1
        cards_remaining -= 1
        card_index += 1
    return count, total


with open('day4.txt', 'rt') as f:
    lines = [line.strip() for line in f.readlines()]

cards = []
for line in lines:
    card_number, s1 = line.split(':')
    card_number = int(card_number.split()[1].strip())
    winning_numbers, elf_numbers = s1.split('|')
    winning_numbers = [int(n.strip()) for n in winning_numbers.split()]
    elf_numbers = [int(n.strip()) for n in elf_numbers.split()]
    cards.append((card_number, winning_numbers, elf_numbers))

# part 1
count, total = score_cards(False)
print(f'total: {total}')

# part 2
count, total = score_cards(True)
print(f'count: {len(cards)}')