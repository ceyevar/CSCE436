#create mysql tables for nhl app
import pymysql
import sys
import time
import getpass

def create_standing_tables(hostname,username,password,database):
	con = None
	try:
		con = pymysql.connect(host=hostname, user=username, passwd=password, db=database) 
		print "Opened database successfully"
		cur = con.cursor()
		tbname = 'current_standings'
		
		sql = """CREATE TABLE %s(current_ranking int, team_name varchar(20) PRIMARY KEY, name_abbreviation varchar(20), 
			games_played int, wins int, losses int, overtime int, points int, row int, goals_for int, goals_against int, 
			goal_differential int, home_record varchar(20), away_record varchar(20), shootout_record varchar(20), 
			last_ten_record varchar(20), streak varchar(20),last_game varchar(30), next_game varchar(30), division varchar(20), conference varchar(20), 
			ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, CONSTRAINT rank_division UNIQUE (current_ranking, division))""" % tbname
		cur.execute(sql)
		
		print "Table created successfully"
		con.commit()
		
	except pymysql.DatabaseError, e:
		if con:
			con.rollback()
		print "Error %s" % e
		sys.exit(1)
	
	finally:
		if con:
			con.close()
			
def create_team_tables(hostname,username,password,database):
	con = None
	try:
		con = pymysql.connect(host=hostname, user=username, passwd=password, db=database) 
		print "Opened database successfully"
		cur = con.cursor()
		
		#instead of full team names for tables, using abbreviations
		# data=[]
		# data.append("carolina_hurricanes")
		# data.append("columbus_bluejackets")
		# data.append("newjersey_devils")
		# data.append("newyork_islanders")
		# data.append("newyork_rangers")
		# data.append("philadelphia_flyers")
		# data.append("pittsburgh_penguins")
		# data.append("washington_capitals")
		
		# data.append("boston_bruins")
		# data.append("buffalo_sabres")
		# data.append("detroit_redwings")
		# data.append("florida_panthers")
		# data.append("montreal_canadiens")
		# data.append("ottawa_senators")
		# data.append("tampabay_lightning")
		# data.append("toronto_mapleleafs")
		
		# data.append("chicago_blackhawks")
		# data.append("colorado_avalanche")
		# data.append("dallas_stars")
		# data.append("minnesota_wild")
		# data.append("nashville_predators")
		# data.append("stlouis_blues")
		# data.append("winnipeg_jets")
		
		# data.append("annaheim_ducks")
		# data.append("arizona_coyotes")
		# data.append("calgary_flames")
		# data.append("edmonton_oilers")
		# data.append("losangeles_kings")
		# data.append("sanjose_sharks")
		# data.append("vancouver_canucks")
		
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
		
		
		for dat in data:
			sql = """CREATE TABLE %s(game_date varchar(20), home_road varchar(1), game_outcome varchar(1), 
			overtime_shootout varchar(2), opponent varchar(5), record varchar(20), goals_for int, goals_against int, power_play_goals int, power_play_opportunities int, power_play_goals_against int, 
			times_shorthanded int, shorthanded_goals_for int, shorthanded_goals_against int, shots_for int, shots_against int, attendence int, 
			winning_goalie varchar(20), winning_goal_scorer varchar(20), ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""" % dat
			cur.execute(sql)
		
		print "Tables created successfully"
		con.commit()
		
	except pymysql.DatabaseError, e:
		if con:
			con.rollback()
		print "Error %s" % e
		sys.exit(1)
	
	finally:
		if con:
			con.close()
			
def drop_all_standings_tables(hostname,username,password,database):
	con = None
	try:
		con = pymysql.connect(host=hostname, user=username, passwd=password, db=database) 
		print "Opened database successfully"
		cur = con.cursor() 

		cur.execute("DROP TABLE current_standings")

		con.commit()
		print "Table successfully deleted"

	except pymysql.DatabaseError, e:
		print 'Error %s' % e	
		sys.exit(1)
	
	
	finally:
		if con:
			con.close()
def drop_all_teams_tables(hostname,username,password,database):
	con = None
	try:
		con = pymysql.connect(host=hostname, user=username, passwd=password, db=database) 
		print "Opened database successfully"
		cur = con.cursor()
		
		# data=[]
		# data.append("carolina_hurricanes")
		# data.append("columbus_bluejackets")
		# data.append("newjersey_devils")
		# data.append("newyork_islanders")
		# data.append("newyork_rangers")
		# data.append("philadelphia_flyers")
		# data.append("pittsburgh_penguins")
		# data.append("washington_capitals")
		
		# data.append("boston_bruins")
		# data.append("buffalo_sabres")
		# data.append("detroit_redwings")
		# data.append("florida_panthers")
		# data.append("montreal_canadiens")
		# data.append("ottawa_senators")
		# data.append("tampabay_lightning")
		# data.append("toronto_mapleleafs")
		
		# data.append("chicago_blackhawks")
		# data.append("colorado_avalanche")
		# data.append("dallas_stars")
		# data.append("minnesota_wild")
		# data.append("nashville_predators")
		# data.append("stlouis_blues")
		# data.append("winnipeg_jets")
		
		# data.append("annaheim_ducks")
		# data.append("arizona_coyotes")
		# data.append("calgary_flames")
		# data.append("edmonton_oilers")
		# data.append("losangeles_kings")
		# data.append("sanjose_sharks")
		# data.append("vancouver_canucks")
		
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
		
		for dat in data:
			sql = "DROP TABLE %s" % dat
			cur.execute(sql)

		con.commit()
		print "Table successfully deleted"

	except pymysql.DatabaseError, e:
		print 'Error %s' % e	
		sys.exit(1)
	
	
	finally:
		if con:
			con.close()

def drop_table(hostname,username,password,database,tab):
	con = None
	try:
		con = pymysql.connect(host=hostname, user=username, passwd=password, db=database) 
		print "Opened database successfully"
		cur = con.cursor()
		sql = "DROP TABLE %s"
		cur.execute(sql, (tab,))
		
		con.commit()
		print "Table " +tab+ " has been deleted successfully"

	except pymysql.DatabaseError, e:
		print 'Error %s' % e	
		sys.exit(1)
	
	
	finally:
		if con:
			con.close()

def test_connection(hostname,username,password,database):
	con = None
	try:
		con = pymysql.connect(host=hostname, user=username, passwd=password, db=database) 
		print "Opened database successfully"
		
		con.commit()
		print "Connection terminated successfully"

	except pymysql.DatabaseError, e:
		print 'Error %s' % e	
		sys.exit(1)
	
	
	finally:
		if con:
			con.close()
def main():
	hostname="localhost"
	username="root"
	database="NHL"
	password = getpass.getpass('Password:')
	
	input = raw_input("Which function would you like to use?\n")
	if(input == "create standings_tables"):
		create_standing_tables(hostname,username,password,database)
		time.sleep(1)
	elif(input == "create team_tables"):
		create_team_tables(hostname,username,password,database)
		time.sleep(1)
	elif(input == "drop standings_tables"):
		answer = raw_input("This will delete current table of date, are you sure?")
		if(answer == "yes"):
			drop_all_standings_tables(hostname,username,password,database)
		else:
			print "Table drop aborted successfully"
	elif(input == "drop teams_tables"):
		answer = raw_input("This will delete current table of date, are you sure?")
		if(answer == "yes"):
			drop_all_teams_tables(hostname,username,password,database)
		else:
			print "Table drop aborted successfully"
	elif(input == "drop"):
		tab = raw_input("what table would you like to drop?")
		answer = raw_input("This will delete current table of date, are you sure?")
		if(answer == "yes" or answer == "y"):
			drop_table(hostname,username,password,database,tab)
		else:
			print "Table drop aborted successfully"
	elif(input == "test connection"):
		test_connection(hostname,username,password,database)
			
if __name__ == "__main__":
	main()