"""
	Name: binary File Search
	Description: Executed from HP OO, Checks for the file binary files in given server
	Team: Software Service Automation
	Inputs: Arguments Source and Targets Hostname
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
    filename = "Binary_Search.log"
    filepath = "C:\Python_Logs\\ORACLE_Installation"
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
    if len(sys.argv) == 4:
        
        Hostname = sys.argv[1]  #Target HostName  	
        osuser = sys.argv[2]	#Target Host user name to connect 
        ospassword = sys.argv[3]	#Target Host user password to connect
        #Directory_Name = sys.argv[4]	Directory_Name
        #Directory_Name=Directory.split("/")
        #Directory_Name="/"+Directory[1]
        
        CIServer = Hostname
        address = Hostname
        port = 22
        command="locate -i '*_12102_database_*.zip'"
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)
        log.info('Command Execution Starts')
        stdin, stdout, stderr = dssh.exec_command(command)
        output = stdout.read()
        pathA=[]
        pathB=[]
        if output:
            
            output=output.split("\n")
            
            for i in output:
                
                i=i.split("/")
                i= i[:-1:]
                j="/".join(i)
                pathA.append(j)
            for i in pathA:
                if i not in pathB:
                    if i !="":
                        pathB.append(i)
            log.info('Given path for Binary is  Available')
            print "0"
            print "ExitDesc: Binaries are availbale in given path"
            print ",".join(pathB)
        
            
        else:

            log.info('Given path for Binary is not Available')
            print "10"
            print "ExitDesc: No Oracle 12c Binaries available in this server"
		
    else:
        print "10"
        print "ExitDesc: Missing Arguments"

except Exception, e:
    print "1"
    print "ExitDesc: {0}".format(e)
