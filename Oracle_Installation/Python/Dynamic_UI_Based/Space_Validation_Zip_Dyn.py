"""
	Name: Space_Validation_Zip_Dyn.py
	Description: Executed from HP OO, to Space_Validation_Zip_Dyn
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
import socket


try:
    filename = "Space_Validation_Zip_Dyn.log"
    filepath = "C:\Python_Logs\ORACLE_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".format(filename)

# Variable Mapping #
ActivityName = "Space Validation before unzip"
Des = "Space Validation before unzip"
s = socket.socket()

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 5:
        log.info('Input Variables mapping...')

        #APID = sys.argv[1]
        ##Script Variables##
        Hostname = sys.argv[1]  #Target HostName  	
        osuser = sys.argv[2]	#Target Host user name to connect 
        ospassword = sys.argv[3]	#Target Host user password to connect
        zip_loc = sys.argv[4]
        CIServer = Hostname
        address = Hostname
        port = 22 

        #Connectivity Test #

        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)
        command="cd {0}\ndu -c *.zip | tail -1 | cut -f 1".format(zip_loc)
        log.info('Executing the command :{0}'.format(command))
        stdin, stdout, stderr = dssh.exec_command(command)
        zip_size = stdout.read()
        log.info('Output : in bytes : {0}, in MB = {1}'.format(zip_size,int(zip_size)/1024))
        zip_size = int(zip_size)
        if zip_size > 0:
            zip_size = int(zip_size)+int(zip_size)*0.2
            zip_size = int(zip_size)
            drive = zip_loc.split("/")[1]
            #cmd="df -k /u01 | sed -n 2p | awk '\{print $4\}'".format(drive)
            awkcmd = "{"+"print $4"+"}"
            cmd="df -k /{0} | sed -n 2p | awk '{1}'".format(drive,awkcmd)
            log.info('Executing the command :{0}'.format(cmd))
            stdin, stdout, stderr = dssh.exec_command(cmd)
            drive_size = stdout.read()
            log.info('Output : in bytes : {0}, in MB = {1}'.format(drive_size,int(drive_size)/1024))
            drive_size = int(drive_size)
            log.info('Comparing Location Size : {0} with Zipped Binary Size : {1} '.format(drive_size,zip_size))
            if drive_size > zip_size:
                log.info('0')
                log.info('ExitDesc: Binaries can be zipped')
                print "0"
                print "ExitDesc: Binaries can be zipped"

            else:
                log.info('10')
                log.info('ExitDesc: Binaries cannot be zipped, space is not available')
                print "10"
                print "ExitDesc: Binaries cannot be zipped, space is not available"


        else:
            log.info('10')
            log.info('ExitDesc: No Zipfiles found in the location')
            print "10"
            print "ExitDesc: No Zipfiles found in the location"

			
    else:
        print "10"
        print "ExitDesc: Missing Arguments"
        log.info(' 10')
        log.info('ExitDesc: Missing Arguments')


except Exception, e:
    log.info('Error: {0}'.format(e))
    print "1"
    print "ExitDesc: Space Validation for zipped files failed"
