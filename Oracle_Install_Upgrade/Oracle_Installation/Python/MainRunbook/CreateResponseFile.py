"""
	Name: Create Response File
	Description: Executed from HP OO, Creates a response file for silent installation of ORACLE
	Team: Software Service Automation
	Inputs: Arguments [Hostname,OSUsername,OSPassword,AllParametersToCreateFile], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
	
"""
# Modules Initializing #
from sys import path
import sys
import logging as log
import time
import datetime
from os import system,getcwd,path,makedirs
import subprocess
import socket
import paramiko
import ActivityLogger
import HLStatus

# Workflow engine log module Initializing

OFol="C:\Python_Logs\ORACLE_Installation";
OFile=OFol + "\\" + 'CreateResponseFile';
try:
	filename = "CreateResponseFile.txt"
	filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
	filename = "%s\%s" %(filepath,filename)
	OFile=filename
	if not path.exists(filepath):
		makedirs(filepath)
	log.basicConfig(filename=filename, filemode='w', format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
	log.info('*************************************************************************')
	log.info('Started Script Execution')
except Exception, e:
	print "Unable to create Logfile {0}".format(filename)

# Variable Mapping #
ActivityName = "Create Response File";
Des = "Creating Response File for Silent Installation of Oracle";
a=0
s = socket.socket()
try:
	log.info('Input Variables mapping...')
	# Arguments Mapping #
	if len(sys.argv) == 18 :
		##Log Variables##
		LogServer = sys.argv[1]
		LogDB = sys.argv[2]
		APID = sys.argv[3]
		LogAccountName = sys.argv[4]
		LogUser = sys.argv[5]
		LogPwd = sys.argv[6]
		##Script Variables##
		Hostname = sys.argv[7]  #Target HostName  	
		OsUser = sys.argv[8]	#Target Database user to connect to listener
		OsPass = sys.argv[9]	#Target Database user password to connect to listener
		OraHome =sys.argv[10]	#Target TNS Name
		OraBase=sys.argv[11]
		InvLoc=sys.argv[12]
		DBAGN=sys.argv[13]
		OPERGN=sys.argv[14]
		DGDBAGN=sys.argv[15]
		KMDBAGN=sys.argv[16]
		BACKUPDBAGN=sys.argv[17]
		CIServer = Hostname
		address = Hostname
		port = 22 

		#Connectivity Test #
		ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
		log.info('Checking connectivity to the host : {0}'.format(Hostname))
		HLStatus.UpdateHLStatus(APID,"Stepid96","In Progress","Oracle Response file Configuration is in Progress",LogServer,LogDB,LogUser,LogPwd)
		s.connect((address, port)) 
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Host is reachable", LogServer, LogDB, LogUser, LogPwd)
		log.info('{0} host is reachable'.format(Hostname))
		FileContent='oracle.install.responseFileVersion=/oracle/install/rspfmt_dbinstall_response_schema_v12.1.0\noracle.install.option=INSTALL_DB_SWONLY\nUNIX_GROUP_NAME=oinstall\n'
		FileContent=FileContent+'INVENTORY_LOCATION='+InvLoc+'\n'+'ORACLE_HOME='+OraHome+'\n'+'ORACLE_BASE='+OraBase+'\n'+'oracle.install.db.InstallEdition=EE\nSELECTED_LANGUAGES=en\n'
		FileContent=FileContent+'oracle.install.db.DBA_GROUP='+DBAGN+'\n'+'oracle.install.db.OPER_GROUP='+OPERGN+'\n'+'oracle.install.db.DGDBA_GROUP='+DGDBAGN+'\n'+'oracle.install.db.KMDBA_GROUP='+KMDBAGN+'\n'
		FileContent=FileContent+'oracle.install.db.BACKUPDBA_GROUP='+BACKUPDBAGN+'\nDECLINE_SECURITY_UPDATES=true'
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(Hostname, username=OsUser, password=OsPass)
		command1='pwd'
		log.info('Executing command : {0}'.format(command1))
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Fetching the directory", LogServer, LogDB, LogUser, LogPwd)
		stdin, stdout, stderr = dssh.exec_command(command1)
		output = stdout.read()
		if stderr.read():
			print "1"
			print "ExitDesc: Check the logs for errors"
			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "Check the log for errors", LogServer, LogDB, LogUser, LogPwd)
			HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Response file Configuration Script Failed Check Logs",LogServer,LogDB,LogUser,LogPwd)
			log.info('ExitCode: 1')
			log.info('ExitDesc : {0}'.format(stderr.read()))
		else:
			FP=output.strip()+'/Response.rsp'
			command2='echo '+'"'+FileContent+'"' + ' >'+FP 
			log.info('Executing command : {0}'.format(command2))
			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Adding content to the file", LogServer, LogDB, LogUser, LogPwd)
			stdin, stdout, stderr = dssh.exec_command(command2)
			command3="test -e "+FP+";echo $?"
			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Checking the file existence", LogServer, LogDB, LogUser, LogPwd)
			if stderr.read():
				ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "Check the log for errors", LogServer, LogDB, LogUser, LogPwd)
				print "1"
				print "ExitDesc: Check the logs for errors"
				log.info('ExitCode: 1')
				log.info('ExitDesc : {0}'.format(stderr.read()))
				HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Response file Configuration Script Failed Check Logs",LogServer,LogDB,LogUser,LogPwd)
			else:
				log.info('Executing command : {0}'.format(command3))
				stdin, stdout, stderr = dssh.exec_command(command3)
				ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Fetching the size of created file", LogServer, LogDB, LogUser, LogPwd)
				op=stdout.read()
				if op.strip() == "0":
					command4="du "+FP+" | cut -f 1"
					log.info('Executing command : {0}'.format(command4))
					stdin, stdout, stderr = dssh.exec_command(command4)
					output = stdout.read()
					if output.strip() == "0":
						ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "No content added to the file", LogServer, LogDB, LogUser, LogPwd)
						print "1"
						print "ExitDesc: No Content in the file."
						log.info('ExitCode: 1')	
						log.info('ExitDesc: No content in the file')
						HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Response file Configuration Script Failed, No Content in the file",LogServer,LogDB,LogUser,LogPwd)
					elif stderr.read():
						ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "Check the log for errors", LogServer, LogDB, LogUser, LogPwd)
						print "1"
						print "ExitDesc: Check the logs for errors"
						log.info('ExitCode: 1')
						log.info('ExitDesc : {0}'.format(stderr.read()))
						HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Response file Configuration Script Failed, Check the logs for errors",LogServer,LogDB,LogUser,LogPwd)
					else:
						print "0"
						print "ExitDesc: Response file created and content added"
						print FP
						log.info('ExitCode: 0')
						log.info('ExitDesc : Response File created and content added')	
						ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"No Error", "Response File created and added", LogServer, LogDB, LogUser, LogPwd)
				elif stderr.read():
					ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "Check the log for errors", LogServer, LogDB, LogUser, LogPwd)
					print "1"
					print "ExitDesc: Check the logs for errors"
					log.info('ExitCode: 1')
					log.info('ExitDesc : {0}'.format(stderr.read()))
					HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Response file Configuration Script Failed, Check the logs for errors",LogServer,LogDB,LogUser,LogPwd)
					
				else:
					print "1"
					print "ExitDesc: File Creation Failed"
					log.info('ExitCode: 1')
					log.info('ExitDesc : File Creation Failed')	
					ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "File Creation Failed", LogServer, LogDB, LogUser, LogPwd)
					HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Response file Configuration Script Failed, File Creation Failed",LogServer,LogDB,LogUser,LogPwd)
	else:
		log.info('ExitCode: 10')
		log.info('ExitDesc : Missing Arguments')
		print "10";
		print "ExitDesc: Missing Arguments";
except socket.error:
	ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "Invalid server IP address", LogServer, LogDB, LogUser, LogPwd)
	log.info('Exitcode: 10')
	log.info('ExitDesc: Invalid server ip addres')
	print "10"
	print "ExitDesc: script failed due to Invalid server ip address %s" %address
	HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Response file Configuration Script Failed, Invalid server ip addres",LogServer,LogDB,LogUser,LogPwd)
	
except :
	log.info('ExitCode: 1')
	log.info('ExitDesc : {0}'.format(sys.exc_info()[1]))	
	print "1";
	print "ExitDesc: Check the log for errors"
	ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", "Check the log for errors", LogServer, LogDB, LogUser, LogPwd)
	HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Response file Configuration Script Failed, Check the logs for errors",LogServer,LogDB,LogUser,LogPwd)
	
finally:
	s.close()
