"""
	Name: Group_Name_Validation.py
	Description: Executed from HP OO, to Group_Name_Validation
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
    filename = "Group_Name_Validation.log"
    filepath = "C:\Python_Logs\\ORACLE_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".format(filename)

# Variable Mapping #
ActivityName = "Group Name Validation Task"
Des = "Group Name Validation Task"
s = socket.socket()

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 5:
        #APID = sys.argv[1]
        Hostname = sys.argv[1]  #Target HostName  	
        osuser = sys.argv[2]	#Target Host user name to connect 
        ospassword = sys.argv[3]	#Target Host user password to connect
        group_name = sys.argv[4]
        address = Hostname
        port = 22 
        groups=[]
        User_check=[]
        #Connectivity Test #

        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        log.info('{0} host is reachable'.format(Hostname))

        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
		
        ## Connection to the remote host ##

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)
        if "," in group_name:
            group_name = group_name.split(",")
            for group in group_name:
                command="getent group {0}".format(group)
                log.info('Executing the command :{0}'.format(command))
                stdin, stdout, stderr = dssh.exec_command(command)
                out = stdout.read()
                #print out
                log.info('Group : {0} & Output : {1}'.format(group,out))
                if out:
                    command="""if id -nG """+osuser+""" | grep -qw """+group+"""; then
    echo True
else
    echo False
fi
"""
                    stdin, stdout, stderr = dssh.exec_command(command)
                    out = stdout.read()
                    if "True" in out:
                        User_check.append(group)
                    else:
                        User_check.append(" ")
                        
                    groups.append(group)
                else:
                    groups.append(" ")
            if group_name == groups:
                if " " not in User_check:
                    log.info('ExitCode: 0')
                    log.info('ExitDesc: Group exists in the server.')
                    print "0"
                    print "ExitDesc: Groups exists in the server and It is mapped with provided User."
                    print ",".join(groups)
                else:
                    log.info('ExitCode: 10')
                    log.info('ExitDesc: Group name is not mapped with provided User.')
                    print "10"
                    print "ExitDesc: Blank field's Group name is not mapped with provided User."
                    print ",".join(User_check)

            else:
                if groups:

                    log.info('ExitCode: 10')
                    log.info('ExitDesc: Groups {0} exists in the server.'.format(groups))
                    print "10"
                    print "ExitDesc: Blank field's Group dos't exists in the server."
                    
                    print ",".join(groups)

                else:

                    log.info('ExitCode: 10')
                    log.info('ExitDesc: Groups doesnot exists in the server.')
                    print "10"
                    print "ExitDesc: Groups doesnot exists in the server."

        else:
            command="getent group {0}".format(group_name)

            log.info('Executing the command :{0}'.format(command))

            stdin, stdout, stderr = dssh.exec_command(command)
            out = stdout.read()
            log.info('Output : {0}'.format(out))

            if out:

                log.info('ExitCode: 0')
                log.info('ExitDesc: Group exists in the server.')
                print "0"
                print "ExitDesc: Group exists in the server."
                print ",".join(group_name)

            else:

                log.info('ExitCode: 10')
                log.info('ExitDesc: Group doesnot exists in the server.')
                print "10"
                print "ExitDesc: Group doesnot exists in the server."
                print ",".join(group_name)

			
    else:

        print "10"
        print "ExitDesc: Missing Arguments"
        log.info('ExitCode: 10')
        log.info('ExitDesc: Missing Arguments')


except Exception, e:

    log.info('Error: {0}'.format(e))
    print "1"
    print "ExitDesc: {0}".format(e)
