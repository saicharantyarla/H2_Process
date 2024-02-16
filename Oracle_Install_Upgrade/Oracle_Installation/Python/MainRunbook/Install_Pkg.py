"""
	Name: Install_Pkg.py
	Description: Executed from HP OO, to Install_Pkg
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
    filename = "Install_Pkg.log"
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
ActivityName = "Install the Packages"
Des = "Install the Packages"
s = socket.socket()

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 11:
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
        pkg_list = sys.argv[10]
        CIServer = Hostname
        address = Hostname
        port = 22 
        #Connectivity Test #
        HLStatus.UpdateHLStatus(APID,"Stepid96","In Progress","Installed Packages Script run is In Progress",LogServer,LogDB,LogUser,LogPwd)
        ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			
        log.info('{0} host is reachable'.format(Hostname))

        count = 0


        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)

        def chk_pkg(cmd):
            log.info('Executing the command :{0}'.format(cmd))
            stdin, stdout, stderr = dssh.exec_command(cmd)
            out = stdout.read()
            log.info('Output of the command :{0}'.format(out))
            if "Error" in out:
                return "false"
            else:
                return "true"

        def inst_pkg(cmd):

            log.info('Executing the command :{0}'.format(cmd))
            stdin, stdout, stderr = dssh.exec_command(cmd)
            out = stdout.read()
            log.info('Output of the command :{0}'.format(out))
            if "Complete!" in out:
                return "true"
            else:
                return "false"

        if "," in pkg_list:
            chk_list = pkg_list.split(",")
            for pkg in chk_list:
                chk_cmd="yum list {0}".format(pkg)
                check = chk_pkg(chk_cmd)
                if check == "false":
                    count = count+1
            log.info('Count : {0} '.format(count))
            if count < 1:
                pkg_list = pkg_list.replace(","," ")
                cmd="yum install {0} -y".format(pkg_list)
                install = inst_pkg(cmd)
                if install == "true":
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Packages Installation Succesfull",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc: Packages Installation Succesfull.')
                    print "0"
                    print "ExitDesc: Packages Installation Succesfull."

                else:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Packages Installation Failed",LogServer,LogDB,LogUser,LogPwd)
                    log.info('1')
                    log.info('ExitDesc: Packages Installation Failed.')
                    print "1"
                    print "ExitDesc: Packages Installation Failed.%s"%pkg_list
                    HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Package Installation Script run Failed",LogServer,LogDB,LogUser,LogPwd)

            else:
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Package Not Available in Yum Repo",LogServer,LogDB,LogUser,LogPwd)
                log.info('1')
                log.info('ExitDesc: Package Not Available in Yum Repo')
                print "1"
                print "ExitDesc: Package Not Available in Yum Repo."
                HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Given Package for intallation is not available in Yum Repo",LogServer,LogDB,LogUser,LogPwd)




        else:
            chk_cmd="yum list {0}".format(pkg_list)
            check = chk_pkg(chk_cmd)
            if check == "true":
                cmd="yum install {0} -y".format(pkg_list)
                install = inst_pkg(cmd)
                if install == "true":
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Packages Installation Succesfull",LogServer,LogDB,LogUser,LogPwd)
                    log.info('0')
                    log.info('ExitDesc: Packages Installation Succesfull.')
                    print "0"
                    print "ExitDesc: Packages Installation Succesfull."

                else:
                    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Packages Installation Failed",LogServer,LogDB,LogUser,LogPwd)
                    log.info('1')
                    log.info('ExitDesc: Packages Installation Failed.')
                    print "1"
                    print "ExitDesc: Packages Installation Failed."
                    HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Given Package for intallation is Failed",LogServer,LogDB,LogUser,LogPwd)
                
            else:
                ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Package Not Available in Yum Repo",LogServer,LogDB,LogUser,LogPwd)
                log.info('1')
                log.info('ExitDesc: Package Not Available in Yum Repo')
                print "1"
                print "ExitDesc: Package Not Available in Yum Repo."
                HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Given Package for intallation is not available in Yum Repo",LogServer,LogDB,LogUser,LogPwd)

			
    else:
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Missing Arguments",LogServer,LogDB,LogUser,LogPwd)
        print "10"
        print "ExitDesc: Missing Arguments"
        log.info('10')
        log.info('ExitDesc: Missing Arguments')
        HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Package installation Script Failed Missing Argument",LogServer,LogDB,LogUser,LogPwd)

except Exception, e:
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error",str(e),LogServer,LogDB,LogUser,LogPwd)
    log.info('Error: {0}'.format(e))
    print "1"
    print "ExitDesc: {0}".format(e)
    HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Package Installation Script failed due to any Exception",LogServer,LogDB,LogUser,LogPwd)
