"""
	Name: Fetching partitions where the size is > 8G
	Description: Executed from HP OO, Fetching partitions where the size is > 8G
	Team: Software Service Automation
	Inputs: Arguments [LogServer,LogDB,ORACLEServer,APID,LogAccountName,LogUser,LogPwd,ORACLEServer,ORACLESeUsername,ORACLESePassword], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
"""

# Modules Initializing #
import datetime
import sys
import socket
import cx_Oracle as dbc
import ActivityLogger
#import HLStatus
import paramiko

OFol = "C:\\Python_Logs\\OracleInstallUpgrade"
OFile = OFol + "\\" + 'fetch_partition_greterthan8.log'
# Variable Mapping #
ActivityName = "Fetching partitions where the size is > 8G"
Des = " Fetching partitions where the size is > 8G"
a = 0
s = socket.socket()

try:
	with open(OFile, 'w+') as of:
		print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Starting Script Execution"
		# Arguments Mapping #

		if len(sys.argv) == 4:
			##Log Variables##
			#LogServer = sys.argv[1]
			#LogDB = sys.argv[2]
			#APID = sys.argv[3]
			#LogAccountName = sys.argv[4]
			#LogUser = sys.argv[5]
			#LogPwd = sys.argv[6]

			##Script Variables##
			ORACLEServer = sys.argv[1]  # Target ORACLEServer
			ORACLESeUsername=sys.argv[2] #
			ORACLESePassword=sys.argv[3]
			#DbUser = sys.argv[10]  # Target Database user to connect to listener
			#ORACLEDBPassword = sys.argv[11]  # Target Database user password to connect to listener
			   
			CIServer = ORACLEServer
			address = ORACLEServer
			port = 22
			
			l = []
			
			# Connectivity Test #
			# HLStatus.UpdateHLStatus(APID,"Stepid26","In Progress"," validate limits.conf file. ")
			#ActivityLogger.InsertActivityLog(APID, CIServer, ActivityName, Des, "Initiated", LogAccountName, "No Error", "Connectivity check initiated", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Checking connectivity for", ORACLEServer

			s.connect((address, port))

			#ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Host is reachable", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ":", ORACLEServer, "is reachable "
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Estimate datafile size "

			## Database Connection String ##
				
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(ORACLEServer, username=ORACLESeUsername, password=ORACLESePassword)
			#ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesfull to the host",LogServer,LogDB,LogUser,LogPwd)

			#log.info('Executing the command :{0}'.format(command))
			#ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Fetching partitions where the size is > 8G",LogServer,LogDB,LogUser,LogPwd)
			#print "hi"

			command1="df | awk '{ if ($4/1024/1024 > 8) print $6; }'"
			stdin, stdout, stderr = dssh.exec_command(command1)
			output1 = stdout.read()
			errout = stderr.read()
			#print output1
			type(output1)
			#print output1
			output1=output1.split("\n")
			if "/" in output1:
                                output1.remove("/")
                        #print output1
			if output1 == ['']:
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 10"
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: No partitions is having space more than 8GB" 
				print "10"
				print "ExitDesc: No partition is having space more than 8GB"
			else:
				#output1=output1.split("\n")
				makeitastring = ",".join(str(x) for x in output1)
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 10"
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc:  partitions  having space more than 8GB are %s " %makeitastring 
				print "0"
				print "ExitDesc: Some partition is having space more than 8GB "
				print makeitastring
				#ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Fetching partitions where the size is > 8G",LogServer,LogDB,LogUser,LogPwd)
		else:
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 10"
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Missing Arguments"
			print "1"
			print "ExitDesc: Missing Arguments" 
except socket.error:
	with open(OFile,'a') as of1:
		#ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1"
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Connectivity to server %s failed" %address
	print "1"
	print "ExitDesc: Connectivity to server %s failed" %address

except:
	with open(OFile, 'a') as of1:
		#ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		# HLStatus.UpdateHLStatus(APID,"Stepid26","Failed","Fetching partitions where the size is > 8G failed.")
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 1"
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	print "1"
	print "ExitDesc: Script Failed due to ", sys.exc_info()[1]

finally:
	s.close()
	
