"""
	Name: Space_Availability_Check_specificDrive.py
	Description: Executed from HP OO, to check for space availablity
	Team: Software Service Automation
	Author: Sravani
	Inputs: Arguments [Hostname,Username,Password,Size,MaxSize,TNSName,datafiles], LogFileLoc
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

import cx_Oracle as dbc


try:
    filename = "Space_Availability_Check_SpecDrive.txt"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "10"
    print "ExitDesc: Unable to create Logfile {0}".filename


# Variable Mapping #
ActivityName = "Space_Availability_Check_SpecDrive"
Des = "Check for space availability in Specific drive"
s = socket.socket()
a=0

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 4:

        ##Script Variables##
        Hostname = sys.argv[1]  #Target HostName  	
        osuser = sys.argv[2]	#Target Host user name to connect 
        ospassword = sys.argv[3]	#Target Host user password to connect
        ReqSize = "8G"	#Size of tablespace
        DFPath = '/u01'	#MaxSize of tablespace


        address = Hostname
        port = 22
        input_drives = []
        other_drives = []
        count = None
        tbspath  = None
        if "g" in ReqSize:
            ReqSize = int(ReqSize.split("g")[0])*1024

        elif "m" in ReqSize:
            ReqSize = int(ReqSize.split("m")[0])

        elif "G" in ReqSize:
            ReqSize = int(ReqSize.split("G")[0])*1024

        elif "M" in ReqSize:
            ReqSize = int(ReqSize.split("M")[0])

        else:
            ReqSize = int(ReqSize)


        #Connectivity Test #

        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        log.info('{0} host is reachable'.format(Hostname))
        command1="test -d %s \necho $?" %(DFPath)
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)
        log.info('Command Execution Starts')
        stdin, stdout, stderr = dssh.exec_command(command1)
        output = stdout.read()
	#print output
        output = str(output).translate(None, "[( ',\n	\r)]")
        if output == "0":
            log.info('Given path for Binary is Available')
            command="df -h -m %s | awk '{print $4}'"%(DFPath)
            log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
             
            log.info('Succesfully connected  to the host {0} '.format(Hostname))

            log.info('Executing the command :{0}'.format(command))

            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            output=output[:-1]
            output = output.split("\n")
            output = int(output[1])
            output=output * (0.80)
            output= int(output)
            if output > ReqSize:
                print "0"
                print "ExitDesc: Space is available in the default Drive"
                print "%s"%DFPath
                log.info('Exitcode: 0')
                log.info("ExitDesc: Space is available in the default %s drive"%DFPath)
            else:
                print "10"
                print "ExitDesc: Space is not available in default drive"
                log.info('Exitcode: 10')
                log.info("ExitDesc: Space is not available in the default %s drive"%DFPath)

        else:
            log.info('Exitcode: 10')
            log.info("Given path %s is not Available"%DFPath)
            print "10"
            print "ExitDesc: Given path %s is not Available"%DFPath
        
    else:
        print "10"
        print "ExitDesc: Missing Arguments"
        log.info('Exitcode: 10')
        log.info('ExitDesc: Missing Arguments')
        
except socket.error:
    log.info('Exitcode: 1')
    log.info('ExitDesc: Invalid server ip addres')
    print "1"
    print "ExitDesc: script failed due to Invalid server ip address %s" %address
except Exception, e:
    log.info('Error: {0}'.format(e))
    s.close()
    print "1"
    print "ExitDesc: {0}".format(e)
			
finally:
	s.close()
