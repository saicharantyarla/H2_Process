"""	
	Name: Fetch Database List
	Description: Executed from HP OO, fetches Database List based on Oracle Home selected
	Team: Software Service Automation
	Inputs: Arguments [ORACLEServer,ORACLESeUsername,ORACLESePassword,OraHome11], LogFileLoc
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

OFol = "C:\\Python_Logs\\Oracle_Upgradation"
OFile = OFol + "\\" + 'FetchDBList.log'
# Variable Mapping #
ActivityName = "Fetch DBList"
Des = " Validate Oracle 12c is installed or not"
a = 0
s = socket.socket()

try:
	with open(OFile, 'w+') as of:
		print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Starting Script Execution"
		# Arguments Mapping #

		if len(sys.argv) == 5:
			
			##Script Variables##
			ORACLEServer = sys.argv[1]  # Target ORACLEServer
			ORACLESeUsername=sys.argv[2] #
			ORACLESePassword=sys.argv[3]
			OraHome11=sys.argv[4]
			
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
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Validating oracle 12.1.0.2 is already Installed"

			## Database Connection String ##
				
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(ORACLEServer, username=ORACLESeUsername, password=ORACLESePassword)
			#ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesfull to the host",LogServer,LogDB,LogUser,LogPwd)

			#log.info('Executing the command :{0}'.format(command))
			#ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Validating oracle 12 is installed",LogServer,LogDB,LogUser,LogPwd)
			#print "hi"

			command1="""cat /etc/oratab | grep :"""+OraHome11+""":|grep -v '#'| cut -d ":" -f 1 """
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Command that got executed",command1
			stdin, stdout, stderr = dssh.exec_command(command1)
			output1 = stdout.read()
			errout = stderr.read()
			
			if len(output1) == 0:
				if errout:
					print >> of, "[Error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Error:",errout
				else:
					print >> of, "[Error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Unable to fetch the output"
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 10"
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Check the log for errors"
				print "10"
				print "ExitDesc: Check the log for errors"				
			else:
				output1 = output1.split("\n")
				output1=filter(lambda x:x != '', output1)
				opstr = ",".join(str(x) for x in output1)
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"Output Fetched:",opstr 
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 0"
				print >>of,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Database List Fetched " 
				print "0"
				print "ExitDesc:  Database List Fetched "
				print opstr
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
		# HLStatus.UpdateHLStatus(APID,"Stepid26","Failed","Validation failed")
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 1"
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	print "1"
	print "ExitDesc: Script Failed due to ", sys.exc_info()[1]

finally:
	s.close()
	
