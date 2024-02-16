"""
	Name: update_oratab.py
	Description: Executed from HP OO, to update_oratab.sql
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
    filename = "update_oratab.log"
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
ActivityName = "This script updates /etc/oratab with new ORACLE_HOME"
Des = "This script updates /etc/oratab with new ORACLE_HOME"
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
			
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
        HLStatus.UpdateHLStatus(APID,"Stepid102","In Progress","Oracle Post Check is in Progress which is executing Update ORATAB script",LogServer,LogDB,LogUser,LogPwd)		
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)


        def gethome(TNSName):
            command="cat /etc/oratab | grep {0} | grep -v '#'| cut -d':' -f2".format(TNSName)
            log.info('Executing the command : {0}'.format(command))
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            log.info('Output  : {0}'.format(output))
            return output 

        def update_oratab(oldorahome,orahome,TNSName):
            count = 0
            command="sed -i '/^#/!s/{2}\:{0}/{2}\:{1}/g' /etc/oratab".format(oldorahome,orahome,TNSName)
            log.info('Executing the command : {0}'.format(command))
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            outerr = stderr.read()
            log.info('Output  : {0}'.format(output))
            if outerr:
                log.info('Errors : {0}'.format(outerr))
                return "False"
            else:
                return "True"

        if isinstance(TNSName, list):
            for TNS in TNSName:
                check=gethome(TNS)
                if "\n" in check:
                    check = check.replace("\n","")
                if check:
                    if check != orahome:
                        check = check.replace("\n","")
                        check = check.replace("/","\/")
                        orahome = orahome.replace("/","\/")
                        out = update_oratab(check,orahome,TNS)
                        if out == "True":
                            tns_names=tns_names+TNS+","
                        else:
                            count=count+1
                    else:
                        log.info("ORACLE_HOME for SID {0} is set to {1} in /etc/oratab already. So skipping this SID".format(TNS,check))

                else:
                    log.info("{0} doesnot exists in /etc/oratab. So skipping this SID".format(TNS))
            if tns_names:
                tns_names=tns_names.rstrip(",")
                log.info('Succesfully updated /etc/oratab for the TNSNames  {0}'.format(tns_names))
                if count == 0:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","oratab updation succesfull",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc:oratab updation succesfull')
                    print "0"
                    print "ExitDesc: oratab updation succesfull"
                else:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","oratab updation failed",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc:oratab updation succesfull for few SIDs')
                    print "0"
                    print "ExitDesc: oratab updation succesfull for few SIDs"
                print tns_names

            else:
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","oratab updation failed",LogServer,LogDB,LogUser,LogPwd)
                log.info('10')
                log.info('ExitDesc:oratab updation failed')
                print "10"
                print "ExitDesc: oratab updation failed"

        else:
            check=gethome(TNSName)

            if "\n" in check:
                check = check.replace("\n","")
            if check:

                if check != orahome:
                    check = check.replace("/","\/")
                    orahome = orahome.replace("/","\/")
                    out = update_oratab(check,orahome,TNSName)

                    if out == "True":
                        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","oratab updation succesfull",LogServer,LogDB,LogUser,LogPwd)
                        log.info('0')
                        log.info('ExitDesc:oratab updation succesfull')
                        print "0"
                        print "ExitDesc: oratab updation succesfull"
                    else:
                        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","oratab updation failed",LogServer,LogDB,LogUser,LogPwd)
                        log.info('10')
                        log.info('ExitDesc:oratab updation failed')
                        print "10"
                        print "ExitDesc: oratab updation failed"
                        HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Update Oratab Script failed",LogServer,LogDB,LogUser,LogPwd)
                else:
                    log.info("ORACLE_HOME for SID {0} is set to {1} in /etc/oratab already. So skipping this SID".format(TNSName,check))
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","oratab already updated",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc:oratab already updated')
                    print "0"
                    print "ExitDesc: oratab already updated"


            else:
                log.info("{0} doesnot exists in /etc/oratab. So skipping this SID".format(TNSName))
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","oratab updation failed",LogServer,LogDB,LogUser,LogPwd)
                log.info('10')
                log.info('ExitDesc: oratab updation failed')
                print "10"
                print "ExitDesc: oratab updation failed. Please provide a valid SID."
                HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Update Oratab Script failed",LogServer,LogDB,LogUser,LogPwd)

    except Exception, e:
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error, see logs for more details",LogServer,LogDB,LogUser,LogPwd)
        log.info('Error: {0}'.format(e))
        print "1"
        print "ExitDesc: Error, see logs for more details"
        HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Update Oratab Script failed",LogServer,LogDB,LogUser,LogPwd)
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('10')
    log.info('ExitDesc: Missing Arguments')
