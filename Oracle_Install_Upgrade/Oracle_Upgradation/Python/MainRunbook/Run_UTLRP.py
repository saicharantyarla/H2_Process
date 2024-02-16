"""
	Name: Run_UTLRP.py
	Description: Executed from HP OO, to Run_UTLRP
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
    filename = "Run_UTLRP.log"
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
ActivityName = "Run UTLRL"
Des = "Executes UTLRP and checks for successful execution"
s = socket.socket()

if len(sys.argv) == 13:
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
        Stepid=sys.argv[12]
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
        HLStatus.UpdateHLStatus(APID,Stepid,"In Progress","Oracle Upgradation Pre Check is in Progress which is executing UTLRP script",LogServer,LogDB,LogUser,LogPwd)			
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)

        def run_utlrp(oraclehome):
            command="export ORACLE_HOME={0}\nexport ORACLE_SID={1}\nexport PATH=$ORACLE_HOME/bin:$PATH\nsqlplus /nolog <<EOF;\nconn / as sysdba;\n@{0}/rdbms/admin/utlrp.sql; \nexit; \nEOF\n".format(oraclehome,TNSName)
            log.info('Executing the command : {0}'.format(command))
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            log.info('Output  : {0}'.format(output))
            output = output.split("\n")
            for i in range(len(output)):
                if "ERRORS DURING RECOMPILATION" in output[i]:
                    log.info("#####*****After parsing output*****#####")
                    log.info("{0}".format(output[i]))
                    log.info("{0}".format(output[i+1]))
                    log.info("{0}".format(output[i+2]))
                    count = output[i+2]
            count = int(count)
            if count == 0:
                return "True"
            else:
                return "False"

        if isinstance(OracleHomeList, list):
            for bin in OracleHomeList:
                out=run_utlrp(bin)
                if out == "True":
                    orahomes=orahomes+bin+","
            orahomes=orahomes.rstrip(",")

        else:
            out=run_utlrp(OracleHomeList)

        if out == "True":
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","UTLRP Run Succesfull",LogServer,LogDB,LogUser,LogPwd)
            log.info('0')
            log.info('ExitDesc: UTLRP Run Succesfull')
            print "0"
            print "ExitDesc: UTLRP Run Succesfull"



        else:
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","UTLRP Run Failed",LogServer,LogDB,LogUser,LogPwd)
            log.info('10')
            log.info('ExitDesc: UTLRP Run Failed')
            print "10"
            print "ExitDesc: UTLRP Run Failed"
            HLStatus.UpdateHLStatus(APID,Stepid,"Failed","Oracle Upgradation- UTLRP Script failed",LogServer,LogDB,LogUser,LogPwd)
        if orahomes:
            print orahomes




    except Exception, e:
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error, see logs for more details",LogServer,LogDB,LogUser,LogPwd)
        log.info('Error: {0}'.format(e))
        print "1"
        print "ExitDesc: Error, see logs for more details"
        HLStatus.UpdateHLStatus(APID,Stepid,"Failed","Oracle Upgradation- UTLRP Script failed",LogServer,LogDB,LogUser,LogPwd)
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('10')
    log.info('ExitDesc: Missing Arguments')
