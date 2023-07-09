import random

gamerbank = 100
dealerbank = 100
choise = [0, 0, 0]
choiseperc = [0, 0, 0]

for i in range(10000):
    bet = random.choices([random.randint(1, min([gamerbank, dealerbank]) // 3),
                                  random.randint(min([gamerbank, dealerbank])//3 + 1, 2 * min([gamerbank, dealerbank]) // 3),
                                  random.randint(2 * min([gamerbank, dealerbank]) // 3 + 1, min([gamerbank, dealerbank]))],
                                 weights=[50, 33, 17], k=1)[0]
    if bet in range(1, min([gamerbank, dealerbank]) // 3 + 1):
        choise[0] += 1
    elif bet in range(min([gamerbank, dealerbank])//3 + 1, 2 * min([gamerbank, dealerbank]) // 3 + 1):
        choise[1] += 1
    elif bet in range(2 * min([gamerbank, dealerbank]) // 3 + 1, min([gamerbank, dealerbank]) + 1):
        choise[2] += 1
    choiseperc = list(map(lambda x: round(100 * x / sum(choise), 5), choise))
    print(bet, choiseperc)

