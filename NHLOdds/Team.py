from random import shuffle
from ProbDist import PoiBin

#how much weight each specific match has. 32 is used in chess
kFactor = 50

class Team:
    def __init__(self, name, win, loss, otl, ELO):
        self.name = name
        self.win = win
        self.loss = loss
        self.otl = otl
        self.ELO = ELO
    def recalculateElo(self, otherTeam, result):
        #result: 1- you win, 0 - other team wins, 2 - tie
        transformation1 = pow(10, self.ELO/400)
        transformation2 = pow(10, otherTeam.ELO/400)
        expectedscore = transformation1/(transformation1 + transformation2)
        if(result == 1):
            adjustment = 1
            self.win += 1
        elif(result == 0):
            adjustment = 0
            self.loss += 1
        else:
            adjustment = .5
            self.otl += 1

        self.ELO += kFactor * (adjustment - expectedscore)
    def winPercentageBetween(self, team2):
        if __name__ == '__main__':
            winpercentage = self.ELO/(self.ELO + team2.ELO)
        return winpercentage
    def printElo(self):
        print(self.name, " : ", self.win, " - ", self.loss, " =  ", self.ELO)

def playGame(winner, loser):
    winner.recalculateElo(loser, 1)
    loser.recalculateElo(winner, 0)

    winner.printElo()
    loser.printElo()

def main():
    team1 = Team("Stars",0,0,0,1000)
    team2 = Team("Islanders", 0, 0, 0, 1000)

    teams = []
    teams.append(team1)
    teams.append(team2)
    listprob = [.47, .50, .30]
    func  = PoiBin(listprob)
    print(func.pmf(2))
    gamelength = 10

    #Stars win, Isles lose
    #playGame(team1, team2)

    #for index in range(gamelength):
    #    print("GAME ", index)
    #    print("win %", teams[0].winPercentageBetween(teams[1]))
    #    playGame(teams[0], teams[1])
    #    shuffle(teams)
    #    print("--------------")




if __name__ == "__main__": main()