# -*- coding: utf-8 -*-
"""
	Name: Execute catupgd.sql
	Description: Executed from HP OO, Execute catupgd.sql in ORACLE
	Team: Software Service Automation
	Author: Vikrant Kumar (vikrant.a.kumar@capgemini.com)
	Inputs: Arguments [HostName,UserName,Password,OracleHome]
	Output: ExitCode, ExitDesc(Log File)"""

# Modules Initializing #
import datetime
import sys
import socket
import paramiko
import logging as log
from os import system,getcwd,path,makedirs
import ActivityLogger
import HLStatus
try:
    filename = "Oracle_Execute_catupgd.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Upgradation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".format(filename)
    print str(e)

# Variable Mapping #
ActivityName = "Execute catupgd.sql"
Des = "Execute catupgd.sql in ORACLE"
s = socket.socket()

log.info('Input Variables mapping...')
# Arguments Mapping #
if len(sys.argv) == 12:
    ##Log Variables##
    LogServer = sys.argv[1]
    LogDB = sys.argv[2]
    APID = sys.argv[3]
    LogAccountName = sys.argv[4]
    LogUser = sys.argv[5]
    LogPassword = sys.argv[6]

    ##Script Variables##
    HostName = sys.argv[7] #HostName  	
    UserName = sys.argv[8] #UserName
    Password = sys.argv[9] #Password
    OracleHome = sys.argv[10] #Oracle Home
    TNS_List = sys.argv[11] #Oracle Home
    CIServer = HostName
    address = HostName
    port = 22 			

    #Connectivity Test #
    ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPassword)
    log.info('Checking connectivity to the host : {0}'.format(HostName))
    try:
        s.connect((address, port)) 
        log.info('{0} host is reachable'.format(HostName))		
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid101","In Progress","Oracle Upgradation is in Progress which is executing Catupgd script",LogServer,LogDB,LogUser,LogPassword)	
        ## Connection to the remote host ##
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(HostName,UserName))
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to take remote session.",LogServer,LogDB,LogUser,LogPassword)

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(HostName, username=UserName, password=Password)

        log.info('Succesfully connected  to the host {0} '.format(HostName))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesful to the host",LogServer,LogDB,LogUser,LogPassword)
        command = """. ~/.bash_profile
export ORACLE_SID={1}
export ORACLE_HOME={0}
export PATH=$ORACLE_HOME/bin:$PATH
cd $ORACLE_HOME/rdbms/admin
$ORACLE_HOME/perl/bin/perl catctl.pl -n 4 catupgrd.sql""".format(OracleHome,TNS_List)

        #print command

        log.info("Executing the command...\n{}".format(command))        
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to execute commnd on remote host",LogServer,LogDB,LogUser,LogPassword)
        stdin, stdout, stderr = dssh.exec_command(command)
        output = stdout.read()
        error = stderr.read()
		
        #print "Output: \n{0}".format(output)
        #print "="*45
        #print "Error: \n{0}".format(error)
        log.info("Error: \n{0}".format(error))
		
        if "Unexpected error encountered" not in error.strip():
            print "0"
            print "ExitDesc: catupgd.sql execution is successful!"
            log.info('Exitcode: 0')
            log.info('ExitDesc: catupgd.sql execution is successful!')
            ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","catupgd.sql execution is successful!",LogServer,LogDB,LogUser,LogPassword)			
        else:
            print "1"
            print "ExitDesc: catupgd.sql execution failed!"
            log.info('Exitcode: 1')
            log.info('ExitDesc: catupgd.sql execution failed!')
            ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","catupgd.sql execution failed!",LogServer,LogDB,LogUser,LogPassword)
            HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- Catupgd sql Script failed",LogServer,LogDB,LogUser,LogPassword)
    except socket.error, e:
        print "10"
        print "ExitDesc: Exception Failure.Check the log for errors."
        log.info('Exitcode: 10')
        log.info('ExitDesc: {0}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"Error","Exception Failure.Check the log for errors",LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- Catupgd sql Script failed",LogServer,LogDB,LogUser,LogPassword)
    except Exception, e:
        print "10"
        print "ExitDesc: Exception Failure.Check the log for errors."
        log.info('Exitcode: 10')
        log.info('ExitDesc: {0}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"Error","Exception Failure.Check the log for errors",LogServer,LogDB,LogUser,LogPassword)	
        HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- Catupgd sql Script failed",LogServer,LogDB,LogUser,LogPassword)
    finally:
        s.close()	
        dssh.close()
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info("Exitcode: 10")
    log.info("ExitDesc: Missing Arguments")