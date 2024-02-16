"""
	Name: Parent_Folder_Validation.py
	Description: Executed from HP OO, to Parent_Folder_Validation
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
import socket
import paramiko
import os

import ActivityLogger
#import HLStatus

try:
    filename = "Binary_path_validation.log"
    filepath = "C:\Python_Logs\\Oracle_Upgrade_Install\\Oracle_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".filename


try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 5:
        
        Hostname = sys.argv[1]  #Target HostName  	
        osuser = sys.argv[2]	#Target Host user name to connect 
        ospassword = sys.argv[3]	#Target Host user password to connect
        Directory_Name = sys.argv[4]	#Directory_Name
        #Directory_Name=Directory.split("/")
        #Directory_Name="/"+Directory[1]
        
        CIServer = Hostname
        address = Hostname
        port = 22
        command="test -d %s \necho $?" %(Directory_Name)
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)
        log.info('Command Execution Starts')
        stdin, stdout, stderr = dssh.exec_command(command)
        output = stdout.read()
	#print output
        output = str(output).translate(None, "[( ',\n	\r)]")
        if output == "0":
            log.info('Given path for Binary is Available')
            print "0"
            print "ExitDesc: Given Binary Path is Available"

        else:

            log.info('Given path for Binary is not Available')
            print "10"
            print "ExitDesc: Given Binary path is not Available"
		
    else:
        print "10"
        print "ExitDesc: Missing Arguments"

except Exception, e:
    print "1"
    print "ExitDesc: {0}".format(e)
