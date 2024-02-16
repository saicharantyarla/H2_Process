"""
	Name: OracleBinary install.py
	Description: Executed from Framework a script based solution, it will install ORACLE binary
	Team: Software Service Automation
	Inputs: Arguments [Hostname,Osusername,Ospassword,Databasename]
	Output: ExitCode, ExitDesc(Log File)
"""

#!/usr/bin/env python
from sys import path
import sys
from Logger import Logger
import Logger as log
import time
import datetime
from os import system, getcwd, path, makedirs
import paramiko
import os

if len(sys.argv) == 6:
	Execution_Location=sys.argv[1]
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	
	################################### Creating Log File ###############################
	try:
			if os.name == 'nt':
					logdir = os.getcwd()+"\\logs"
			if os.name == 'posix':
					logdir = os.getcwd()+"/logs"

			logfile = "Oracle_Binary_inst_%s.log"%HostName
			log = Logger(logdir,logfile)

			log.info('*************************************************************************')

			log.info('Started Script Execution')

	except Exception, e:
			print "ExitCode: 10"
			print "ExitDesc: Unable to create Logfile {0}".format(logfile)	
	############################## End of LogFile Creation ################################
	
	try:
		log.info("The script started execution")
		def a():				
			Ora_version=raw_input("""Please Enter option for the Oracle version you want to install in Linux
				A:12.1.02
				B:11.2.0.4
				C:Exit:""")
			Ora_version=Ora_version.upper()
			if len(Ora_version) == 1 and Ora_version.isalpha() == True:
				
				if "A" in Ora_version or "B" in Ora_version:
					
					dict={'A' : "12.1.02",
						  'B' : "11.2.0.4" ,
						  'C' : "exit"}

					Oracle_version=dict[Ora_version]
					
					return Oracle_version
				elif "C" in Ora_version:
					print("User Terminated session")
					exit()
				else:
					print("enter proper input:")
					Oracle_version=a()
					return Oracle_version
			else:
				print("enter proper input:")
				Oracle_version=a()
				return Oracle_version
		def isfloat(value):
			try:
				float(value)
				return True
			except ValueError:
				return False
		Oracle_version=a()
		log.info("Trying to connect the target host %s"%HostName)
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(HostName, username=OSUser, password=OSPassword)
		log.info("The connection is successful")	
		loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
		if Oracle_version=="12.1.02":
			res=Kernel_Param_check.rpm_package_availability(HostName,OSUser,OSPassword)
			if "success" in res:
				log.info("RPM packages check successful")
				log.info("Verifying kernel parameter values for installation")
				res1=Kernel_Param_check.Kernel_Param_check(HostName,OSUser,OSPassword)
				if "success" in res1:
					log.info("Verifying kernel param values successful")
					log.info("Verifying Shell limits are configured for oracle user as per installation requirement")
					
					
			
				
			
					
					
					
					
					
					
					
					
					


		
	except Exception, e:
		Status="Failure. Check logs"
		print "ExitCode: 1"
		print "ExitDesc: script failed due to: {0}".format(e)
		log.info('ExitCode: 1')
		log.info('ExitDesc: script failed due to: {0}'.format(e))

else:
	print "Missing Arguments"		