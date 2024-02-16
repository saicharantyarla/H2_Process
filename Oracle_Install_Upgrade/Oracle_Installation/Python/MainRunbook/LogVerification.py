"""
	Name: Validate Logs after Oracle Installation
	Description: Executed from HP OO, Validate Logs for catupgd.sql
	Team: Software Service Automation
	Inputs: Arguments [LogServer,LogDB,ORACLEServer,APID,LogAccountName,LogUser,LogPwd,ORACLEServer,ORACLESeUsername,ORACLESePassword], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
"""

# Modules Initializing #

from sys import path
import sys
import logging as log
import time
import datetime
from os import system,getcwd,path,makedirs
import socket
import paramiko
import os
import ActivityLogger
import HLStatus

try:
	filename = "InstallOracle_log.txt"
	filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
	filename = "%s\%s" %(filepath,filename)
	if not path.exists(filepath):
		makedirs(filepath)
	log.basicConfig(filename=filename, filemode='w', format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
	log.info('*************************************************************************')
	log.info('Started Script Execution')
except Exception, e:
	print "10"
	print "ExitDesc: Unable to create Logfile {0}".filename
# Variable Mapping #
ActivityName = "validating log"
Des = " Validating log after Oracle Installation"
a = 0
s = socket.socket()

try:

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
			   
		CIServer = ORACLEServer
		address = ORACLEServer
		port = 22
		log.info('Checking connectivity to the host : {0}'.format(ORACLEServer))	
			# Connectivity Test #
		ActivityLogger.InsertActivityLog(APID, CIServer, ActivityName, Des, "Initiated", LogAccountName, "No Error", "Connectivity check initiated", LogServer, LogDB, LogUser, LogPwd)
                HLStatus.UpdateHLStatus(APID,"Stepid98","In Progress","Oracle Installation Post Check is in Progress",LogServer,LogDB,LogUser,LogPwd)	
		s.connect((address, port))

		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Host is reachable", LogServer, LogDB, LogUser, LogPwd)
		log.info('{0} host is reachable'.format(ORACLEServer))
		log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(ORACLEServer,ORACLESeUsername))
				
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(ORACLEServer, username=ORACLESeUsername, password=ORACLESePassword)
		log.info('Succesfully connected  to the host {0} '.format(ORACLEServer))
		ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesfull to the host",LogServer,LogDB,LogUser,LogPwd)
		ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Validating  Installation log files",LogServer,LogDB,LogUser,LogPwd)
		command1="""
abc=`cat """+path+""" | grep "SEVERE"`
if [[ $abc != "" ]];then
echo $abc
fi
"""
		log.info('Executing the command :{0}'.format(command1))
		stdin, stdout, stderr = dssh.exec_command(command1)
		output1 = stdout.read()
		err = stderr.read()
		output1 = output1.strip()
		if err:
			print "1"
			print "ExitDesc: Unable to execute the command.Check the log for errors."
			log.info('Exitcode: 1')
			log.info('Error: {0}'.format(err))
			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Unable to execute the command.Check the log for errors.",LogServer,LogDB,LogUser,LogPwd)
			HLStatus.UpdateHLStatus(APID,"Stepid98","Failed","Oracle Installation Post Check failed,Check the log for errors",LogServer,LogDB,LogUser,LogPwd)	
		else:
			if len(output1) == 0:
				log.info('ExitCode: 0')
				log.info('ExitDesc: Log files are validated ,No errors')
				print "0"
				print "ExitDesc: Log files are validated ,No errors"
				ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Log Files are Validated. No error found",LogServer,LogDB,LogUser,LogPwd)
				#HLStatus.UpdateHLStatus(APID,"Stepid85","Failed","Oracle Installation Post Check failed,Check the log for errors",LogServer,LogDB,LogUser,LogPwd)	
			else:
				log.info('errors Fetched after executing the command :{0}'.format(output1))
				log.info('ExitCode: 10')
				log.info('ExitDesc: Log files are validated ,Errors found. Check the logs for error')
				print "10"
				print "ExitDesc:  Log files are validated ,Errors found. Check the logs for error"
				ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Log files are validated ,Errors found. Check the logs for error",LogServer,LogDB,LogUser,LogPwd)
				HLStatus.UpdateHLStatus(APID,"Stepid98","Failed","Oracle Installation Post Check failed,Log files are validated ,Errors found. Check the logs for error",LogServer,LogDB,LogUser,LogPwd)	
	else:
		log.info('ExitCode: 1')
		log.info('ExitDesc: Missing Arguments')
		print "1"
		print "ExitDesc: Missing Arguments"
		HLStatus.UpdateHLStatus(APID,"Stepid98","Failed","Oracle Installation Post Check failed,Missing Arguments",LogServer,LogDB,LogUser,LogPwd)	
except socket.error:
	ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
	log.info('ExitCode: 1')
	log.info('ExitDesc: Connectivity to server failed.')
	print "1"
	print "ExitDesc: Connectivity to server %s failed" %address
        HLStatus.UpdateHLStatus(APID,"Stepid98","Failed","Oracle Installation Post Check failed,Check the Log for error",LogServer,LogDB,LogUser,LogPwd)	
except:
	ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
	print "1"
	print "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	log.info('ExitCode: 1')
	log.info('ExitDesc: Check the log for errors.')

finally:
	s.close()	
