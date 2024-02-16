"""
	Name: config_selinux.py
	Description: Executed from HP OO, to config_selinux
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
    filename = "config_selinux.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".format(filename)

# Variable Mapping #
ActivityName = "Configure SElinux"
Des = "Configure Selinux parameter validation"
s = socket.socket()

if len(sys.argv) == 10:
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
        CIServer = Hostname
        address = Hostname
        port = 22 
        #Connectivity Test #
        HLStatus.UpdateHLStatus(APID,"Stepid96","In Progress","Oracle Selinux file Configuration is in Progress",LogServer,LogDB,LogUser,LogPwd)
        ActivityLogger.InsertActivityLog(APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)

        cmd="getenforce"
        log.info('Executing the command : {0}'.format(cmd))
        stdin, stdout, stderr = dssh.exec_command(cmd)
        out = stdout.read()
        log.info('Output of getenforce : {0}'.format(out))
        if out != "Permissive":
            command="setenforce 0"
            log.info('Executing the command : {0}'.format(command))
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            log.info('Output of setenforce 0 : {0}'.format(output))
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","SELinux Configuration Succesfull",LogServer,LogDB,LogUser,LogPwd)
            log.info('0')
            log.info('ExitDesc: SELinux Configuration Succesfull')
            print "0"
            print "ExitDesc: SELinux Configuration Succesfull"



        else:
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","SELinux Configuration is already Permissive",LogServer,LogDB,LogUser,LogPwd)
            log.info('0')
            log.info('ExitDesc: SELinux Configuration is already Permissive')
            print "0"
            print "ExitDesc: SELinux Configuration is already Permissive"




    except Exception, e:
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error",str(e),LogServer,LogDB,LogUser,LogPwd)
        log.info('Error: {0}'.format(e))
        print "1"
        print "ExitDesc: {0}".format(e)
        HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Selinux Configuration Script failed becouse of some exception",LogServer,LogDB,LogUser,LogPwd)

else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('10')
    log.info('ExitDesc: Missing Arguments')
