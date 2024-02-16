"""
	Name: Oracle_Connection_Check.py
	Description: Executed from HP OO, to Oracle_Connection_Check
	Team: Software Service Automation
	Author: Vinaykumar Kalyankar(Vinay.Kalyankar@capgemini.com)
	Inputs: Arguments [Hostname,Username,Password,Directory_Name], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
	
"""

#!/usr/bin/env python
from sys import path
import sys
import logging as log
import time
import datetime
from os import system,getcwd,path,makedirs
import paramiko
import os
import ActivityLogger
import socket
import HLStatus
try:
    filename = "Oracle_Connection_Check.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.getLogger("paramiko").setLevel(log.INFO)
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".format(filename)

# Variable Mapping #
ActivityName = "Oracle Connection Post Check"
Des = "Oracle Connection Post Check"
s = socket.socket()

if len(sys.argv) == 11:
    try:
        log.info('Input Variables mapping...')
        LogServer = sys.argv[1]
        LogDB = sys.argv[2]
        APID = sys.argv[3]
        LogAccountName = sys.argv[4]
        LogUser=sys.argv[5]
        LogPwd=sys.argv[6]
        ##Script Variables##
        Hostname = sys.argv[7]  #Target HostName  	
        osuser = sys.argv[8]	#Target Host user name to connect 
        ospassword = sys.argv[9]	#Target Host user password to connect
        oracle_home = sys.argv[10]	#ORACLE_HOME value
        CIServer = Hostname
        address = Hostname
        port = 22 

        #Connectivity Test #
        ActivityLogger.InsertActivityLog(APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))
        HLStatus.UpdateHLStatus(APID,"Stepid98","In Progress","Oracle Installation Post Check is in Progress,Oracle Connection Check",LogServer,LogDB,LogUser,LogPwd)	
        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)

        cmd = "export ORACLE_HOME={0}\nexport PATH=$PATH:$ORACLE_HOME/bin\nsqlplus /nolog <<EOF\nexit; \nEOF\n".format(oracle_home)

        log.info('Executing the command : {0}'.format(cmd))
        stdin, stdout, stderr = dssh.exec_command(cmd)
        out = stdout.read()

        log.info('Output : {0}'.format(out))
        if out:
            version = oracle_home.split("/")[-2]
            if version in out:
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Oracle Connection Check Succesfull",LogServer,LogDB,LogUser,LogPwd)
                log.info('0')
                log.info('ExitDesc: Oracle Connection Check Succesfull')
                print "0"
                print "ExitDesc: Oracle Connection Check Succesfull for %s"%version
                HLStatus.UpdateHLStatus(APID,"Stepid98","Completed","Oracle Installation Post Check is Succesfull",LogServer,LogDB,LogUser,LogPwd)	
            else:
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Oracle Connection Check Failed",LogServer,LogDB,LogUser,LogPwd)
                log.info('10')
                log.info('ExitDesc: Oracle Connection Check Failed')
                print "10"
                print "ExitDesc: Oracle Connection Check Failed"
                HLStatus.UpdateHLStatus(APID,"Stepid98","Failed","Oracle Installation Post Check is failed,please check logs",LogServer,LogDB,LogUser,LogPwd)	
        else:
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Oracle Connection Check Failed",LogServer,LogDB,LogUser,LogPwd)
            log.info('10')
            log.info('ExitDesc: Oracle Connection Check Failed')
            print "10"
            print "ExitDesc: Oracle Connection Check Failed"
            HLStatus.UpdateHLStatus(APID,"Stepid98","Failed","Oracle Installation Post Check is failed, please check logs",LogServer,LogDB,LogUser,LogPwd)	



    except Exception, e:
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error",LogServer,LogDB,LogUser,LogPwd)
        log.info('Error: {0}'.format(e))
        print "1"
        print "ExitDesc:Error. Please see logs for more details"
        HLStatus.UpdateHLStatus(APID,"Stepid98","Failed","Oracle Installation Post Check is failed,Please see logs for more details",LogServer,LogDB,LogUser,LogPwd)	

else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('10')
    log.info('ExitDesc: Missing Arguments')
