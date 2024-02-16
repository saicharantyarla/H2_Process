"""
    Name: Oracle_Validate_user_write_permission.py
    Description: Executed from HP OO, to validate write permission of a user on a folder
    Team: Software Service Automation
    Author: Vikrant Kumar (vikrant.a.kumar@capgemini.com)
    Inputs: Arguments [HostName, UserName, Password, Directory], LogFileLoc
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
    filename = "Validate_write_permission.log"
    filepath = "C:\Python_Logs\ORACLE_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "10"
    print "ExitDesc: Unable to create Logfile {0}".format(filename)

# Variable Mapping #
ActivityName = "Validate  Write permission"
Des = "validate write permission of a user on a folder"
s = socket.socket()

log.info('Input Variables mapping...')
if len(sys.argv) == 5:
    ##Script Variables##
    HostName = sys.argv[1]  #Target HostName    
    UserName = sys.argv[2]  #Target Host user name to connect 
    Password = sys.argv[3]  #Target Host user password to connect
    Directory = sys.argv[4] #Size of tablespace

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
        command1 = """if [ -d """+Directory+""" ]; then
                        echo "Yes"
                    else
                        echo "No"
                    fi"""
        stdin, stdout, stderr = dssh.exec_command(command1)
        output1 = stdout.read()
        errout = stderr.read()
        #print command1
        output1=output1.strip()
        #print output1
        if output1 == "No":
        
            #print output1
            #print "Directory doesnot exists creating the Directory"
            command2 = " mkdir -p %s " %Directory
            #print command2
            stdin, stdout, stderr = dssh.exec_command(command2)
            output2 = stdout.read()
            #print output2
            
            command1 = """if [ -d """+Directory+""" ]; then
            echo "Yes"
            else
            echo "No"
            fi"""
            stdin, stdout, stderr = dssh.exec_command(command1)
            output2 = stdout.read()
            errout = stderr.read()
            output2 = output2.strip()
            if output2 == "Yes":
                command = "ls -ld {0} | cut -d' ' -f1".format(Directory)
                log.info('Executing the command :{0}'.format(command))
                stdin, stdout, stderr = dssh.exec_command(command)
                output = stdout.read()
                error = stderr.read()
 
                if error.strip() == "":
                    if output[2] == "w":
                        print "0"
                        print "ExitDesc: The user has write permission."
                        log.info('Exitcode: 0')
                        log.info('ExitDesc: The user has write permission.')
                    else:
                        print "1"
                        print "ExitDesc: The user does not have write permission."
                        log.info('Exitcode: 1')
                        log.info('ExitDesc: The user does not have write permission.')
                else:
                    print "10"
                    print "ExitDesc: %s" %(error)
                    log.info('Exitcode: 10')
                    log.info('Error: {0}'.format(error))
                        
            else:
                print "10"
                print "ExitDesc: %s" %(errout)
                log.info('Exitcode: 10')
                log.info('Error: {0}'.format(errout))
                
        else:
                    
            command = "ls -ld {0} | cut -d' ' -f1".format(Directory)
            log.info('Executing the command :{0}'.format(command))
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            error = stderr.read()
 
            if error.strip() == "":
                if output[2] == "w":
                    print "0"
                    print "ExitDesc: The user has write permission."
                    log.info('Exitcode: 0')
                    log.info('ExitDesc: The user has write permission.')
                else:
                    print "1"
                    print "ExitDesc: The user does not have write permission."
                    log.info('Exitcode: 1')
                    log.info('ExitDesc: The user does not have write permission.')
            else:
                print "10"
                print "ExitDesc: %s" %(error)
                log.info('Exitcode: 10')
                log.info('Error: {0}'.format(error))                   
            
                   
    except socket.error:
        print "10"
        print "ExitDesc: script failed due to Invalid server ip address %s" %address
        log.info('Exitcode: 1')
        log.info('ExitDesc: Invalid server ip addres')
    except Exception, e:
        print "10"
        print "ExitDesc: {0}".format(e)             
        log.info('Error: {0}'.format(e))
    finally:
        s.close()
        dssh.close()        
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('Exitcode: 10')
    log.info('ExitDesc: Missing Arguments')
