#scrapy crawl nhl -a usr=root -a pwd=PASSWORD
#curl http://localhost:6800/schedule.json -d project=nhlscraper -d spider=nhl -d usr=root -d pwd=PASSWORD
from decimal import *
import pymysql
import sys
import scrapy
import json
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
import multiprocessing
import selenium.webdriver.support.ui as UI
import logging
import os
import time

class LoginSpider(Spider):
	name = 'teams'
	start_urls = ['https://www.nhl.com/standings']

	#arguments
	def __init__(self, *args, **kwargs):
		super(LoginSpider,self).__init__(*args,**kwargs)
		
		#connect to mysql
		self.hostname = "localhost"
		self.username = str(kwargs.get("usr","HELLO"))
		self.password = str(kwargs.get("pwd","HELLO"))
		self.which_team = int(kwargs.get("team","HELLO"))
		self.database = "NHL"
		self.start_time = time.time()
		self.password = "!" + self.password
		
	def parse(self, response):
			
		LOGGER.setLevel(logging.WARNING)
		driver = webdriver.PhantomJS("/home/ec2-user/phantomjs-2.1.1-linux-x86_64/bin/phantomjs",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
		
		print "trying pymysql connection..."
		con = pymysql.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database)  
		cur = con.cursor()
		j = self.which_team
		time.sleep(1)
		
		try:
			abbr=[]
			abbr.append("CAR")
			abbr.append("CBJ")
			abbr.append("NJD")
			abbr.append("NYI")
			abbr.append("NYR")
			abbr.append("PHI")
			abbr.append("PIT")
			abbr.append("WSH")
			
			abbr.append("BOS")
			abbr.append("BUF")
			abbr.append("DET")
			abbr.append("FLA")
			abbr.append("MTL")
			abbr.append("OTT")
			abbr.append("TBL")
			abbr.append("TOR")
			
			abbr.append("CHI")
			abbr.append("COL")
			abbr.append("DAL")
			abbr.append("MINN")
			abbr.append("NSH")
			abbr.append("STL")
			abbr.append("WPG")
			
			abbr.append("ANA")
			abbr.append("ARI")
			abbr.append("CGY")
			abbr.append("EDM")
			abbr.append("LAK")
			abbr.append("SJS")
			abbr.append("VAN")
			
			# for dat in abbr:
				# sql = "DELETE FROM %s" % dat
				# cur.execute(sql)
			
			sql = "DELETE FROM %s" % abbr[j]
			cur.execute(sql)
			
			time.sleep(2)
			
			teamname = []
			teamname.append("hurricanes")
			teamname.append("bluejackets")
			teamname.append("devils")
			teamname.append("islanders")
			teamname.append("rangers")
			teamname.append("flyers")
			teamname.append("penguins")
			teamname.append("capitals")
			
			teamname.append("bruins")
			teamname.append("sabres")
			teamname.append("redwings")
			teamname.append("panthers")
			teamname.append("canadiens")
			teamname.append("senators")
			teamname.append("lightning")
			teamname.append("mapleleafs")
			
			teamname.append("blackhawks")
			teamname.append("avalanche")
			teamname.append("stars")
			teamname.append("wild")
			teamname.append("predators")
			teamname.append("blues")
			teamname.append("jets")
			
			teamname.append("ducks")
			teamname.append("coyotes")
			teamname.append("flames")
			teamname.append("oilers")
			teamname.append("kings")
			teamname.append("sharks")
			teamname.append("canucks")

			
			#slows down from connecting to too
			
			#print j
			team_url = "http://" + teamname[j] + ".ice.nhl.com/club/gamelog.htm"

			time.sleep(.5)
			print team_url
		
			browser = driver.get('%s' % team_url)
			
			time.sleep(2)
			
			print "connecting to %s" % driver.current_url
			
			time.sleep(4)
			
			i = 3
			
			while i < len(driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']").find_elements_by_tag_name('tr')):
				game_date = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[1]/a/span").get_attribute('innerHTML')
				home_or_road = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[3]").get_attribute('innerHTML')
				game_outcome = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[4]").get_attribute('innerHTML')
				overtime_shootout = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[5]").get_attribute('innerHTML')
				opponent = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[6]").get_attribute('innerHTML')
				record = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[7]").get_attribute('innerHTML')
				goals_for = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[8]").get_attribute('innerHTML')
				goals_against = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[9]").get_attribute('innerHTML')
				power_play_goals = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[10]").get_attribute('innerHTML')
				power_play_opportunities = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[11]").get_attribute('innerHTML')
				power_play_goals_against = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[12]").get_attribute('innerHTML')
				times_shorthanded = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[13]").get_attribute('innerHTML')
				shorthanded_goals_for = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[14]").get_attribute('innerHTML')
				shorthanded_goals_against = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[15]").get_attribute('innerHTML')
				shots_for = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[16]").get_attribute('innerHTML')
				shots_against = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[17]").get_attribute('innerHTML')
				attendence = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[18]").get_attribute('innerHTML')
				winning_goalie = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[19]").get_attribute('innerHTML')
				winning_goal_scorer = driver.find_element_by_xpath("//div[@id='twoColSpan']/div[@class='tieUpWrap']/div/table[@class='data']/tbody/tr[" + str(i) + "]/td[20]").get_attribute('innerHTML')
				
				sql = """INSERT INTO """ + abbr[j] + """(game_date, home_road, game_outcome, overtime_shootout, opponent, record, goals_for, goals_against, power_play_goals, power_play_opportunities, power_play_goals_against, times_shorthanded, 
					shorthanded_goals_for, shorthanded_goals_against, shots_for, shots_against, attendence, winning_goalie, winning_goal_scorer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
				cur.execute(sql,(game_date, home_or_road, game_outcome, overtime_shootout, opponent, record, goals_for, goals_against, power_play_goals, power_play_opportunities, power_play_goals_against, times_shorthanded, 
					shorthanded_goals_for, shorthanded_goals_against, shots_for, shots_against, attendence, winning_goalie, winning_goal_scorer))
				#print (i-2)
				i+=1
				
			print "Great success! %s %s added!" % (abbr[j],teamname[j])
			
			time.sleep(0.5)
				
			con.commit()
			if con:
				con.close()
		except pymysql.DatabaseError, e:
				print 'Error %s' % e    
				sys.exit(1)
		print("--- %s seconds ---" % (time.time() - self.start_time))