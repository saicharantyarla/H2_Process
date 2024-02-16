"""
	Name: Validating parameters in limits.conf file
	Description: Executed from HP OO, Estimate datafile size in oracle
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
import os
OFol = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
OFile = OFol + "\\" + 'oracle_Inventory_validation.log'
# Variable Mapping #
ActivityName = "Validating ORACLE_Inv path"
Des = " Validating ORACLE_Inv path "
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
			path = sys.argv[10]
			trueout = ""
			falseout = ""
			#DbUser = sys.argv[10]  # Target Database user to connect to listener
			#ORACLEDBPassword = sys.argv[11]  # Target Database user password to connect to listener
			   
			CIServer = ORACLEServer
			address = ORACLEServer
			port = 22
			
			# Connectivity Test #
			HLStatus.UpdateHLStatus(APID,"Stepid96","In Progress","Oracle Inventory Validation Script Run is in Progress",LogServer,LogDB,LogUser,LogPwd)
			ActivityLogger.InsertActivityLog(APID, CIServer, ActivityName, Des, "Initiated", LogAccountName, "No Error", "Connectivity check initiated", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Checking connectivity for", ORACLEServer

			s.connect((address, port))

			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Host is reachable", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ":", ORACLEServer, "is reachable "
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Estimate datafile size "

			## Database Connection String ##
				
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(ORACLEServer, username=ORACLESeUsername, password=ORACLESePassword)
			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesfull to the host",LogServer,LogDB,LogUser,LogPwd)

			#log.info('Executing the command :{0}'.format(command))
			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Validating ORACLE_Inv path",LogServer,LogDB,LogUser,LogPwd)
			#print "hi"

			#command1="grep -E 'oracle' /etc/security/limits.conf | grep soft | grep nproc | awk '{print $4}'"	
			command1 = """if [ -d """+path+""" ]; then
						echo "Yes"
					else
						echo "No"
					fi"""
			stdin, stdout, stderr = dssh.exec_command(command1)
			output1 = stdout.read()
			errout = stderr.read()
			#print command1
			output1=output1.strip()
			#print output1
			if output1 == "No":
                                #print output1
				#print "path doesnot exists creating the path"
				command2 = " mkdir -p %s " %path
				#print command2
				stdin, stdout, stderr = dssh.exec_command(command2)
				output2 = stdout.read()
				#print output2
				
				command1 = """if [ -d """+path+""" ]; then
							echo "Yes"
						else
							echo "No"
						fi"""
				stdin, stdout, stderr = dssh.exec_command(command1)
				output2 = stdout.read()
				errout = stderr.read()
				output2 = output2.strip()
				if output2 == "Yes":
					
					print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "The ORACLE_Inv path successfully validated"
					ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"No Error", "The ORACLE_Inv path successfully validated", LogServer, LogDB, LogUser, LogPwd)
					#HLStatus.UpdateHLStatus(APID,"Stepid26","Completed","Validating ORACLE_HOME path completed successfully.")
					print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 0 \n"
					print "0"
					print "ExitDesc: The ORACLE_Inv path successfully validated"
					HLStatus.UpdateHLStatus(APID,"Stepid96","Completed","Oracle Installation Environmetal Setup Step Completed",LogServer,LogDB,LogUser,LogPwd)
				
				else:
					
					print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "unable to create ORACLE_Inv path "
					ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "unable to create ORACLE_Inv path ", LogServer, LogDB, LogUser, LogPwd)
					#HLStatus.UpdateHLStatus(APID,"Stepid26","Completed","unable to create ORACLE_HOME path.")
					print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 10 \n"
					print "10"
					print "ExitDesc: unable to create ORACLE_HOME path "
					HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Inv Validation Script Failed, unable to create ORACLE_Inv path",LogServer,LogDB,LogUser,LogPwd)
			else:
				
				print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "The ORACLE_Inv path successfully validated"
				ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"No Error", "The ORACLE_Inv path successfully validated", LogServer, LogDB, LogUser, LogPwd)
				#HLStatus.UpdateHLStatus(APID,"Stepid26","Completed","Validating ORACLE_HOME path completed successfully.")
				print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 0 \n"
				print "0"
				print "ExitDesc: The ORACLE_inv path successfully validated"
				HLStatus.UpdateHLStatus(APID,"Stepid96","Completed","Oracle Installation Environmetal Setup Step Completed",LogServer,LogDB,LogUser,LogPwd)
		else:
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 10"
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Missing Arguments"
			print "10"
			print "ExitDesc: Missing Arguments"
			HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Inv Validation Script Failed, Missing Arguments",LogServer,LogDB,LogUser,LogPwd)
except socket.error:
	with open(OFile,'a') as of1:
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1"
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Connectivity to server %s failed" %address
	print "1"
	print "ExitDesc: Connectivity to server %s failed" %address
        HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Inv Validation Script Failed, Connectivity to server failed",LogServer,LogDB,LogUser,LogPwd)
except:
	with open(OFile, 'a') as of1:
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		# HLStatus.UpdateHLStatus(APID,"Stepid26","Failed","Validating limits.conf file failed.")
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 1"
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	print "1"
	print "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Inv Validation Script Failed, Some Exception Check Logs",LogServer,LogDB,LogUser,LogPwd)

finally:
	s.close()
	
