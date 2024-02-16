"""
	Name: preupgrade_fixups.py
	Description: Executed from HP OO, to preupgrade_fixups.sql
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
    filename = "preupgrade_fixups.log"
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
ActivityName = "Run Pre-Upgrade Fixup SQL File"
Des = "Run Pre-Upgrade Fixup SQL File"
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
        TNSName=sys.argv[10]
        if "," in TNSName:
            TNSName=TNSName.split(",")
        orahome=sys.argv[11]
        CIServer = Hostname
        address = Hostname
        tns_names=""
        count=0
        port = 22 
        #Connectivity Test #
        ActivityLogger.InsertActivityLog(APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
        HLStatus.UpdateHLStatus(APID,"Stepid99","In Progress","Oracle Upgradation Pre Check is in Progress which is executing Preupgrade Fixup script",LogServer,LogDB,LogUser,LogPwd)		
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)


        def chkfile(orahome,TNSName):
            orabase='/'.join(orahome.split("/")[:4])
            command="[ -f {0}/cfgtoollogs/{1}/preupgrade/preupgrade_fixups.sql ] && echo True".format(orabase,TNSName)
            log.info('Executing the command : {0}'.format(command))
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            log.info('Output  : {0}'.format(output))
            return output 

        def run_preupgrade(orahome,TNSName):
            count = 0
            orabase='/'.join(orahome.split("/")[:4])
            command="export ORACLE_HOME={0}\nexport ORACLE_SID={1}\nexport PATH=$PATH:$ORACLE_HOME/bin\nsqlplus /nolog <<EOF \n conn / as sysdba;\n@{2}/cfgtoollogs/{1}/preupgrade/preupgrade_fixups.sql; \nexit; \nEOF\n".format(orahome,TNSName,orabase)
            log.info('Executing the command : {0}'.format(command))
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            log.info('Output  : {0}'.format(output))
            output = output.split("\n")
            for i in range(len(output)):
                if "ORA-" in output[i]:
                    count = count+1
            log.info('No of Errors  : {0}'.format(count))
            if count == 0:
                return "True"
            else:
                return "False"

        if isinstance(TNSName, list):
            for TNS in TNSName:
                check=chkfile(orahome,TNS)
                if "True" in check:
                    out = run_preupgrade(orahome,TNS)
                    if out == "True":
                        tns_names=tns_names+TNS+","
                    else:
                        count=count+1
                else:
                    log.info("{0}/cfgtoollogs/{1}/preupgrade/preupgrade_fixups.sql doesnot exists. Trying with UPPERCASE TNSName. Reason: Folder may be created with UPPERCASE, Since Linux is Case sensitive".format(orahome,TNS))
                    TNS = TNS.upper()
                    check=chkfile(orahome,TNS)
                    if "True" in check:
                        out = run_preupgrade(orahome,TNS)
                        if out == "True":
                            tns_names=tns_names+TNS+","
                        else:
                            count=count+1
                    else:
                        log.info("{0}/cfgtoollogs/{1}/preupgrade/preupgrade_fixups.sql doesnot exists. So skipping Preupgrade fixups execution".format(orahome,TNS))
            if tns_names:
                tns_names=tns_names.rstrip(",")
                log.info('Succesfull Preupgrade fixups are {0}'.format(tns_names))
                if count == 0:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Preupgrade fixups execution Succesfull",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc:Preupgrade fixups execution Succesfull')
                    print "0"
                    print "ExitDesc: Preupgrade fixups execution Succesfull"
                    HLStatus.UpdateHLStatus(APID,"Stepid99","Completed","Oracle Upgradation- PreCheck Completed Successfully",LogServer,LogDB,LogUser,LogPwd)
                else:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Some Preupgrade fixups Failed",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc:Some Preupgrade fixups Failed')
                    print "0"
                    print "ExitDesc: Some Preupgrade fixups Failed"
                    HLStatus.UpdateHLStatus(APID,"Stepid99","Completed","Oracle Upgradation- PreCheck Completed Successfully",LogServer,LogDB,LogUser,LogPwd)
                print tns_names

            else:
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Preupgrade fixups execution Failed",LogServer,LogDB,LogUser,LogPwd)
                log.info('10')
                log.info('ExitDesc:Preupgrade fixups execution Failed')
                HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- PreUpgradeFixup Script failed",LogServer,LogDB,LogUser,LogPwd)
                print "10"
                print "ExitDesc: Preupgrade fixups execution Failed"

        else:
            check=chkfile(orahome,TNSName)

            if "True" in check:
                out = run_preupgrade(orahome,TNSName)
                if out == "True":
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Preupgrade fixups execution Succesfull",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc:Preupgrade fixups execution Succesfull')
                    print "0"
                    print "ExitDesc: Preupgrade fixups execution Succesfull"
                    HLStatus.UpdateHLStatus(APID,"Stepid99","Completed","Oracle Upgradation- PreCheck Completed Successfully",LogServer,LogDB,LogUser,LogPwd)
                else:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Preupgrade fixups execution Failed",LogServer,LogDB,LogUser,LogPwd)
                    log.info('10')
                    log.info('ExitDesc:Preupgrade fixups execution Failed')
                    print "10"
                    print "ExitDesc: Preupgrade fixups execution Failed"
                    HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- PreUpgradeFixup Script failed",LogServer,LogDB,LogUser,LogPwd)
            else:
                TNSName = TNSName.upper()
                check=chkfile(orahome,TNSName)

                if "True" in check:
                    out = run_preupgrade(orahome,TNSName)
                    if out == "True":
                        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Preupgrade fixups execution Succesfull",LogServer,LogDB,LogUser,LogPwd)
                        log.info('0')
                        log.info('ExitDesc:Preupgrade fixups execution Succesfull')
                        print "0"
                        print "ExitDesc: Preupgrade fixups execution Succesfull"
                        HLStatus.UpdateHLStatus(APID,"Stepid99","Completed","Oracle Upgradation- PreCheck Completed Successfully",LogServer,LogDB,LogUser,LogPwd)
                    else:
                        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Preupgrade fixups execution Failed",LogServer,LogDB,LogUser,LogPwd)
                        log.info('10')
                        log.info('ExitDesc:Preupgrade fixups execution Failed')
                        print "10"
                        print "ExitDesc: Preupgrade fixups execution Failed"
                        HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- PreUpgradeFixup Script failed",LogServer,LogDB,LogUser,LogPwd)
                else:
                    log.info("{0}/cfgtoollogs/{1}/preupgrade/preupgrade_fixups.sql doesnot exists. So skipping Preupgrade fixups execution".format(orahome,TNSName))
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Preupgrade fixups execution Failed",LogServer,LogDB,LogUser,LogPwd)
                    log.info('10')
                    log.info('ExitDesc:Preupgrade fixups execution Failed')
                    HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- PreUpgradeFixup Script failed",LogServer,LogDB,LogUser,LogPwd)
                    print "10"
                    print "ExitDesc: Preupgrade fixups execution Failed. Please provide a valid orahome and TNSName."


    except Exception, e:
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error, see logs for more details",LogServer,LogDB,LogUser,LogPwd)
        log.info('Error: {0}'.format(e))
        print "1"
        print "ExitDesc: Error, see logs for more details"
        HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- PreUpgradeFixup Script failed",LogServer,LogDB,LogUser,LogPwd)
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('10')
    log.info('ExitDesc: Missing Arguments')