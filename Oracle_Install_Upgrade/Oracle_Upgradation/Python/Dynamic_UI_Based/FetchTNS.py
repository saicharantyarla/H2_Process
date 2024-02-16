"""
	Name: Fetch_TNSNames.py
	Description: Executed from HP OO, to fetch TNS Names for a server
	Team: Software Service Automation
	Author: Sravani
	Inputs: Arguments [Hostname,Username,Password], LogFileLoc
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

try:
    filename = "FetchTNS.txt"
    filepath = 'C:\Python_Logs\Oracle_Upgradation'
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
ActivityName = "Fetch_TNSNames"
Des = "Fetches  the list of TNS names"
s = socket.socket()
a=0

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 5:
        ##Script Variables##
        Hostname = sys.argv[1]  #Target HostName  	
        osuser = sys.argv[2]	#Target Host user name to connect 
        ospassword = sys.argv[3]	#Target Host user password to connect
        OraHome = sys.argv[4]	#Target Host user password to connect		
        CIServer=Hostname
        address = Hostname
        port = 22
        count = None
        tbspath  = None
        CorLis=[]
        InCorLis=[]		
        #Connectivity Test #

        log.info('Checking connectivity to the host : {0}'.format(Hostname))
        s.connect((address, port)) 
		
        log.info('{0} host is reachable'.format(Hostname))
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
        ## Connection to the remote host ##
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)
        log.info('Succesfully connected  to the host {0} '.format(Hostname))
        command=". .bash_profile; ps -ef | grep -v \"grep tnslsnr\"| grep tnslsnr | awk  '{print $8,$9}'| grep ^$OraHome | awk '{print $2}'"
        log.info('Executing the command :{0}'.format(command))
        stdin, stdout, stderr = dssh.exec_command(command)
        output = stdout.read()
        output=output.strip()
        err= stderr.read()
        if err:
            print "1"
            print "ExitDesc: Unable to execute the command.Check the log for errors."
            log.info('Exitcode: 1')
            log.info('Error: {0}'.format(err))
        else:
            if output:
                print "0"
                print "ExitDesc: Tns Names Fetched"
                fiop=output.split("\n")
                fiop=filter(None,fiop)
                opst=",".join(fiop)
                print opst
                log.info('ExitCode:0')
                log.info('Info: Successfully stopped the listeners.')
            else:
                print "10"
                print "Exitdesc: No Tns Names are present"
                log.info('ExitCode:10')
                log.info('Info: No TNS Names Present.')
    else:
        print "1"
        print "ExitDesc: Missing Arguments"
        log.info('Exitcode: 1')
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