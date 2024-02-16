"""
	Name: Install_Oracle.py
	Description: Executed from HP OO, to Install Oracle 12
	Team: Software Service Automation
	Author: Sravani
	Inputs: Arguments [Hostname,Username,Password,ResponseFileLocation], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
	
"""

#!/usr/bin/env python
from sys import path
import sys
import logging as log
import time
import datetime
from os import system,getcwd,path,makedirs
import socket
import paramiko
import os
import ActivityLogger
import HLStatus
try:
    filename = "InstallOracle.txt"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, filemode='w', format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "10"
    print "ExitDesc: Unable to create Logfile {0}".filename


# Variable Mapping #
ActivityName = "Install Oracle 12"
Des = "Performs Silent installation for Oracle 12"
s = socket.socket()
a=0

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 12:
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
        ResponseFileLoc=sys.argv[10]
        BinaryPath=sys.argv[11]
        CIServer=Hostname
        address = Hostname
        port = 22
	
        #Connectivity Test #

        log.info('Checking connectivity to the host : {0}'.format(Hostname))
        ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        s.connect((address, port)) 
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)	
	HLStatus.UpdateHLStatus(APID,"Stepid97","In Progress","Oracle Installation is In Progress",LogServer,LogDB,LogUser,LogPwd)	
        log.info('{0} host is reachable'.format(Hostname))
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
        ## Connection to the remote host ##
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to take session to Server",LogServer,LogDB,LogUser,LogPwd)	
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)
        log.info('Succesfully connected  to the host {0} '.format(Hostname))
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Successfully conencted to server and execution of command initiated",LogServer,LogDB,LogUser,LogPwd)	
        InstallPath=BinaryPath+"/database"
        command="cd %s; ./runInstaller -silent -noconfig -responseFile %s"%(InstallPath,ResponseFileLoc)
        log.info('Executing the command :{0}'.format(command))
        stdin, stdout, stderr = dssh.exec_command(command)
        output = stdout.read()
        err= stderr.read()
        if err:
            print "1"
            print "ExitDesc: Unable to execute the command.Check the log for errors."
            log.info('Exitcode: 1')
            log.info('Error: {0}'.format(err))
            HLStatus.UpdateHLStatus(APID,"Stepid97","Failed","Oracle Installation Script failes, Unable to execute the command.Check the log for errors",LogServer,LogDB,LogUser,LogPwd)	
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Unable to execute the command.Check the log for errors.",LogServer,LogDB,LogUser,LogPwd)	
        else:
            if output:
                log.info('Log from execution is:{0}'.format(output))
                oplist=output.split("\n")
                oplist=filter(None, oplist)
                stringtoMatch="The installation of Oracle Database 12c was successful."
                if stringtoMatch in oplist:
                    LocFetchLog="You can find the log of this install session at:" 
                    RootFileLoc="As a root user, execute the following script(s):"
                    i=oplist.index(LocFetchLog)
                    i=i+1
                    logpath=oplist[i]
                    i=oplist.index(RootFileLoc)
                    rootpath=oplist[i+1]
                    rootpath=rootpath.split("1.",1)
                    log.info('ExitCode:0')
                    log.info('Info: Installation Succesful still Log has to be checked.')
                    log.info('Info: LogPath is {0} '.format(logpath)) 
                    log.info('Info: RootPath is {0} '.format(rootpath)) 
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Installation Successful still logs has to be verified.",LogServer,LogDB,LogUser,LogPwd)
                    print "0"
                    print "ExitDesc: Installation Succesful still Log has to be checked"
                    print logpath.strip()
                    print rootpath[1].strip()
                    HLStatus.UpdateHLStatus(APID,"Stepid97","Completed","Oracle Installation Succesful",LogServer,LogDB,LogUser,LogPwd)	
                else:
                    print "10"
                    print "ExitDesc: Installation was not Succesful.Check the Logs"
                    log.info('ExitCode:10')
                    log.info('Info: Installation was not Succesful.Check the Logs.')
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Installation was not Successful.Check the logs",LogServer,LogDB,LogUser,LogPwd)
                    HLStatus.UpdateHLStatus(APID,"Stepid97","Failed","Oracle Installation Script failes, Installation was not Succesful.Check the log for errors",LogServer,LogDB,LogUser,LogPwd)	
            else:
                print "10"
                print "Exitdesc: Installation not successfull"
                log.info('ExitCode:10')
                log.info('Error: Installation not successfull.')
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Installation not successfull.",LogServer,LogDB,LogUser,LogPwd)
                HLStatus.UpdateHLStatus(APID,"Stepid97","Failed","Oracle Installation Script failes, Installation was not Succesful.Check the log for errors",LogServer,LogDB,LogUser,LogPwd)	
    else:
        print "1"
        print "ExitDesc: Missing Arguments"
        log.info('Exitcode: 1')
        log.info('ExitDesc: Missing Arguments')
        HLStatus.UpdateHLStatus(APID,"Stepid97","Failed","Oracle Installation Script failes, Missing Argument",LogServer,LogDB,LogUser,LogPwd)	
except socket.error:
    log.info('Exitcode: 1')
    log.info('ExitDesc: Invalid server ip addres')
    print "1"
    print "ExitDesc: script failed due to Invalid server ip address %s" %address
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Invalid server ip address",LogServer,LogDB,LogUser,LogPwd)
    HLStatus.UpdateHLStatus(APID,"Stepid97","Failed","Oracle Installation Script failes,Invalid server ip address",LogServer,LogDB,LogUser,LogPwd)	
except Exception, e:
    log.info('Error: {0}'.format(e))
    s.close()
    print "1"
    print "ExitDesc: {0}".format(e)
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Exception faced with script.Check Logs",LogServer,LogDB,LogUser,LogPwd)
    HLStatus.UpdateHLStatus(APID,"Stepid97","Failed","Oracle Installation Script failes,Exception faced with script.Check Logs",LogServer,LogDB,LogUser,LogPwd)
finally:
	s.close()
