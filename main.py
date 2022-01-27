import random
import matplotlib.pyplot as plt

class ScoreStrategy:
    def __init__(self):
        self.counts = [[0 for x in range(19)] for i in range(6)]
        self.MAXNUM = None

    def append(self, other):
        other.sort()
        for i in range(len(other)):
            n = other[i]
            self.counts[i][n] += 1

    def __str__(self):
        for x in self.counts:
            print(x)

    def plot(self):
        self.freq = [[ self.counts[i][x]/sum(self.counts[i]) for x in range(19)] for i in range(6)]
        plt.figure(figsize = (10, 5), dpi = 100)
        for x in self.freq:
            plt.plot(x, label = f'Maximum Score: ({x.index(max(x))}, {max(x):.2f})')
            # annot_max(x, ax = plt)
        plt.xticks(range(0, 19, 2))
        x1,x2,y1,y2 = plt.axis()
        plt.axis((x1,x2,y1, y2+.1))
        plt.grid()
        plt.xlabel('Ability Score')
        plt.ylabel('Relative Frequency')
        plt.title(self.__class__.__name__)
        plt.legend(loc = 2)
        # plt.show()

    def simulate(self, N):
        for i in range(N):
            scores = self.rollfunc()
            if self.MAXNUM != None:
                while True:
                    if max(scores) >= self.MAXNUM:
                        scores = self.rollfunc()
                    else:
                        self.append(scores)
                        break
            else:
                self.append(scores)

class Roll4d6(ScoreStrategy):
    def rollfunc(self):
        scores = []
        for i in range(6):
            l = [random.randint(1, 6) for i in range(4)]
            l.sort()
            l.pop(0)
            scores.append(sum(l))
        return scores

class Reroll70(ScoreStrategy):
    def rollfunc(self):
        while True:
            scores = []
            for i in range(6):
                l = [random.randint(1, 6) for i in range(4)]
                l.sort()
                l.pop(0)
                scores.append(sum(l))
            if sum(scores) >= 70:
                return scores

class DropLowest(ScoreStrategy):
    def rollfunc(self):
        scores = []
        for i in range(7):
            l = [random.randint(1, 6) for i in range(4)]
            l.sort()
            l.pop(0)
            scores.append(sum(l))
        scores.sort()
        return scores[1:]

class PointBuy(ScoreStrategy):
    def rollfunc(self):
        POINTS = 27
        scores = [8, 8, 8, 8, 8, 8]
        while True:
            s = random.randint(0, 5)
            if scores[s] >= 13 and scores[s] <= 14 and POINTS > 2:
                scores[s] += 1
                POINTS -= 2
            elif scores[s] <= 12:
                scores[s] += 1
                POINTS -= 1

            if POINTS == 0:
                return scores

class RandomTTT(ScoreStrategy):
    def rollfunc(self):
        b = Board([[random.randint(1, 6) for x in range(3)] for y in range(3)])
        return b.getScores()

class MaxTTT(ScoreStrategy):
    def rollfunc(self):
        array = ([[None for i in range(3)] for i in range(3)])
        nums = [random.randint(1, 6) for x in range(9)]
        nums.sort()
        array[1][1] = nums.pop()
        array[0][0] = nums.pop()
        array[2][2] = nums.pop()
        array[2][0] = nums.pop()
        array[0][2] = nums.pop()
        array[0][1] = nums.pop()
        array[2][1] = nums.pop()
        array[1][0] = nums.pop()
        array[1][2] = nums.pop()
        b = Board(array)
        return b.getScores()

class TriangleTTT(ScoreStrategy):
    def rollfunc(self):
        array = ([[None for i in range(3)] for i in range(3)])
        nums = [random.randint(1, 6) for x in range(9)]
        nums.sort()
        array[1][1] = nums.pop()
        array[0][0] = nums.pop()
        array[0][2] = nums.pop()
        array[0][1] = nums.pop()
        array[2][0] = nums.pop()
        array[2][2] = nums.pop()
        array[2][1] = nums.pop()
        array[1][0] = nums.pop()
        array[1][2] = nums.pop()
        b = Board(array)
        return b.getScores()


class Board:
    def __init__(self, array):
        # array needs to be 2x2
        self.array = array

    def getScores(self):
        scores = [sum(self.array[x]) for x in range(3)]
        scores += [sum(self.array[x][y] for x in range(3)) for y in range(3)]
        scores.append(sum(self.array[x][x] for x in range(3)))
        scores.append(sum(self.array[x][2-x] for x in range(3)))
        scores.sort()
        return scores[2:]

def main():
    for c in ScoreStrategy.__subclasses__():
        x = c()
        x.simulate(100000)
        x.plot()
    plt.show()

if __name__ == '__main__':
    main()
