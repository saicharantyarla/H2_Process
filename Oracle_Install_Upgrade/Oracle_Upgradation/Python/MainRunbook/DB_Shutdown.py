"""
	Name: Oracle_DB_Shutdown.py
	Description: Executed from HP OO, to Oracle_DB_Shutdown
	Team: Software Service Automation
	Author: Gaurav Pandey(gaurav.a.pandey@capgemini.com
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
    filename = "Oracle_DB_Shutdown.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Upgradation"
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
ActivityName = "Oracle DB ShutDown"
Des = "Script shutdowns the Database"
s = socket.socket()

if len(sys.argv) == 12:
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
        oracle_sid=sys.argv[11]
        CIServer = Hostname
        address = Hostname
        port = 22 

        #Connectivity Test #
        ActivityLogger.InsertActivityLog(APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
        HLStatus.UpdateHLStatus(APID,"Stepid100","In Progress","Oracle Upgradation Environment Setup is in Progress which is executing DB shutdown script",LogServer,LogDB,LogUser,LogPwd)	 	
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)

        cmd = "export ORACLE_HOME={0}\nexport ORACLE_SID={1}\nPATH=$PATH:$ORACLE_HOME/bin\nsqlplus / as sysdba <<EOF\nshutdown immediate\nEOF\n".format(oracle_home,oracle_sid)
        #print cmd
        log.info('Executing the command : {0}'.format(cmd))
        stdin, stdout, stderr = dssh.exec_command(cmd)
        out = stdout.read()
        err=stderr.read()
        if err!="":
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Failed to shutdown the db",LogServer,LogDB,LogUser,LogPwd)
            HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Shutdown Database Script failed",LogServer,LogDB,LogUser,LogPwd)	
            log.info('10')
            log.info('ExitDesc: failed to shutdown:{0}'.format(err))
            print "10"
            print "ExitDesc: Shutdown is failed Please check logs"
        else:
            #print out
            cmd = "export ORACLE_HOME={0}\nexport ORACLE_SID={1}\nPATH=$PATH:$ORACLE_HOME/bin\nsqlplus / as sysdba <<EOF\nEOF\n".format(oracle_home,oracle_sid)
            #print cmd
            log.info('Executing the command : {0}'.format(cmd))
            stdin, stdout, stderr = dssh.exec_command(cmd)
            out = stdout.read()
            err=stderr.read()
            if err!="":
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Failed to shutdown the db",LogServer,LogDB,LogUser,LogPwd)
                HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Shutdown Database Script failed",LogServer,LogDB,LogUser,LogPwd)	
                log.info('10')
                log.info('ExitDesc: failed to shutdown:{0}'.format(err))
                print "10"
                print "ExitDesc: Shutdown is failed Please check logs"
            else:
                log.info('Output : {0}'.format(out))
                if "Connected to an idle instance." in out:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Database is shutdown",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc: Given Database shutdown is succesfull')
                    print "0"
                    print "ExitDesc: Given Database shutdown is succesfull"

                else:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Database is not shutdown",LogServer,LogDB,LogUser,LogPwd)
                    HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Shutdown Database Script failed",LogServer,LogDB,LogUser,LogPwd)	
                    log.info('10')
                    log.info('ExitDesc: Given Database shutdown is unsuccesfull')
                    print "10"
                    print "ExitDesc: Given Database shutdown is unsuccesfull"
    except Exception, e:
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error",LogServer,LogDB,LogUser,LogPwd)
        log.info('Error: {0}'.format(e))
        print "1"
        print "ExitDesc:Error. Please see logs for more details"
        HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Shutdown Database Script failed",LogServer,LogDB,LogUser,LogPwd)	
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('10')
    log.info('ExitDesc: Missing Arguments')