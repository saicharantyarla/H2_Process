"""
	Name: TNSCheck
	Description: Executed from HP OO, Checks TNS
	Team: Software Service Automation
	Inputs: Arguments [Hostname,DBUsername,DBPassword,TNSName], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
	
"""
# Modules Initializing #
import datetime
import sys
import socket
import cx_Oracle as dbc
# Workflow engine log module Initializing

OFol="C:\Python_Logs\Oracle_Upgradation"
OFile=OFol + "\\" + 'DBcredValid_FetchDB.txt'
a=0
s = socket.socket()
try:
	with open(OFile,'w+') as of:
		print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,": Starting Script Execution";
	# Arguments Mapping #
		if len(sys.argv) == 5 :
			
			##Script Variables##
			Hostname = sys.argv[1]  #Target HostName  	
			DbUser = sys.argv[2]	#Target Database user to connect to listener
			DbPass = sys.argv[3]	#Target Database user password to connect to listener
			TNSName =sys.argv[4]	#Target TNS Name
			
			address = Hostname;
			port = 22 

			#Connectivity Test #
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,": Checking connectivity for",Hostname;
			
			s.connect((address, port)) 
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,":", Hostname, "is reachable ";
		
			UrCh="select name from v$database";
			
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"Checking whether TNS is able to connect ";
				
			## Database Connection String ##
			conn=dbc.connect(dsn=TNSName,user=DbUser,password=DbPass,mode=dbc.SYSDBA)
			cur=conn.cursor()
			cur.execute(UrCh)
			out = cur.fetchall()

			if out :
				print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"Credentials are valid"
				print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 0 \n";
				print "0"
				print "ExitDesc: Credentials are valid"
				print out[0][0]
			else:
				print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"Unable to Fetch Database NAme"
				print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 10 \n";
				print "10"
				print "ExitDesc: Unable to fetch Database Name"
			
			cur.close()
			conn.close()
			
		else:
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1";
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Missing Arguments";
			print "1";
			print "ExitDesc: Missing Arguments";
except socket.error:
	with open(OFile,'a') as of1:
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1"
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Invalid server ip address"
	print "1"
	print "ExitDesc: script failed due to Invalid server ip address %s" %address
except dbc.DatabaseError as e:
	error, = e.args
	if error.code == 12154:
		ExitCode="10"
		ExitDesc="Issue with TNS Name"
	elif error.code == 1017:
		ExitCode="10"
		ExitDesc="Password is incorrect "
	else:
		ExitCode="1"
		ExitDesc=sys.exc_info()[1]
	print ExitCode
	print "ExitDesc:",ExitDesc
	with open(OFile,'a') as of1:
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode:%s"%ExitCode
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: %s"%ExitDesc
	
except:
	ms=sys.exc_info()[1]
	#print ms.code	
	#ms.strip()
	ExitCode="1"
	ExitDesc="Check the log for errors"
	with open(OFile,'a') as of1:
		
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode:%s"%ExitCode
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: %s"%ExitDesc
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"Error: %s"%ms
	print ExitCode
	print "ExitDesc: %s"%ExitDesc
finally:
	s.close()