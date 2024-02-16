"""
	Name: SpaceCheckForbackup
	Description: Executed from HP OO, With the Size required for backup looks for bestfit partition
	Team: Software Service Automation
	Inputs: Arguments [Hostname,DBUsername,DBPassword,TNSName], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
	
"""
# Modules Initializing #
import datetime
import sys
import re
import socket
import ActivityLogger
import HLStatus
import paramiko
#import cx_Oracle as dbc
# Workflow engine log module Initializing

OFol="C:\Python_Logs\Oracle_Upgradation"
OFile=OFol + "\\" + 'SpaceCheckForbackup.log'
# Variable Mapping #
ActivityName = "SpaceCheckForbackup"
Des = "With the Size required for backup looks for bestfit partition"
a=0
s = socket.socket()
try:
	with open(OFile,'w+') as of:
		print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,": Starting Script Execution";
	# Arguments Mapping #
		if len(sys.argv) == 12 :
			##Log Variables##
			LogServer = sys.argv[1];
			LogDB = sys.argv[2];   
			APID = sys.argv[3];
			LogAccountName =sys.argv[4]
			LogUser=sys.argv[5]
			LogPwd=sys.argv[6]
			
			##Script Variables##
			Hostname = sys.argv[7]    #Target HostName  	
			LinUser = sys.argv[8]	  #Target Database user to connect to listener
			LinPass = sys.argv[9]	  #Target Database user password to connect to listener
			BackupSize = sys.argv[10] #Backup size required
			Ex = sys.argv[11]	  #Excluded partitions in list e.g.(/,/x,/xm)
			Ex=Ex.split(",")
			CIServer = Hostname;
			address = Hostname;
			port = 22 

			ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
			#HLStatus.UpdateHLStatus(APID,"Stepid75","In Progress","Checking Space available partition for backups",LogServer,LogDB,LogUser,LogPwd)
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,": Checking connectivity for",Hostname;
			
			s.connect((address, port)) 
			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,":", Hostname, "is reachable ";
		

			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Connecting to server",LogServer,LogDB,LogUser,LogPwd)
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,":", Hostname, "is reachable ";
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(Hostname, username=LinUser, password=LinPass)
			
			command ="df -h -m | awk '($4*0.80)>%s{print $6}'"%(BackupSize)
			
			stdin, stdout, stderr = dssh.exec_command(command)
			output = stdout.read()
			dssh.close()	
			output = output[:-1]
			selectpart = output.split("\n")
			selectpart = list(filter(None, selectpart))
			#print selectpart
			#print Ex
			parts = list(set(selectpart) - set(Ex))
			#print set(selectpart) - set(Ex)
			if not parts:
				print "10";
				print "ExitDesc: Space is not available";
			else:
				print "0";
				print "ExitDesc: Space is available";
				print parts[0]
			
		else:
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 10";
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Missing Arguments";
			#HLStatus.UpdateHLStatus(APID,"Stepid75","Failed","Missing Arguments.")
			print "10";
			print "ExitDesc: Missing Arguments";
except socket.error:
	with open(OFile,'a') as of1:
		#print "%s" %exc
		#print "%s is invalid" %address
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 10"
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Invalid server ip address"
	ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Invalid server ip",LogServer,LogDB,LogUser,LogPwd)
	#HLStatus.UpdateHLStatus(APID,"Stepid75","Failed","Invalid server ip address",LogServer,LogDB,LogUser,LogPwd)
	print "10"
	print "ExitDesc: script failed due to Invalid server ip address %s" %address
except:
	with open(OFile,'a') as of1:
		
		ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Check the Log for error",LogServer,LogDB,LogUser,LogPwd)
		#HLStatus.UpdateHLStatus(APID,"Stepid75","Failed","SpcaeCheck Backup Failed Check Log for errors",LogServer,LogDB,LogUser,LogPwd)
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 10";
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Script Failed due to ",sys.exc_info()[1];
	print "1";
	print "ExitDesc: Script Failed due to ",sys.exc_info()[1];
finally:
	s.close()