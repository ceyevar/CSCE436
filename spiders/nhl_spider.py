#scrapy crawl nhl -a usr=USER -a pwd=PASSWORD
#curl http://localhost:6800/schedule.json -d project=nhlscraper -d spider=nhl -d usr=USER -d pwd=!PASSWORD 
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
	name = 'nhl'
	start_urls = ['https://www.nhl.com/standings']

	#arguments
	def __init__(self, *args, **kwargs):
		super(LoginSpider,self).__init__(*args,**kwargs)
		
		#connect to mysql
		self.hostname = "localhost"
		self.username = str(kwargs.get("usr","HELLO"))
		self.password = str(kwargs.get("pwd","HELLO"))
		self.database = "NHL"
		self.start_time = time.time()
		self.password = "!" + self.password
		
	def parse(self, response):
		LOGGER.setLevel(logging.WARNING)
		driver = webdriver.PhantomJS("/home/ec2-user/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
		browser = driver.get('https://www.nhl.com/standings')

		time.sleep(3)
		
		driver.find_element_by_xpath("//a[@aria-controls='division'][@role='tab'][@class='standings-jumbotron__title-banner__navigation__item']").click()
		time.sleep(3)

		try:
			print "trying pymysql connection..."
			con = pymysql.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database)  
			cur = con.cursor()
			
			time.sleep(1)
			
			cur.execute("DELETE FROM current_standings")
			
			time.sleep(1)
			
			east_conf = []
			east_conf.append("CAR")
			east_conf.append("CBJ")
			east_conf.append("NJD")
			east_conf.append("NYI")
			east_conf.append("NYR")
			east_conf.append("PHI")
			east_conf.append("PIT")
			east_conf.append("WSH")
			
			east_conf.append("BOS")
			east_conf.append("BUF")
			east_conf.append("DET")
			east_conf.append("FLA")
			east_conf.append("MTL")
			east_conf.append("OTT")
			east_conf.append("TBL")
			east_conf.append("TOR")
			
			east_metropolitan_div = []
			east_metropolitan_div.append("CAR")
			east_metropolitan_div.append("CBJ")
			east_metropolitan_div.append("NJD")
			east_metropolitan_div.append("NYI")
			east_metropolitan_div.append("NYR")
			east_metropolitan_div.append("PHI")
			east_metropolitan_div.append("PIT")
			east_metropolitan_div.append("WSH")
			
			east_atlantic_div = []
			east_atlantic_div.append("BOS")
			east_atlantic_div.append("BUF")
			east_atlantic_div.append("DET")
			east_atlantic_div.append("FLA")
			east_atlantic_div.append("MTL")
			east_atlantic_div.append("OTT")
			east_atlantic_div.append("TBL")
			east_atlantic_div.append("TOR")
			
			west_conf = []
			west_conf.append("CHI")
			west_conf.append("COL")
			west_conf.append("DAL")
			west_conf.append("MINN")
			west_conf.append("NSH")
			west_conf.append("STL")
			west_conf.append("WPG")
			
			west_conf.append("ANA")
			west_conf.append("ARI")
			west_conf.append("CGY")
			west_conf.append("EDM")
			west_conf.append("LAK")
			west_conf.append("SJS")
			west_conf.append("VAN")
			
			west_central_div = []
			west_central_div.append("CHI")
			west_central_div.append("COL")
			west_central_div.append("DAL")
			west_central_div.append("MINN")
			west_central_div.append("NSH")
			west_central_div.append("STL")
			west_central_div.append("WPG")
			
			west_pacific_div = []
			west_pacific_div.append("ANA")
			west_pacific_div.append("ARI")
			west_pacific_div.append("CGY")
			west_pacific_div.append("EDM")
			west_pacific_div.append("LAK")
			west_pacific_div.append("SJS")
			west_pacific_div.append("VAN")
			
			i = 1
			#Initial insert for Eastern and Metropolitan
			while i < len(driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']").find_elements_by_tag_name('tr')):
				teamrank = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[1]").get_attribute('innerHTML')
				teamname = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[2]").get_attribute('innerHTML')
				if ("p-"== teamname[:2] or "x-" == teamname[:2] or "y-" == teamname[:2] or "z-" == teamname[:2]):
					teamname = teamname[2:]
				print teamname
				teamnameabbr = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[3]").get_attribute('innerHTML')
				if ("p-"== teamnameabbr[:2] or "x-" == teamnameabbr[:2] or "y-" == teamnameabbr[:2] or "z-" == teamnameabbr[:2]):
					teamnameabbr = teamnameabbr[2:]
				print teamnameabbr
				gamesplayed = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(2)+ "]/span").get_attribute('innerHTML')
				wins = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(3)+ "]/span").get_attribute('innerHTML')
				losses = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(4)+ "]/span").get_attribute('innerHTML')
				overtime = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(5)+ "]/span").get_attribute('innerHTML')
				points = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(6)+ "]/span").get_attribute('innerHTML')
				row = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(7)+ "]/span").get_attribute('innerHTML')
				goalsfor = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(8)+ "]/span").get_attribute('innerHTML')
				goalsagainst = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(9)+ "]/span").get_attribute('innerHTML')
				if goalsfor==goalsagainst:
					goaldifferential = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(10)+ "]/span").get_attribute('innerHTML')
				elif goalsfor!=goalsagainst:
					goaldifferential = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(10)+ "]/span/span").get_attribute('innerHTML')
				home = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(11)+ "]/span").get_attribute('innerHTML')
				away = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(12)+ "]/span").get_attribute('innerHTML')
				shootout = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(13)+ "]/span").get_attribute('innerHTML')
				lastten = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(14)+ "]/span").get_attribute('innerHTML')
				streak = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(15)+ "]/span").get_attribute('innerHTML')
				lastgame = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(16)+ "]/span/a").get_attribute('innerHTML')
				poop = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(17)+ "]/span").get_attribute('innerHTML')
				if(poop != ""):
					nextgame = driver.find_element_by_xpath("//div[@id='division-division-18']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(17)+ "]/span/a").get_attribute('innerHTML')
				else:
					nextgame = ""
				teamdivision = "NA"
				teamconference = "NA"
				
				if teamnameabbr in east_conf:
					teamconference = "Eastern"
					if teamnameabbr in east_metropolitan_div:
						teamdivision = "Metropolitan"
					elif teamnameabbr in east_atlantic_div:
						teamdivision = "Atlantic"
				
				if teamnameabbr in west_conf:
					teamconference = "Western"
					if teamnameabbr in west_central_div:
						teamdivision = "Central"
					elif teamnameabbr in west_pacific_div:
						teamdivision = "Pacific"
				
				time.sleep(.5)
				#print teamrank, teamname, teamnameabbr, gamesplayed, wins, losses, overtime, points, row, goalsfor, goalsagainst, goaldifferential, home, away, shootout, lastten, streak, lastgame,nextgame, teamdivision, teamconference
				
				tbname ='current_standings'
				sql = """INSERT INTO current_standings(current_ranking, team_name, name_abbreviation, games_played, wins, losses, overtime, points, row, goals_for, goals_against, goal_differential, home_record, 
					away_record, shootout_record, last_ten_record, streak, last_game, next_game, division, conference) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" #% tbname
				cur.execute(sql,(teamrank, teamname, teamnameabbr, gamesplayed, wins, losses, overtime, points, row, goalsfor, 
					goalsagainst, goaldifferential, home, away, shootout, lastten, streak, lastgame,nextgame, teamdivision, teamconference))
					
				#print teamname, nextgame
				i+=1
			
			i = 1
			#Initial insert for Eastern and Atlantic
			while i < len(driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']").find_elements_by_tag_name('tr')):
				teamrank = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[1]").get_attribute('innerHTML')
				teamname = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[2]").get_attribute('innerHTML')
				if ("p-"== teamname[:2] or "x-" == teamname[:2] or "y-" == teamname[:2] or "z-" == teamname[:2]):
					teamname = teamname[2:]
				print teamname
				teamnameabbr = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[3]").get_attribute('innerHTML')
				if ("p-"== teamnameabbr[:2] or "x-" == teamnameabbr[:2] or "y-" == teamnameabbr[:2] or "z-" == teamnameabbr[:2]):
					teamnameabbr = teamnameabbr[2:]
				print teamnameabbr
				gamesplayed = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(2)+ "]/span").get_attribute('innerHTML')
				wins = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(3)+ "]/span").get_attribute('innerHTML')
				losses = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(4)+ "]/span").get_attribute('innerHTML')
				overtime = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(5)+ "]/span").get_attribute('innerHTML')
				points = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(6)+ "]/span").get_attribute('innerHTML')
				row = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(7)+ "]/span").get_attribute('innerHTML')
				goalsfor = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(8)+ "]/span").get_attribute('innerHTML')
				goalsagainst = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(9)+ "]/span").get_attribute('innerHTML')
				if goalsfor==goalsagainst:
					goaldifferential = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(10)+ "]/span").get_attribute('innerHTML')
				elif goalsfor!=goalsagainst:
					goaldifferential = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(10)+ "]/span/span").get_attribute('innerHTML')
				home = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(11)+ "]/span").get_attribute('innerHTML')
				away = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(12)+ "]/span").get_attribute('innerHTML')
				shootout = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(13)+ "]/span").get_attribute('innerHTML')
				lastten = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(14)+ "]/span").get_attribute('innerHTML')
				streak = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(15)+ "]/span").get_attribute('innerHTML')
				lastgame = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(16)+ "]/span/a").get_attribute('innerHTML')
				poop = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(17)+ "]/span").get_attribute('innerHTML')
				if(poop != ""):
					nextgame = driver.find_element_by_xpath("//div[@id='division-division-17']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(17)+ "]/span/a").get_attribute('innerHTML')
				else:
					nextgame = ""
				teamdivision = "NA"
				teamconference = "NA"
				
				if teamnameabbr in east_conf:
					teamconference = "Eastern"
					if teamnameabbr in east_metropolitan_div:
						teamdivision = "Metropolitan"
					elif teamnameabbr in east_atlantic_div:
						teamdivision = "Atlantic"
				
				if teamnameabbr in west_conf:
					teamconference = "Western"
					if teamnameabbr in west_central_div:
						teamdivision = "Central"
					elif teamnameabbr in west_pacific_div:
						teamdivision = "Pacific"
				
				time.sleep(.5)
				#print teamrank, teamname, teamnameabbr, gamesplayed, wins, losses, overtime, points, row, goalsfor, goalsagainst, goaldifferential, home, away, shootout, lastten, streak, lastgame,nextgame, teamdivision, teamconference
				
				tbname ='current_standings'
				sql = """INSERT INTO current_standings(current_ranking, team_name, name_abbreviation, games_played, wins, losses, overtime, points, row, goals_for, goals_against, goal_differential, home_record, 
					away_record, shootout_record, last_ten_record, streak, last_game, next_game, division, conference) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" #% tbname
				cur.execute(sql,(teamrank, teamname, teamnameabbr, gamesplayed, wins, losses, overtime, points, row, goalsfor, 
					goalsagainst, goaldifferential, home, away, shootout, lastten, streak, lastgame,nextgame, teamdivision, teamconference))
					
				#print teamname, nextgame
				i+=1
			
			i = 1
			#Initial insert for Western and Central
			while i < len(driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']").find_elements_by_tag_name('tr')):
				teamrank = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[1]").get_attribute('innerHTML')
				teamname = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[2]").get_attribute('innerHTML')
				if ("p-"== teamname[:2] or "x-" == teamname[:2] or "y-" == teamname[:2] or "z-" == teamname[:2]):
					teamname = teamname[2:]
				print teamname
				teamnameabbr = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[3]").get_attribute('innerHTML')
				if ("p-"== teamnameabbr[:2] or "x-" == teamnameabbr[:2] or "y-" == teamnameabbr[:2] or "z-" == teamnameabbr[:2]):
					teamnameabbr = teamnameabbr[2:]
				print teamnameabbr
				gamesplayed = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(2)+ "]/span").get_attribute('innerHTML')
				wins = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(3)+ "]/span").get_attribute('innerHTML')
				losses = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(4)+ "]/span").get_attribute('innerHTML')
				overtime = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(5)+ "]/span").get_attribute('innerHTML')
				points = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(6)+ "]/span").get_attribute('innerHTML')
				row = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(7)+ "]/span").get_attribute('innerHTML')
				goalsfor = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(8)+ "]/span").get_attribute('innerHTML')
				goalsagainst = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(9)+ "]/span").get_attribute('innerHTML')
				if goalsfor==goalsagainst:
					goaldifferential = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(10)+ "]/span").get_attribute('innerHTML')
				elif goalsfor!=goalsagainst:
					goaldifferential = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(10)+ "]/span/span").get_attribute('innerHTML')
				home = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(11)+ "]/span").get_attribute('innerHTML')
				away = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(12)+ "]/span").get_attribute('innerHTML')
				shootout = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(13)+ "]/span").get_attribute('innerHTML')
				lastten = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(14)+ "]/span").get_attribute('innerHTML')
				streak = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(15)+ "]/span").get_attribute('innerHTML')
				lastgame = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(16)+ "]/span/a").get_attribute('innerHTML')
				poop = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(17)+ "]/span").get_attribute('innerHTML')
				if(poop != ""):
					nextgame = driver.find_element_by_xpath("//div[@id='division-division-16']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(17)+ "]/span/a").get_attribute('innerHTML')
				else:
					nextgame = ""
				teamdivision = "NA"
				teamconference = "NA"
				
				if teamnameabbr=="MIN":
					teamnameabbr="MINN"
				if teamnameabbr in east_conf:
					teamconference = "Eastern"
					if teamnameabbr in east_metropolitan_div:
						teamdivision = "Metropolitan"
					elif teamnameabbr in east_atlantic_div:
						teamdivision = "Atlantic"
				
				if teamnameabbr in west_conf:
					teamconference = "Western"
					if teamnameabbr in west_central_div:
						teamdivision = "Central"
					elif teamnameabbr in west_pacific_div:
						teamdivision = "Pacific"
				
				
				time.sleep(.5)
				#print teamrank, teamname, teamnameabbr, gamesplayed, wins, losses, overtime, points, row, goalsfor, goalsagainst, goaldifferential, home, away, shootout, lastten, streak, lastgame,nextgame, teamdivision, teamconference
				
				tbname ='current_standings'
				sql = """INSERT INTO current_standings(current_ranking, team_name, name_abbreviation, games_played, wins, losses, overtime, points, row, goals_for, goals_against, goal_differential, home_record, 
					away_record, shootout_record, last_ten_record, streak, last_game, next_game, division, conference) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" #% tbname
				cur.execute(sql,(teamrank, teamname, teamnameabbr, gamesplayed, wins, losses, overtime, points, row, goalsfor, 
					goalsagainst, goaldifferential, home, away, shootout, lastten, streak, lastgame,nextgame, teamdivision, teamconference))
					
				#print teamname, nextgame
				i+=1
			
			i = 1
			#Initial insert for Western and Pacific
			while i < len(driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']").find_elements_by_tag_name('tr')):
				teamrank = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[1]").get_attribute('innerHTML')
				teamname = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[2]").get_attribute('innerHTML')
				if ("p-"== teamname[:2] or "x-" == teamname[:2] or "y-" == teamname[:2] or "z-" == teamname[:2]):
					teamname = teamname[2:]
				print teamname
				teamnameabbr = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(1)+ "]/span/a/span[3]").get_attribute('innerHTML')
				if ("p-"== teamnameabbr[:2] or "x-" == teamnameabbr[:2] or "y-" == teamnameabbr[:2] or "z-" == teamnameabbr[:2]):
					teamnameabbr = teamnameabbr[2:]
				print teamnameabbr
				gamesplayed = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(2)+ "]/span").get_attribute('innerHTML')
				wins = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(3)+ "]/span").get_attribute('innerHTML')
				losses = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(4)+ "]/span").get_attribute('innerHTML')
				overtime = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(5)+ "]/span").get_attribute('innerHTML')
				points = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(6)+ "]/span").get_attribute('innerHTML')
				row = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(7)+ "]/span").get_attribute('innerHTML')
				goalsfor = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(8)+ "]/span").get_attribute('innerHTML')
				goalsagainst = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(9)+ "]/span").get_attribute('innerHTML')
				if goalsfor==goalsagainst:
					goaldifferential = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(10)+ "]/span").get_attribute('innerHTML')
				elif goalsfor!=goalsagainst:
					goaldifferential = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(10)+ "]/span/span").get_attribute('innerHTML')
				home = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(11)+ "]/span").get_attribute('innerHTML')
				away = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(12)+ "]/span").get_attribute('innerHTML')
				shootout = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(13)+ "]/span").get_attribute('innerHTML')
				lastten = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(14)+ "]/span").get_attribute('innerHTML')
				streak = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(15)+ "]/span").get_attribute('innerHTML')
				lastgame = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(16)+ "]/span/a").get_attribute('innerHTML')
				poop = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(17)+ "]/span").get_attribute('innerHTML')
				if(poop != ""):
					nextgame = driver.find_element_by_xpath("//div[@id='division-division-15']/div/div/div[@class='responsive-datatable__pinned']/table/tbody/tr[" +str(i)+ "]/td[" +str(17)+ "]/span/a").get_attribute('innerHTML')
				else:
					nextgame = ""
				teamdivision = "NA"
				teamconference = "NA"
				
				if teamnameabbr in east_conf:
					teamconference = "Eastern"
					if teamnameabbr in east_metropolitan_div:
						teamdivision = "Metropolitan"
					elif teamnameabbr in east_atlantic_div:
						teamdivision = "Atlantic"
				
				if teamnameabbr in west_conf:
					teamconference = "Western"
					if teamnameabbr in west_central_div:
						teamdivision = "Central"
					elif teamnameabbr in west_pacific_div:
						teamdivision = "Pacific"
				
				time.sleep(.5)
				#print teamrank, teamname, teamnameabbr, gamesplayed, wins, losses, overtime, points, row, goalsfor, goalsagainst, goaldifferential, home, away, shootout, lastten, streak, lastgame,nextgame, teamdivision, teamconference
				
				tbname ='current_standings'
				sql = """INSERT INTO current_standings(current_ranking, team_name, name_abbreviation, games_played, wins, losses, overtime, points, row, goals_for, goals_against, goal_differential, home_record, 
					away_record, shootout_record, last_ten_record, streak, last_game, next_game, division, conference) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" #% tbname
				cur.execute(sql,(teamrank, teamname, teamnameabbr, gamesplayed, wins, losses, overtime, points, row, goalsfor, 
					goalsagainst, goaldifferential, home, away, shootout, lastten, streak, lastgame,nextgame, teamdivision, teamconference))
					
				#print teamname, nextgame
				i+=1
				
			con.commit()
			if con:
				con.close()
		except pymysql.DatabaseError, e:
				print 'Error %s' % e    
				sys.exit(1)
		print("--- %s seconds ---" % (time.time() - self.start_time))