#removed password from code

from random import shuffle
from ProbDist import PoiBin
import random
from operator import itemgetter

import pymysql
import sys
import time


#how much weight each specific match has. 32 is used in chess
kFactor = 90


class Standings:
    def __init__(self, teams):
        self.teams = teams
    def sortStandings(self, conference):
        point_sorted = {}
        for elem in self.teams:
            if elem.conference == conference:
                point_sorted[elem] = 2*elem.win  + elem.otl
        return (sorted(point_sorted.items(), key=itemgetter(1), reverse =True))
    def pointsToMakePlayoffs(self, conference):
        point_sorted = self.sortStandings(conference)
        return point_sorted[0][0]

    def getIndexInStandings(self, team):
        count = 0
        for elem in self.sortStandings(team.conference):
            if(elem[0] == team.name):
                break;
            else:
                count= count+1
        return count
    def getScheduleProbability(self, team, schedule):
        list = []
        for elem in schedule:
            list.append(EloCalculator.winPercentageBetween(team, elem))
        return list
    def getPlayoffProbability(self, team):
        team_competing= self.pointsToMakePlayoffs(team.conference)

        neededpoints = (team_competing.win * 2 + team_competing.otl)
        currentpoints = 2*team.win + team.otl


        ppg_top = neededpoints/team_competing.gamesplayed
        points_end = neededpoints+ppg_top*(82-team_competing.gamesplayed)
        ppg_needed = (points_end - currentpoints)/(82-team.gamesplayed)

        schedule = team.schedule
        schedule_perc = self.getScheduleProbability(team, schedule)

        print(schedule_perc)
        func = PoiBin(schedule_perc)
        print(int(len(schedule_perc)*(ppg_needed/2)))
        print(func.pmf(int(len(schedule)*(ppg_needed/2))))

        print("need pts", ppg_needed)
    def ifWin(self, team1, team2):
        current_points = team1.win * 2 + team1.otl
        new_points = current_points+2

        team_competing= self.pointsToMakePlayoffs(team1.conference)

        neededpoints = (team_competing.win * 2 + team_competing.otl)


        ppg_top = neededpoints/team_competing.gamesplayed
        points_end = neededpoints+ppg_top*(82-team_competing.gamesplayed)
        ppg_needed = (points_end - new_points)/(82-team1.gamesplayed)
        ppg_prev = (points_end - current_points) / (82 - team1.gamesplayed)

        schedule = team1.schedule
        schedule_perc = self.getScheduleProbability(team1, schedule)

        print(schedule_perc)
        func = PoiBin(schedule_perc)
        print(func.pmf(int(len(schedule)*(ppg_needed/2))))
        print(func.pmf(int(len(schedule)*(ppg_needed/2) -1 )))


def calculateElo(eloteam1, eloteam2, result):
	kFactor = 64
	list = []
	#if result = 0, Team1 wins
	#if result = 1, Team2 wins
	#if result = 2, Team1 overtime loss
	#if result = 3, Team2 overtime loss
	transformation1 = pow(10, eloteam1/400)
	transformation2 = pow(10, eloteam2/400)
	expectedscore = transformation1/(transformation1 + transformation2)
	if(result == 1):
		adjustment = 1
		eloteam1 += kFactor * (adjustment - expectedscore)
		eloteam2 -= kFactor * (adjustment - expectedscore)
	elif(result == 0):
		adjustment = 0
		eloteam1 -= kFactor * (adjustment - expectedscore)
		eloteam2 += kFactor * (adjustment - expectedscore)
	elif(result ==2):
		eloteam1 -= kFactor * (.5 - expectedscore)
		eloteam2 += kFactor * (1 - expectedscore)
	else:
		eloteam1 += kFactor * (.5 - expectedscore)
		eloteam2 -= kFactor * (1 - expectedscore)
	list.append(eloteam1)
	list.append(eloteam2)
	return list
	
def winPercentageBetween(team1elo, team2elo):
	winpercentage = team1elo / (team1elo + team2elo)
	return winpercentage
	
def getPlayoffProbability(playoffpoints, playoffgamesplayed, schedule, teampoints, teamgamesplayed, teamelo):
	#playoff points: 8th highest in the conference of the team
	#playoff gamesplayed: 8th highest num of gamesplayed
	#schedule: ***FUTURE*** list of elo values for remaining games in season ex. [1050, 1060, 1007, 1100]
			#current elo values for the future schedule
	#points : current points of team
	#teamgamesplayed: num of games played for team
	#elo: elo of team

	playoff_pointsneeded = (82-playoffgamesplayed)*(playoffpoints/playoffgamesplayed) + playoffpoints
	if(82-teamgamesplayed > 0 ):
		my_ppg = (playoff_pointsneeded-teampoints)/(82-teamgamesplayed)
	elif(82-teamgamesplayed == 0 and playoffpoints < teampoints):
		return 1.0
	else:
		return 0.0
	
	print(playoff_pointsneeded-teampoints)
	print(82-teamgamesplayed)

	schedule_perc = []
	for elem in schedule:
		schedule_perc.append(EloCalculator.winPercentageBetween(teamelo, elem))

	func = PoiBin(schedule_perc)

	print(my_ppg)
	print(int(len(schedule_perc)*(my_ppg/2)))
	if(my_ppg < 2):
		winperc = func.pmf(int(len(schedule_perc)*(my_ppg/2)))
	else:
		winperc = 0

	return winperc 
	
class TeamToChange:
    def __init__(self,name, ELO):
        self.name = name
        self.ELO = ELO	
	def printTeam(self):
		print self.name, self.ELO
		
def main():
	start_time = time.time()

	data=[]
	data.append("CAR")
	data.append("CBJ")
	data.append("NJD")
	data.append("NYI")
	data.append("NYR")
	data.append("PHI")
	data.append("PIT")
	data.append("WSH")
	
	data.append("BOS")
	data.append("BUF")
	data.append("DET")
	data.append("FLA")
	data.append("MTL")
	data.append("OTT")
	data.append("TBL")
	data.append("TOR")
	
	data.append("CHI")
	data.append("COL")
	data.append("DAL")
	data.append("MINN")
	data.append("NSH")
	data.append("STL")
	data.append("WPG")
	
	data.append("ANA")
	data.append("ARI")
	data.append("CGY")
	data.append("EDM")
	data.append("LAK")
	data.append("SJS")
	data.append("VAN")
	
	
	months=[]
	months.append("Oct")
	months.append("Nov")
	months.append("Dec")
	months.append("Jan")
	months.append("Feb")
	months.append("Mar")
	months.append("Apr")
	
	dates=[]
	year = "\'\'16"
	for mon in months:
		i=0
		if mon == "Jan":
			year = "\'\'17"
		while i < 31:
			i+=1
			if i < 10:
				gamedate = mon + " 0" + str(i) + " " + year
			else:
				gamedate = mon + " " + str(i) + " " + year
			dates.append(gamedate)
	
	try:
		#print "trying pymysql connection..."
		#con = pymysql.connect(host="localhost", user="root", passwd="!PASSWORD", db="NHL")  
		cur = con.cursor()
		time.sleep(1)
		
		for d in dates:
			records=[]
			teams_to_update=[]
			for dat in data:
				sql = "SELECT team_self,game_date,game_outcome,opponent,record,overtime_shootout FROM " + dat + " WHERE game_date='"+ d + "'"
				cur.execute(sql)
				records.append(cur.fetchall())
			
			for record in records:
				for rec in record:
					team_self = rec[0]
					if team_self =="MIN":
						team_self = "MINN"
					game_date = rec[1]
					game_outcome = rec[2]
					opponent = rec[3]
					if opponent =="MIN":
						opponent = "MINN"
					current_record = rec[4]
					overtime_shootout = rec[5]
					
					sql="SELECT elo FROM current_standings WHERE name_abbreviation='" + team_self + "' OR name_abbreviation='" + opponent + "'"
					cur.execute(sql)
					game_elos = cur.fetchall()
					team_one_elo = (game_elos[0])[0]
					team_two_elo = (game_elos[1])[0]
					
					#if result = 0, Team1 wins
					#if result = 1, Team2 wins
					#if result = 2, Team1 overtime loss
					#if result = 3, Team2 overtime loss
					if (game_outcome == "W" and overtime_shootout == ""):
						result = 0
					elif(game_outcome == "W" and overtime_shootout != ""):
						result = 3
					elif(game_outcome == "L"):
						result = 1
					elif(game_outcome == "O"):
						result = 2
						
					elo_list = calculateElo(team_one_elo, team_two_elo, result)
					
					for t in data:
						if(t == team_self):
							teams_to_update.append(TeamToChange(t, elo_list[0]))
							
							
			for teamssss in teams_to_update:
				sql="UPDATE current_standings SET elo="+str(teamssss.ELO)+" WHERE name_abbreviation='"+ teamssss.name+"'"
				cur.execute(sql)
			
		con.commit()
		if con:
			con.close()
	except pymysql.DatabaseError, e:
		print 'Error %s' % e    
		sys.exit(1)
	
	#get all team records?
	#go through each date and calculate_elo, remove 
	
	print("--- %s seconds ---" % (time.time() - start_time))
	
	
if __name__ == "__main__": main()
"""
def main():
    team2 = Team([], 0,"Islanders", "Metro", "East", 0, 0, 0, 1000)
    team3 = Team([], 0,"Blackhawks", "Metro", "West", 0, 0, 0, 1000)
    team1 = Team([team2, team3, team3, team2, team3, team2], 0, "Stars", "Metro", "East", 0,0,0,1000)

    listprob = [.47, .50, .50]
    func  = PoiBin(listprob)
    print(func.pmf(2))
    gamelength = 10

    #Stars win, Isles lose
    playGame(team3, team1)
    for index in range(10):
        playGame(team1, team2)

    teams = {team1, team2, team3}
    standing = Standings(teams)
    sorted = standing.sortStandings("East")
    print(standing.pointsToMakePlayoffs("East").win)
    standing.getPlayoffProbability(team1)

    print("playoff impact")
    standing.ifWin(team1, team2)
    #for index in range(gamelength):
    #    print("GAME ", index)
    #    print("win %", teams[0].winPercentageBetween(teams[1]))
    #    playGame(teams[0], teams[1])
    #    shuffle(teams)
    #    print("--------------")




if __name__ == "__main__": main()
"""
