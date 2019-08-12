import numpy as np
import random
from collections import Counter
import matplotlib.pyplot as plt

class turn():
    def __init__(self, rolls = [], hots = [], score = 0, verbose = False):
        self.rolls = rolls
        self.hots = set(hots)
        self.score = score
        self.hots_payoff = {1: 1000, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}
        self.bust = False
        self.remove = []
        self.verbose = verbose
  
    def __repr__(self):
        return "roll: %s, removed: %s, hots: %s, score: %d" %(self.rolls,
     self.remove, self.hots, self.score)  
    
    def reset_roll(self, hots = []):
        self.rolls = []
        self.hots = set(hots)

    def roll_em(self):
        if (not self.rolls):
            self.rolls = [0, 0, 0, 0, 0, 0]
        for i in range(len(self.rolls)):
            self.rolls[i] = random.randint(1, 6)
        self.rolls.sort()
    
    def special_rolls(self):
        if (self.rolls[0] == self.rolls[1] == self.rolls[2] and self.rolls[3] == self.rolls[4] == self.rolls[5]
            and not self.rolls[0] == self.rolls[3]):
            self.score += 2500

        elif (self.rolls[0] == self.rolls[1] and self.rolls[2] == self.rolls[3] 
              and self.rolls[4] == self.rolls[5] 
              and len(set([self.rolls[0], self.rolls[2], self.rolls[4]])) == 3):
            self.score += 750

        elif (self.rolls[0] == 1 and self.rolls[1] == 2 and self.rolls[2] == 3 
              and self.rolls[3] == 4 and self.rolls[4] == 5 and self.rolls[5] == 6):
            self.score += 1500
        
        else: return
            
        self.remove = self.rolls
        self.reset_roll()
    
    def take_hots(self):
        if (self.hots):
            self.remove += [x for x in self.rolls if x in self.hots]
            self.rolls[:] = [x for x in self.rolls if not x in self.hots]
            self.hots = set(self.remove)
            self.score += sum([self.hots_payoff[x] for x in self.remove])

        if (not self.rolls):
            return

        [hots] = Counter(self.rolls).most_common(1)
        
        if (hots[1] > 2):
            self.score += (np.count_nonzero(np.array(self.rolls) == hots[0]) - 2) * self.hots_payoff[hots[0]]
            self.hots.add(hots[0])
            self.remove += [x for x in self.rolls if x == hots[0]]
            self.rolls[:] = [x for x in self.rolls if not x == hots[0]]

    def take_iv(self):
        if (not self.rolls):
            return
        
        ones = np.count_nonzero(np.array(self.rolls) == 1)
        fives = np.count_nonzero(np.array(self.rolls) == 5)
        
        if (ones + fives == len(self.rolls)):
            self.remove += self.rolls
            self.score += 100*ones + 50*fives
            if (len(self.remove) > ones + fives):
                self.reset_roll(hots = self.hots)
            else:
                self.reset_roll()
        
        elif (not self.remove or len(self.rolls)<3):
            
            for i, a in enumerate(self.rolls):
                if (a == 1):
                    self.score += 100
                    self.remove.append(a)
                    self.rolls.pop(i)
                    if (len(self.rolls)>2):
                        break
                elif (a == 5):
                    self.score += 50
                    self.remove.append(a)
                    self.rolls.pop(i)
                    if (len(self.rolls)>2):
                        break
            if (not self.remove):
                if (self.verbose):
                    print("roll: %s, you Busted, your turn is over!" % (self.rolls))
                self.bust = True
            
    def take(self):
        self.remove = []
        self.rolls.sort()
        if (len(self.rolls) == 6):
            self.special_rolls()
        self.take_hots()
        self.take_iv()
        if (not self.bust and self.verbose):
            print(my_turn)

score = []
for i in range(10000):
    my_turn = turn(rolls = [1, 1, 5, 5, 3], score = 100)
    my_turn.take()
    while not my_turn.bust:
        my_turn.roll_em()
        my_turn.take()
    score.append(my_turn.score)

print("\nExpected value of your roll: %s \nThe 10th, 20th, ..., 90th percentile scores: %s\n" 
    %(np.mean(score), np.percentile(score, [10, 20 , 30, 40, 50, 60, 70, 80, 90])))

if ([1]):
    n, bins, patches = plt.hist(score, 50)
    plt.yscale("log")
    plt.grid(True)
    plt.show()
'''
my_turn = turn(rolls = [4, 1, 1, 5], score = 3250, verbose=True)
my_turn.take()
'''