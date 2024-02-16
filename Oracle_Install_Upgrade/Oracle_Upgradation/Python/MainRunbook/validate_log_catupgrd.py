"""
	Name: Validate Logs for catupgd.sql
	Description: Executed from HP OO, Validate Logs for catupgd.sql
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
import HLStatus
import paramiko

OFol = "C:\\Python_Logs\\Oracle_Upgrade_Install\\Oracle_Upgradation"
OFile = OFol + "\\" + 'validate_log_catupgrd.log'
# Variable Mapping #
ActivityName = "Validating log"
Des = " Validating log for catupgd"
a = 0
s = socket.socket()

try:
	with open(OFile, 'w+') as of:
		print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Starting Script Execution"
		# Arguments Mapping #

		if len(sys.argv) == 11:
			##Log Variables##
			LogServer = sys.argv[1]
			LogDB = sys.argv[2]
			APID = sys.argv[3]
			LogAccountName = sys.argv[4]
			LogUser = sys.argv[5]
			LogPwd = sys.argv[6]

			##Script Variables##
			ORACLEServer = sys.argv[7]  # Target ORACLEServer
			ORACLESeUsername=sys.argv[8] #
			ORACLESePassword=sys.argv[9]
			ORACLEHome = sys.argv[10]
			path1 = "/rdbms/admin/"
			path = ORACLEHome + path1
			   
			CIServer = ORACLEServer
			address = ORACLEServer
			port = 22
			
			l = []
			
			# Connectivity Test #

			ActivityLogger.InsertActivityLog(APID, CIServer, ActivityName, Des, "Initiated", LogAccountName, "No Error", "Connectivity check initiated", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Checking connectivity for", ORACLEServer

			s.connect((address, port))

			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Host is reachable", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ":", ORACLEServer, "is reachable "
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Estimate datafile size "
			HLStatus.UpdateHLStatus(APID,"Stepid101","In Progress","Oracle Upgradation is in Progress which is executing Logcheck of Catupgd script",LogServer,LogDB,LogUser,LogPwd)	
			## Database Connection String ##
				
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(ORACLEServer, username=ORACLESeUsername, password=ORACLESePassword)
			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesfull to the host",LogServer,LogDB,LogUser,LogPwd)

			#log.info('Executing the command :{0}'.format(command))
			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Validating  catupgrd log files",LogServer,LogDB,LogUser,LogPwd)
			#print "hi"

			command1="""cd """+path+"""
for i in `ls catupgr*.log`
do
abc=`cat $i | grep "^ORA-"`
#echo $abc
if [[ $abc != "" ]];then
echo $i
fi
done"""
			
			stdin, stdout, stderr = dssh.exec_command(command1)
			output1 = stdout.read()
			errout = stderr.read()
			output1 = output1.strip()
			output1=output1.split("\n")
			output1=",".join(output1)
			#print output1
			#print len(output1)
			if len(output1) == 0:
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 0"
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Log files are validated ,No errors"
				ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","No error Found in the Log files",LogServer,LogDB,LogUser,LogPwd)				
				print "0"
				print "ExitDesc: log files are validated ,No errors"
				
			else:
				output1 = output1.split("\n")
				makeitastring = ",".join(str(x) for x in output1)
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 10"
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc:  log files containg error are %s " %makeitastring 
				print "10"
				print "ExitDesc:  log files containg error are %s " %makeitastring
				HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- LogCheck for CatUpgrd Script failed",LogServer,LogDB,LogUser,LogPwd)
				ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Check the log for error",LogServer,LogDB,LogUser,LogPwd)
		else:
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 1"
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Missing Arguments"
			print "1"
			print "ExitDesc: Missing Arguments" 
except socket.error:
	with open(OFile,'a') as of1:
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1"
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Connectivity to server %s failed" %address
	print "1"
	print "ExitDesc: Connectivity to server %s failed" %address
	HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- LogCheck for CatUpgrd Script failed",LogServer,LogDB,LogUser,LogPwd)
except:
	with open(OFile, 'a') as of1:
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		# HLStatus.UpdateHLStatus(APID,"Stepid26","Failed",".")
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 1"
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	print "1"
	print "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- LogCheck for CatUpgrd Script failed",LogServer,LogDB,LogUser,LogPwd)
finally:
	s.close()

	
	
	
	

