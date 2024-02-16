# -*- coding: utf-8 -*-
"""
	Name: Execute catuppst.sql
	Description: Executed from HP OO, Execute catuppst.sql in ORACLE
	Team: Software Service Automation
	Inputs: Arguments [HostName,UserName,Password,OracleHomes,Databases]
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
    filename = "Oracle_Execute_catuppst.log"
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
ActivityName = "Execute preupgrade.sql"
Des = "Execute preupgrade.sql in ORACLE"
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
    HostName = sys.argv[7]  #HostName  	
    UserName = sys.argv[8] #UserName
    Password = sys.argv[9]	#Password
    OracleHomes = sys.argv[10] #Comma seperated Oracle Homes
    Databases = sys.argv[11] #Comma seprated database/TNSNames 

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

        ## Connection to the remote host ##
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(HostName,UserName))					
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Execute Catbundle",LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid101","In Progress","Oracle Upgradation is in Progress which is executing catuppst script",LogServer,LogDB,LogUser,LogPassword)	
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(HostName, username=UserName, password=Password)

        log.info('Succesfully connected  to the host {0} '.format(HostName))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesful to the host",LogServer,LogDB,LogUser,LogPassword)
        count = []
        successTNS = []
        if len(OracleHomes.split(',')) == len(Databases.split(',')):
            for i in range(len(OracleHomes.split(','))):
                database = Databases.split(',')[i]
                oracleHome = OracleHomes.split(',')[i]
                command = """. ~/.bash_profile 
export ORACLE_SID={0}
export ORACLE_HOME={1}
export PATH={1}/bin:$PATH
sqlplus / as sysdba <<EOF
@{1}/rdbms/admin/catuppst.sql;
exit;
EOF""".format(database,oracleHome)

				#print command
                log.info("Executing the command...\n{}".format(command))        
                ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to execute commnd on remote host",LogServer,LogDB,LogUser,LogPassword)
                stdin, stdout, stderr = dssh.exec_command(command)
                #exit_status = stdout.channel.recv_exit_status()
                #print exit_status
                output = stdout.read()
                error = stderr.read()

                #print "Output: \n%s" %(output)
                log.info("Output: \n=========================================\n{}".format(output))                 
                #print "Error: \n%s" %(error)
                log.error("\n{}".format(error))        
                if error == "" and "ERROR at line" not in output and "SP2-" not in output:
                    count.append(0)
                    successTNS.append(database)
                else:
                    count.append(1)

            if len(count) != 0 and 1 not in count:
                print "0"
                print "ExitDesc: catuppst.sql execution is successful!"
                print ",".join(successTNS)
                log.info('Exitcode: 0')
                log.info('ExitDesc: catuppst.sql execution is successful!')
                ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","catuppst.sql execution is successful!",LogServer,LogDB,LogUser,LogPassword)
                HLStatus.UpdateHLStatus(APID,"Stepid101","Completed","Oracle Upgradation- Upgradation Completed",LogServer,LogDB,LogUser,LogPassword)
            elif 0 in count and 1 in count:
                print "10"
                print "ExitDesc: catuppst.sql execution failed on some databases!"
                print ",".join(successTNS)
                log.info('Exitcode: 1')
                log.info('ExitDesc: catuppst.sql execution failed on some databases!')
                ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","catuppst.sql execution failed on some databases!",LogServer,LogDB,LogUser,LogPassword)
                HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- Catuppst sql Script failed",LogServer,LogDB,LogUser,LogPassword)	
            else:
                print "1"
                print "ExitDesc: catuppst.sql execution failed!"
                log.info('Exitcode: 1')
                log.info('ExitDesc: catuppst.sql execution failed!')
                ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","catuppst.sql execution failed!",LogServer,LogDB,LogUser,LogPassword)
                HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- Catuppst sql Script failed",LogServer,LogDB,LogUser,LogPassword)	
        else:
            #print "10"
            #print "ExitDesc: Oracle home and sid is not matching."
            log.info("Exitcode: 10")
            log.info("ExitDesc: Oracle home and sid is not matching.")
            ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"Error","Missing Arguments",LogServer,LogDB,LogUser,LogPassword)
            HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- Catuppst script failed",LogServer,LogDB,LogUser,LogPassword)
    except socket.error, e:
        print "10"
        print "ExitDesc: {0}".format(e)
        log.info('Exitcode: 10')
        log.info('ExitDesc: {0}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"Error",str(e),LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- Catuppst sql Script failed",LogServer,LogDB,LogUser,LogPassword)	
    except Exception, e:
        print "10"
        print "ExitDesc: {0}".format(e)
        log.info('Exitcode: 10')
        log.info('ExitDesc: {0}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"Error",str(e),LogServer,LogDB,LogUser,LogPassword)	
        HLStatus.UpdateHLStatus(APID,"Stepid101","Failed","Oracle Upgradation- Catuppst sql Script failed",LogServer,LogDB,LogUser,LogPassword)		
    finally:
        s.close()	
        dssh.close()
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info("Exitcode: 10")
    log.info("ExitDesc: Missing Arguments")