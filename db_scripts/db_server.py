#removed username and password for the db

from socket import *
import pymysql
import sys, getopt
import time
import getpass

def get_stats(db_username, db_password, from_table, columns_to_return, where_statements):
	try:
		#print "trying pymysql connection..."
		con = pymysql.connect(host="localhost", user=db_username, passwd=db_password, db="NHL")  
		cur = con.cursor()
		time.sleep(0.3)
		sql = "SELECT "+columns_to_return+" FROM "+from_table+" WHERE"
		where_list = where_statements.split(",")
		#print where_list
		if not where_list:
			sql = sql[:-6]
			cur.execute(sql)
			records = cur.fetchall()
			return records
		else:	
			for w in where_list:
				sql += " "+w+" AND"
			sql = sql[:-4]
			cur.execute(sql)
			records = cur.fetchall()
			return records
		
		
		con.commit()
		if con:
			con.close()
	except pymysql.DatabaseError, e:
				print 'Error %s' % e    
				sys.exit(1)

def main(argv):
	db_username = ''
	db_password = ''
	# try:
		# opts, args = getopt.getopt(argv, "hu:p:",["uname=","pward="])
	# except getopt.GetoptError:
		# print 'db_server.py -u <username> -p <password>'
		# sys.exit()
	# for opt, arg in opts:
		# if opt == '-h':
			# print 'db_server.py -u <username> -p <password>'
			# syst.exit()
		# elif opt in ("-u", "--uname"):
			# db_username = arg
		# elif opt in ("-p", "--pward"):
			# db_password = "!"+arg
	#db_username = "USER"
	#db_password = "!PASSWORD"
	HOST = ""
	PORT = 5432

	s = socket(AF_INET, SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(5) #how many connections the server can recieve at one time
	#CHANGE THIS VALUE AFTER TESTING

	while True:
		conn, addr = s.accept() #accepts the connection
		#print addr, "is connected"
		data = conn.recv(1024) #defines how many bytes the server can accept at one time 
		#print "Received:", data
		#parse string received
		if((data.count(';')==3) and ("drop" not in data)):
			(garbage, from_tables, columns_to_return, where_statements) = data.split(';')
			records = get_stats(db_username, db_password, from_tables, columns_to_return, where_statements)
			conn.sendall(str(records))
			#print str(records)
		conn.close() #Terminates the connection after a response is made 
		
if __name__ == "__main__":
	main(sys.argv[1:])