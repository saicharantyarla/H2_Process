"""
	Name: Validating database Registry
	Description: Executed from HP OO, Validating database Registry
	Team: Software Service Automation
	Inputs: Arguments [LogServer,LogDB,ORACLEServer,APID,LogAccountName,LogUser,LogPwd,ORACLEServer,ORACLESeUsername,ORACLESePassword,TNSName], LogFileLoc
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
import os
OFol = "C:\\Python_Logs\\Oracle_Upgrade_Install\\Oracle_Upgradation"
OFile = OFol + "\\" + 'validate_dba_registry.log'
# Variable Mapping #
ActivityName = "Validating Database Registry"
Des = " Validating Database Registry "
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
			#ORACLESeUsername=sys.argv[8] #
			#ORACLESePassword=sys.argv[9]
			DbUser = sys.argv[8]  # Target Database user to connect to listener
			ORACLEDBPassword = sys.argv[9]  # Target Database user password to connect to listener
			TNSNames = sys.argv[10]
			
			FTNS = []
			STNS = []

			CIServer = ORACLEServer
			address = ORACLEServer
			port = 22
			# Connectivity Test #
			HLStatus.UpdateHLStatus(APID,"Stepid99","In Progress","Oracle Upgradation Pre Check is in Progress which is executing Validate DBA Registry script",LogServer,LogDB,LogUser,LogPwd)			
			ActivityLogger.InsertActivityLog(APID, CIServer, ActivityName, Des, "Initiated", LogAccountName, "No Error", "Connectivity check initiated", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Checking connectivity for", ORACLEServer
			
			s.connect((address, port))
		
			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Host is reachable", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ":", ORACLEServer, "is reachable "
			
			
			for TNSName in TNSNames.split(','):
				
				#print TNSName
				#print len(TNSName)
				a = 0
				l = []
				
				
				
				
				print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ":", ORACLEServer, "Validating Database Registry "
				## Database Connection String ##
				conn = dbc.connect(dsn=TNSName, user=DbUser, password=ORACLEDBPassword, mode=dbc.SYSDBA)
				cur = conn.cursor()
				comnd="SELECT STATUS FROM DBA_REGISTRY WHERE STATUS ='VALID'"
				print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%s" % (comnd)
				cur.execute(comnd)
				for row in cur:
					a=1
					comnd2="SELECT comp_name FROM DBA_REGISTRY WHERE STATUS ='VALID'"
					cur.execute(comnd2)
					for b in cur:
						c=str(b)
						d=c.encode("utf-8")
						e=d.strip("(',')")
						l.append(e)
					print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": valid components for %s are %s " % (TNSName,l)
					STNS.append(TNSName)
				if a==0:
					FTNS.append(TNSName)
				cur.close()
				conn.close()
				s.close()
			if len(STNS)==0:
				print "10"
				print "ExitDesc: All TNSNames contain INVALID objects and the TNSNames are %s" %(FTNS)
				ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","All TNS contains invalid Objects", LogServer, LogDB, LogUser, LogPwd)	
				HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- Validate DBA Registry Script failed",LogServer,LogDB,LogUser,LogPwd)
			if len(FTNS)==0:
				print "0"
				print "ExitDesc: All TNSNames contain valid objects and the TNSNames are  %s" %(STNS)
				ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "No Error","All TNS contains valid Objects", LogServer, LogDB, LogUser, LogPwd)	
			if (len(STNS)!=0 and len(FTNS)!=0):
				print "0"
				print "ExitDesc: Some TNS contains Valid objects and the TNSNames are %s" %(STNS)
				ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "No Error","Some TNS contains valid Objects", LogServer, LogDB, LogUser, LogPwd)	
		else:
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 10"
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Missing Arguments"
			print "10"
			print "ExitDesc: Missing Arguments" 
except socket.error:
	with open(OFile,'a') as of1:
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1"
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Connectivity to server %s failed" %address
	print "1"
	print "ExitDesc: Connectivity to server %s failed" %address
	HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- Validate DBA Registry Script failed",LogServer,LogDB,LogUser,LogPwd)
except:
	with open(OFile, 'a') as of1:
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- Validate DBA Registry Script failed",LogServer,LogDB,LogUser,LogPwd)
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 1"
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	print "1"
	print "ExitDesc: Script Failed due to ", sys.exc_info()[1]

finally:
	s.close()
	