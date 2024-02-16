
"""
	Name: set_orahome_start_db.py
	Description: Executed from HP OO, to set_orahome_start_db
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
    filename = "StartDBUpgrade.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Upgradation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.getLogger("paramiko").setLevel(log.INFO)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".format(filename)

# Variable Mapping #
ActivityName = "Start DB(12) in Upgrade mode"
Des = "Set 12 ORACLE_HOME and start DB in Upgrade mode"
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
        OracleHomeList=sys.argv[10]
        TNSName=sys.argv[11]
        if "," in OracleHomeList:
            OracleHomeList=OracleHomeList.split(",")
        CIServer = Hostname
        address = Hostname
        orahomes=""
        port = 22 
        #Connectivity Test #
        ActivityLogger.InsertActivityLog(APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
        HLStatus.UpdateHLStatus(APID,"Stepid100","In Progress","Oracle Upgradation Environment Setup is in Progress which is executing to Start DB in Upgrade script",LogServer,LogDB,LogUser,LogPwd)	 	
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)

        def set_orahome(oraclehome):
            count=1
            command="export ORACLE_HOME={0}\nexport ORACLE_SID={1}\nexport PATH=$PATH:$ORACLE_HOME/bin\nsqlplus /nolog <<EOF \n conn / as sysdba;\nstartup upgrade;\nexit; \nEOF\n".format(oraclehome,TNSName)
            log.info('Executing the command : {0}'.format(command))
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            log.info('Output  : {0}'.format(output))
            output = output.split("\n")
            for i in range(len(output)):
                if "cannot start already-running" in output[i]:
                    count = -1
                if "instance started" in output[i]:
                    count = 0
            log.info("Count : {0}".format(count))
            count = int(count)
            if count == 0:
                return "True"
            elif count == -1:
                return "Started"
            else:
                return "False"


        if isinstance(OracleHomeList, list):
            for bin in OracleHomeList:
                out=set_orahome(bin)
                if out == "True":
                    orahomes=orahomes+bin+","
            orahomes=orahomes.rstrip(",")

        else:
            out=set_orahome(OracleHomeList)

        if out == "True":
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","DB started in Upgrade mode Succesfully",LogServer,LogDB,LogUser,LogPwd)
            HLStatus.UpdateHLStatus(APID,"Stepid100","Completed","Oracle Upgradation- Environmental Setup completed successfully",LogServer,LogDB,LogUser,LogPwd)	
            log.info('0')
            log.info('ExitDesc: DB started in Upgrade mode Succesfully')
            print "0"
            print "ExitDesc: Set DB started in Upgrade mode Succesfully"

        elif out == "Started":
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Database already started",LogServer,LogDB,LogUser,LogPwd)
            log.info('0')
            log.info('ExitDesc:Database already started')
            print "0"
            print "ExitDesc: Database already started"
            HLStatus.UpdateHLStatus(APID,"Stepid100","Completed","Oracle Upgradation- Environmental Setup completed successfully",LogServer,LogDB,LogUser,LogPwd)	

        else:
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Set ORACLE_HOME and start DB in Upgrade mode Failed",LogServer,LogDB,LogUser,LogPwd)
            log.info('10')
            log.info('ExitDesc: Starting DB in Upgrade mode Failed')
            print "10"
            print "ExitDesc: Starting DB in Upgrade mode Failed"
            HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Start DB in Upgrade Script failed",LogServer,LogDB,LogUser,LogPwd)	
        if orahomes:
            print orahomes


    except Exception, e:
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error, see logs for more details",LogServer,LogDB,LogUser,LogPwd)
        HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Start DB in Upgrade Script failed",LogServer,LogDB,LogUser,LogPwd)	
        log.info('Error: {0}'.format(e))
        print "1"
        print "ExitDesc: Error, see logs for more details"

else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('10')
    log.info('ExitDesc: Missing Arguments')