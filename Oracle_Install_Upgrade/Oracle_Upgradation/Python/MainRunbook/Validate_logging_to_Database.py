"""
	Name: Oracle Upgraded DB Version Validation 
	Description: Executed from JBPM to Validate Oracle DB Upgraded Version
	Team: Software Service Automation
	Inputs: Arguments [HostName,DBUsername,DBPassword,OracleHomes,TNSNames], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)	
"""
# Modules Initializing #
import datetime
import sys
import socket
import cx_Oracle as dbc
from os import system,getcwd,path,makedirs
import logging as log
import paramiko
import ActivityLogger
import HLStatus
try:
    filename = "Oracle_Upgraded_DB_Version_Validation.log"
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
ActivityName = "Upgraded DB Version validation"
Des = "Validate the upgraded DB Version by logging in."
s = socket.socket()


log.info("Arguments Mapping")
if len(sys.argv) == 12:
    #Log Variables
    LogServer = sys.argv[1]
    LogDB = sys.argv[2]
    APID = sys.argv[3]
    LogAccountName = sys.argv[4]
    LogUser = sys.argv[5]
    LogPassword=sys.argv[6]

	##Script Variables##
    HostName = sys.argv[7] #Target HostName  	
    UserName = sys.argv[8] #Target Database user to connect to listener
    Password = sys.argv[9] #Target Database user password to connect to listener
    OracleHomes = sys.argv[10] #Database Homes
    TNSNames = sys.argv[11] #Target TNS Names

    address = HostName
    CIServer = address
    port = 22

    #Connectivity Test #
    log.info("Checking connectivity for {0}".format(HostName))
    ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPassword)
    try:
        s.connect((address, port)) 
        log.info("{0} is rechable".format(HostName))
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPassword)

        ## Connection to the remote host ##
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(HostName,UserName))
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to take remote session.",LogServer,LogDB,LogUser,LogPassword)		
        HLStatus.UpdateHLStatus(APID,"Stepid102","In Progress","Oracle Post Check is in Progress which is executing Validate By Logging to Database script",LogServer,LogDB,LogUser,LogPassword)		
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(HostName, username=UserName, password=Password)	

        log.info('Succesfully connected  to the host {0} '.format(HostName))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesful to the host",LogServer,LogDB,LogUser,LogPassword)

        def execScript(command):
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            error = stderr.read()
            return output+"\n"+error
		
        if len(OracleHomes.split(',')) == len(TNSNames.split(',')):
            successTNS = []
            statusList = []
            log.info("Executing the command...")        
            ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to execute commnd on remote host",LogServer,LogDB,LogUser,LogPassword)
            for i in range(len(OracleHomes.split(','))):
                OracleHome = OracleHomes.split(',')[i]
                SID = TNSNames.split(',')[i]
                command = """export ORACLE_SID={1}
export ORACLE_HOME={0}
export PATH=$ORACLE_HOME/bin:$PATH
sqlplus -S /nolog <<EOF
connect / as sysdba
SET HEADING OFF
SELECT version FROM V\$INSTANCE;
exit;
EOF
""".format(OracleHome,SID)

                if "ERROR" not in execScript(command) or "ORA-" not in execScript(command):
                    #print execScript(command).strip().split('.')[0]
                    if  int(execScript(command).strip().split('.')[0]) >= 11:
                        successTNS.append(SID)
                        statusList.append(0)
                    else:
					    statusList.append(1)
                else:
                    statusList.append(1)				
	
                
            if 1 not in statusList:
                print "0"
                print "ExitDesc: Upgraded DB Version Validation successful!"
                print ",".join(successTNS)
                log.info('Exitcode: 0')
                log.info('ExitDesc: Upgraded DB Version Validation successful!')
                ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Upgraded DB Version Validation successful!",LogServer,LogDB,LogUser,LogPassword)
                HLStatus.UpdateHLStatus(APID,"Stepid102","Completed","Oracle Post Check- Validation of DB Version Script completed",LogServer,LogDB,LogUser,LogPassword)				
            elif 0 in statusList and 1 in statusList:
                print "0"
                print "ExitDesc: Some of the DB Version Validation Failed!"
                print ",".join(successTNS)
                log.info('Exitcode: 0')
                log.info('ExitDesc: Some of the DB Version Validation Failed!')
                ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Some of the DB Version Validation Failed!",LogServer,LogDB,LogUser,LogPassword)
                HLStatus.UpdateHLStatus(APID,"Stepid102","Completed","Oracle Post Check- Validation of DB Version Script completed",LogServer,LogDB,LogUser,LogPassword)				
            elif 0 not in statusList:
                print "1"
                print "ExitDesc: Upgraded DB Version Validation failed!"
                log.info('Exitcode: 1')
                log.info('ExitDesc: Upgraded DB Version Validation failed!')
                ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Upgraded DB Version Validation failed!",LogServer,LogDB,LogUser,LogPassword)
                HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Validation of DB Version Script failed",LogServer,LogDB,LogUser,LogPassword)
        else:
            print "10"
            print "ExitDesc: Oracle Home is not matching with DB Name."
            log.info("ExitCode: 10")
            log.info("ExitDesc: Oracle Home is not matching with DB Name.")
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Oracle Home is not matching with DB Name.",LogServer,LogDB,LogUser,LogPassword)
            HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Validation of DB Version Script failed",LogServer,LogDB,LogUser,LogPassword)
    except socket.error:
        print "10"
        print "ExitDesc: Script failed due to Invalid server ip address %s" %address
        log.error("ExitCode: 10")
        log.error("ExitDesc: Invalid server ip address")
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Invalid server ip address",LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Validation of DB Version Script failed",LogServer,LogDB,LogUser,LogPassword)
    except Exception, e:
        print "10"
        print "ExitDesc: Exception Failure. Check the log for errors"
        print str(e)
        log.error("ExitCode: 10")
        log.error("ExitDesc: {0}".format(e))
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Exception Failure. Check the log for errors",LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Validation of DB Version Script failed",LogServer,LogDB,LogUser,LogPassword)
    finally:
        s.close()
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info("ExitCode: 10")
    log.info("ExitDesc: Missing Arguments")
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Missing Arguments",LogServer,LogDB,LogUser,LogPassword)
    HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Validation of DB Version Script failed",LogServer,LogDB,LogUser,LogPassword)