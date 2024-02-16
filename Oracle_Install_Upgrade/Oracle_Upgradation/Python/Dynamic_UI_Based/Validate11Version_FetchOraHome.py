# -*- coding: utf-8 -*-
"""
	Name: Get Oracle Home from Oratab
	Description: Executed from HP OO, to Get Oracle Home from Oratab
	Team: Software Service Automation
	Author: Vikrant Kumar (vikrant.a.kumar@capgemini.com)
	Inputs: Arguments [HostName,UserName,Password]
	Output: ExitCode, ExitDesc(Log File)"""

# Modules Initializing #
import datetime
import sys
import socket
import paramiko
import logging as log
from os import system,getcwd,path,makedirs

try:
    filename = "Oracle_Get_Oracle_Home_from_Oratab_11.log"
    filepath = "C:\Python_Logs\Oracle_Upgradation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".format(filename)
    print str(e)

# Variable Mapping #
ActivityName = "Get Oracle Home from Oratab"
Des = "Get Oracle Home from Oratab"
s = socket.socket()

log.info('Input Variables mapping...')
# Arguments Mapping #
if len(sys.argv) == 4:
    ##Script Variables##
    HostName = sys.argv[1] #HostName  	
    UserName = sys.argv[2] #UserName
    Password = sys.argv[3] #Password

    address = HostName
    port = 22 			

    #Connectivity Test #
    log.info('Checking connectivity to the host : {0}'.format(HostName))
    try:
        s.connect((address, port)) 
        log.info('{0} host is reachable'.format(HostName))		

        ## Connection to the remote host ##
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(HostName,UserName))

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(HostName, username=UserName, password=Password)

        log.info('Succesfully connected  to the host {0} '.format(HostName))
        command = """. ~/.bash_profile
cat /etc/oratab | grep -v '#'
"""
        #print command

        log.info("Executing the command...\n{}".format(command))        
        stdin, stdout, stderr = dssh.exec_command(command)
        output = stdout.read()
        error = stderr.read()
        countList = []
        outputList = []
        #print output
        for output in output.strip().split('\n'):
            #print output
            if '11.2.0.4' in output.strip():
                countList.append(0)
                outputList.append(output.strip().split(':')[1])
            else:
                countList.append(1)

        if 0 in countList:
            print "0"
            print "ExitDesc: Oracle_Home is available in Oratab!"
            print ','.join(outputList)
            log.info('Exitcode: 0')
            log.info('ExitDesc: Oracle_Home is available in Oratab!')
        else:
            print "1"
            print "ExitDesc: Oracle_Home is not available in Oratab!"
            log.info('Exitcode: 1')
            log.info('ExitDesc: Oracle_Home is not available in Oratab!')

    except socket.error, e:
        print "10"
        print "ExitDesc: Exception Failure.Check the log for errors."
        log.info('Exitcode: 10')
        log.info('ExitDesc: {0}'.format(e))

    except Exception, e:
        print "10"
        print "ExitDesc: Exception Failure.Check the log for errors."
        log.info('Exitcode: 10')
        log.info('ExitDesc: {0}'.format(e))
		
    finally:
        s.close()
        dssh.close()
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info("Exitcode: 10")
    log.info("ExitDesc: Missing Arguments")