import random
import time


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
        self.fold = []
        random.shuffle(self.cards)

    def minuscard(self):
        return self.cards.pop()

    def plusfold(self, cards):
        self.fold.extend(cards)


class Player:
    def __init__(self, name, type):
        self.name = name
        self.hand = []
        self.sum = 0      # сумма карт игрока
        self.bank = 100   # банк игрока
        self.type = type  # тип игрока: 'human', 'dealer', 'comp'
        self.stat = ''    # тип результата: 'блэкджэк', 'перебор', 'больше', 'меньше', 'ничья'

    def showhand(self):
        for card in self.hand:
            card.showcard()

    # графический вывод карт игрока
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

    # показать сумму карт
    def showsum(self):
        print('\tСумма карт =', self.sum)

    # взять карту и сразу прибавить сумму
    def takecard(self, deck, num=1):
        for i in range(num):
            self.hand.append(deck.minuscard())
            self.sum += self.hand[-1].price

    # сброс карт игрока в отбой
    def fold(self, deck):
        deck.plusfold(self.hand)
        self.hand = []
        self.sum = 0
        self.stat = ''

# функция хода игрока или дилера
def turn(gamer, deck):
    print(f'{gamer.name} берёт ещё карту')
    gamer.takecard(deck)
    print('\tКарты игрока', gamer.name)
    gamer.showhandgraph()
    gamer.showsum()
    if gamer.sum == 21:
        gamer.stat = 'блэкджэк'
    elif gamer.sum > 21:
        gamer.stat = 'перебор'
    else:
        # человек сам решает, брать ли ещё карту
        if gamer.type == 'human':
            match int(input('Ещё карту?\n1 - да\n2 - нет\n')):
                case 1: turn(gamer, deck)
                case _: return
        # если у компьютера меньше 11, то он точно берёт карту
        # если у него от 11 до 19, то чем больше, тем меньше вероятность, что он возьмёт карту
        # при 11 вероятность 90%, при 19 - 10%, шаг 10%
        elif gamer.type == 'comp':
            print(f'{gamer.name} думает...')
            time.sleep(3)
            if gamer.sum < 11 or (11 <= gamer.sum <= 19 and random.choices([True, False], weights=[20-gamer.sum, gamer.sum-10], k=1)[0]):
                turn(gamer, deck)
            else:
                print(f'{gamer.name} отказался брать карту')
                return
        # дилер берёт карту если не больше 16
        else:
            if gamer.sum <= 16:
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
shift = False

while True:

# Подготовка игры
    # выбираем, кто будет играть кон, игрок-компьютер или игрок-человек
    if shift:
        gamer = player2
    else:
        gamer = player1

    # перемешиваем колоду, если в ней осталось меньше трети карт
    if len(deck1.cards) < 18:
        deck1.shuffle()
        print('Отбой вернулся в колоду. Колода была перемешана')

    # раздача начальных карт
    print('Ход игрока', gamer.name)
    gamer.takecard(deck1)
    if not dealer1.hand:
        dealer1.takecard(deck1)
    print('\tКарта игрока', gamer.name)
    gamer.showhandgraph()
    gamer.showsum()

# Ставки
    if gamer.type == 'human':
        while True:
            bet = int(input(f'Сделайте ставку\n'
                            f'Ваш банк:        {player1.bank}\n'
                            f'Банк Компьютера: {player2.bank}\n'
                            f'Банк казино:     {dealer1.bank}\n'))
            if bet > gamer.bank:
                print('Вы не можете себе столько позволить')
            elif bet > dealer1.bank:
                print('Казино не может ответить на вашу ставку')
            elif bet == 0:
                print('Ставка не может быть нулевой')
            else:
                gamer.bank -= bet
                dealer1.bank -= bet
                break
    # компьютер делает ставку не больше своего банка и банка казино
    # если это число больше 3, то допустимый диапазон ставок делится на три равных диапазона
    # (малая, средняя и большая ставка), внутри каждого генерируется случайное число
    # и выбирается одно из трёх с вероятностями 50%, 33% и 17% соответственно
    # если в банке у компьютера или дилера осталось не больше 3, то просто случайное от 1 до 3
    else:
        minbank = min([gamer.bank, dealer1.bank])
        if minbank > 3:
            bet = random.choices([random.randint(                   1,     minbank // 3),
                                  random.randint(    minbank // 3 + 1, 2 * minbank // 3),
                                  random.randint(2 * minbank // 3 + 1,     minbank)],
                                 weights=[50, 33, 17], k=1)[0]
        else:
            bet = random.randint(1, minbank)
        gamer.bank -= bet
        dealer1.bank -= bet
        print(f'{gamer.name} думает...')
        time.sleep(3)
        print('Компьютер ставит', bet)

# Ход игрока
    turn(gamer, deck1)

# Вывод результата и зачисление выигрыша если после хода игрока уже всё ясно. Дилер при этом не ходит
    if gamer.stat == 'блэкджэк':
        print(f'У игрока {gamer.name} {gamer.stat}. Выигрыш')
        gamer.bank += bet * 2
    elif gamer.stat == 'перебор':
        print(f'У игрока {gamer.name} {gamer.stat}. Проигрыш')
        dealer1.bank += bet * 2

# Если после хода игрока результата нет, то ходит дилер.
# Если у дилера не блэкджэк и не перебор, сравниваем его результат с игроком
    if gamer.stat == '':
        turn(dealer1, deck1)
        if dealer1.stat == '':
            if dealer1.sum > gamer.sum:
                dealer1.stat = 'больше'
            elif dealer1.sum < gamer.sum:
                dealer1.stat = 'меньше'
            else:
                dealer1.stat = 'ничья'

# Выводим результат и зачисляем выигрыш после хода дилера
        if dealer1.stat in ['блэкджэк', 'больше']:
            print(f'У Дилера {dealer1.stat}. Выигрывает казино')
            dealer1.bank += bet * 2
        elif dealer1.stat in ['перебор', 'меньше']:
            print(f'У Дилера {dealer1.stat}. Казино проиграло')
            gamer.bank += bet * 2
        else:
            print(f'В результате {dealer1.stat}')
            gamer.bank += bet
            dealer1.bank += bet

# Сбрасываем ставку, сбрасываем карты игрока в отбой
# Карты дилера сбрасываются, если он их раскрывал
    bet = 0
    gamer.fold(deck1)
    if dealer1.stat != '':
        dealer1.fold(deck1)

    print(f'Ваш банк:        {player1.bank}\n'
          f'Банк Компьютера: {player2.bank}\n'
          f'Банк казино:     {dealer1.bank}\n')
    print(f'В колоде осталось {len(deck1.cards)} карт (колода перемешается когда останется меньше 18 карт)')

# Проверяем, не проигрался ли кто-то из трёх участников игры
    if gamer.bank == 0:
        print(f'Игрок {gamer.name} проигрался')
        if gamer.type == 'human':
            break
    elif dealer1.bank == 0:
        print('Казино обанкротилось')
        break
    elif int(input(f'Играем дальше? Следующий кон игрока {[player2.name, player1.name][int(shift)]}\n1 - да\n2 - нет\n')) != 1:
        print('Всего доброго. Ждём вас снова')
        break

# Переключаемся между игроком-компьютером и игроком-человеком для следующего кона
# Если игрок-компьютер проигрался, он больше не участвует
    if player2.bank != 0:
        shift = not shift
    else:
        shift = False

