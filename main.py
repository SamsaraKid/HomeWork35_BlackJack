import random

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        if str(val).isdigit():
            self.price = val
        elif val == 'Т':
            self.price = 11
        else:
            self.price = 10

    def showcard(self):
        print('\t', self.suit, self.val)

class Koloda:
    #cards = []
    suits = ['\u2664', '\u2665', '\u2666', '\u2667']
    nums = ['Т', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'В', 'Д', 'К']
    def __init__(self):
        self.cards = []
        for s in self.suits:
            for n in self.nums:
                self.cards.append(Card(s, n))
        self.fold = []

    def showdeck(self):
        for c in self.cards:
            c.showcard()

    def shuffle(self):
        self.cards.extend(self.fold)
        random.shuffle(self.cards)

    def minuscard(self):
        return self.cards.pop()

    def plusfold(self, cards):
        self.fold.extend(cards)

class Player:
    def __init__(self, name, type):
        self.name = name
        self.hand = []
        self.sum = 0
        self.bank = 100
        self.type = type  # тип игрока: 'human', 'dealer'
        self.stat = ''  # тип результата: 'Блэкджэк', 'Перебор', 'Больше', 'Меньше', 'Ничья'

    def showhand(self):
        for card in self.hand:
            card.showcard()

    def showhandgraph(self):
        for i in range(len(self.hand)):
            print('\t╭─────╮', end='')
        print()
        for i in range(len(self.hand)):
            print(f'\t│{str(self.hand[i].val).ljust(5)}│', end='')
        print()
        for i in range(len(self.hand)):
            print(f'\t│  {self.hand[i].suit}\u2009\u2009\u2009\u2009\u2009\u2009│', end='')
        print()
        for i in range(len(self.hand)):
            print(f'\t│{str(self.hand[i].val).rjust(5)}│', end='')
        print()
        for i in range(len(self.hand)):
            print('\t╰─────╯', end='')
        print()

    def showsum(self):
        print('\tСумма карт =', self.sum)

    def takecard(self, deck, num=1):
        for i in range(num):
            self.hand.append(deck.minuscard())
            self.sum += self.hand[-1].price

    def fold(self, deck):
        deck.plusfold(self.hand)
        self.hand = []
        self.sum = 0
        self.stat = ''


def turn(gamer, deck):
    gamer.takecard(deck)
    print('\tКарты игрока', gamer.name)
    gamer.showhandgraph()
    gamer.showsum()
    if gamer.sum == 21:
        gamer.stat = 'блэкджэк'
    elif gamer.sum > 21:
        gamer.stat = 'перебор'
    else:
        if gamer.type == 'human':
            match int(input('Ещё карту?\n1 - да\n2 - нет\n')):
                case 1: turn(gamer, deck)
                case _: return
        else:
            if gamer.sum <= 16:
                print('Дилер берёт ещё карту')
                turn(gamer, deck)
            else:
                return


name = input('Начнём игру. Введите ваше имя:\n')
player1 = Player(name, type='human')
player2 = Player('Компьютер', type='comp')
dealer1 = Player('Дилер', type='dealer')
deck1 = Koloda()
deck1.shuffle()
bet = 0

while True:

    if len(deck1.cards) < 18:
        deck1.shuffle()
    player1.takecard(deck1)
    dealer1.takecard(deck1)
    print('\tКарта игрока', player1.name)
    player1.showhandgraph()
    player1.showsum()
    while True:
        bet = int(input(f'Сделайте ставку\n'
                        f'Ваш банк:    {player1.bank}\n'
                        f'Банк казино: {dealer1.bank}\n'))
        if bet > player1.bank:
            print('Вы не можете себе столько позволить')
        elif bet > dealer1.bank:
            print('Казино не может ответить на вашу ставку')
        elif bet == 0:
            print('Ставка не может быть нулевой')
        else:
            player1.bank -= bet
            dealer1.bank -= bet
            break

    turn(player1, deck1)

    if player1.stat == 'блэкджэк':
        print(f'У вас {player1.stat}. Вы выиграли')
    elif player1.stat == 'перебор':
        print(f'У вас {player1.stat}. Вы проиграли')

    if player1.stat == '':
        turn(dealer1, deck1)
        if dealer1.stat == '':
            if dealer1.sum > player1.sum:
                dealer1.stat = 'больше'
                player1.stat = 'меньше'
            elif dealer1.sum < player1.sum:
                dealer1.stat = 'меньше'
                player1.stat = 'больше'
            else:
                dealer1.stat = 'ничья'
                player1.stat = 'ничья'

        if dealer1.stat in ['блэкджэк', 'больше']:
            print(f'У Дилера {dealer1.stat}. Выигрывает казино')
        elif dealer1.stat in ['перебор', 'меньше']:
            print(f'У Дилера {dealer1.stat}. Казино проиграло')
        else:
            print(f'В результате {dealer1.stat}')

    if player1.stat in ['блэкджэк', 'больше'] or dealer1.stat in ['перебор', 'меньше']:
        player1.bank += bet * 2
    elif dealer1.stat in ['блэкджэк', 'больше'] or player1.stat in ['перебор', 'меньше']:
        dealer1.bank += bet * 2
    else:
        player1.bank += bet
        dealer1.bank += bet

    bet = 0
    player1.fold(deck1)
    dealer1.fold(deck1)

    if player1.bank == 0:
        print('Вы проигрались')
        break
    elif dealer1.bank == 0:
        print('Вы обыграли казино')
        break
    elif int(input('Играем ещё?\n1 - да\n2 - нет\n')) != 1:
        break




# def comp_take_card():
#     if comp.sum < 11 or (11 <= comp.sum <= 19 and random.choices([True, False], weights=[20-comp.sum, comp.sum-10], k=1)[0]):
#         comp.takecard(deck)
#         print(comp.name, 'взял карту')
#         return True
#     else:
#         print(comp.name, 'отказался от добора')
#         return False
#
