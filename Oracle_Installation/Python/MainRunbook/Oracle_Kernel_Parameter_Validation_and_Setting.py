"""
	Name: Oracle_Kernel_Parameter_Validation.py
	Description: Executed from HP OO to Validate Kernel Parameter
	Team: Software Service Automation
	Author: Vikrant Kumar(vikrant.a.kumar@capgemini.com)
	Inputs: Arguments [HostName,Username,Password]
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
import HLStatus
try:
    filename = "Kernel_Parameter_Validation.log"
    filepath = "C:\Python_Logs\ORACLE_Installation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".filename


# Variable Mapping #
ActivityName = "Kernel_Parameter_Validation"
Des = "Validates the Kernel Parameter and set where required"
s = socket.socket()

log.info('Input Variables mapping...')
if len(sys.argv) == 10:
    #Log Variable Mapping
    LogServer = sys.argv[1]
    LogDB = sys.argv[2]
    APID = sys.argv[3]
    LogAccountName = sys.argv[4]
    LogUser = sys.argv[5]
    LogPassword = sys.argv[6]
    
    ##Script Variables##
    HostName = sys.argv[7] #HostName  	
    UserName = sys.argv[8] #UserName 
    Password = sys.argv[9] #Password
    
    CIServer = HostName
    address = HostName
    port = 22
    count = []

    #Connectivity Test #
    HLStatus.UpdateHLStatus(APID,"Stepid84","In Progress","Oracle Kernel Parameter set is In Progress",LogServer,LogDB,LogUser,LogPassword)
    ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPassword)
    log.info('Checking connectivity to the host : {0}'.format(HostName))
    try:
        s.connect((address, port))
        log.info('{0} host is reachable'.format(HostName))		
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPassword)			
        
        ## Connection to the remote host ##		
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(HostName,UserName))		
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying SSH Connection to the host",LogServer,LogDB,LogUser,LogPassword)

        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(HostName, username=UserName, password=Password)
        
        log.info('Succesfully connected  to the host {0} '.format(HostName))
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesful to the host",LogServer,LogDB,LogUser,LogPassword)

        log.info('Executing the command...')
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to execute commnd on remote host",LogServer,LogDB,LogUser,LogPassword)
		
        def execCommand(command):
           stdin, stdout, stderr = dssh.exec_command(command, get_pty = True) 
           output = stdout.read()
           errout = stderr.read()
           return output+"\n"+errout
		
        vcommand1 = "grep net.ipv4.ip_local_port_range /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3,4"
        vcommand2 = "grep net.core.rmem_default /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
        vcommand3 = "grep net.core.rmem_max /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
        vcommand4 = "grep net.core.wmem_default /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
        vcommand5 = "grep net.core.wmem_max /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
        vcommand6 = "grep kernel.shmmax /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
        vcommand7 = "grep kernel.shmmni /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
        vcommand8 = "grep kernel.sem /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3,4,5,6"
        vcommand9 = "grep fs.file-max /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
        vcommand10 = "grep fs.aio-max-nr /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
        vcommand11 = "grep kernel.shmall /etc/sysctl.conf | grep -v '#' | cut -d' ' -f3"
		
        scommand1 = """sudo sed -i "s/`grep net.ipv4.ip_local_port_range /etc/sysctl.conf | grep -v '#'`/net.ipv4.ip_local_port_range = 9000 65500/" /etc/sysctl.conf"""
        scommand2 = """sudo sed -i "s/`grep net.core.rmem_default /etc/sysctl.conf | grep -v '#'`/net.core.rmem_default = 262144/" /etc/sysctl.conf"""
        scommand3 = """sudo sed -i "s/`grep net.core.rmem_max /etc/sysctl.conf | grep -v '#'`/net.core.rmem_max = 4194304/" /etc/sysctl.conf"""
        scommand4 = """sudo sed -i "s/`grep net.core.wmem_default /etc/sysctl.conf | grep -v '#'`/net.core.wmem_default = 262144/" /etc/sysctl.conf"""
        scommand5 = """sudo sed -i "s/`grep net.core.wmem_max /etc/sysctl.conf | grep -v '#'`/net.core.wmem_max = 1048576/" /etc/sysctl.conf"""
        scommand6 = """sudo sed -i "s/`grep kernel.shmmax /etc/sysctl.conf | grep -v '#'`/kernel.shmmax = 2147483648/" /etc/sysctl.conf"""
        scommand7 = """sudo sed -i "s/`grep kernel.shmmni /etc/sysctl.conf | grep -v '#'`/kernel.shmmni = 4096/" /etc/sysctl.conf"""
        scommand8 = """sudo sed -i "s/`grep kernel.sem /etc/sysctl.conf | grep -v '#'`/kernel.sem = 250 32000 100 128/" /etc/sysctl.conf"""
        scommand9 = """sudo sed -i "s/`grep fs.file-max /etc/sysctl.conf | grep -v '#'`/fs.file-max = 6815744/" /etc/sysctl.conf"""
        scommand10 = """sudo sed -i "s/`grep fs.aio-max-nr /etc/sysctl.conf | grep -v '#'`/fs.aio-max-nr = 1048576/" /etc/sysctl.conf"""
        scommand11 = """sudo sed -i "s/`grep kernel.shmall /etc/sysctl.conf | grep -v '#'`/kernel.shmall = 2097152/" /etc/sysctl.conf"""

        if execCommand(vcommand1).strip() in "9000 65500":
            #print "1 " +execCommand(vcommand1).strip()+ " == "+"9000 65500"+" Yes"
            pass
        else:
            #print "1 " +execCommand(vcommand1).strip()+ " == "+"9000 65500"+" No"
            if execCommand(scommand1).strip() != "":
                count.append('1')
            else:
                count.append('0')

        if execCommand(vcommand2).strip() in "262144":
            #print "2 " +execCommand(vcommand2).strip()+ " == "+"262144"+" Yes"
            pass
        else:
            #print "2 " +execCommand(vcommand2).strip()+ " == "+"262144"+" No"
            if execCommand(scommand2).strip() != "":
                count.append('1')
            else:
                count.append('0')

        if execCommand(vcommand3).strip() in "4194304":
            #print "3 " +execCommand(vcommand3).strip()+ " == "+"4194304"+" Yes"
            pass
        else:
            #print "3 " +execCommand(vcommand3).strip()+ " == "+"4194304"+" No"
            if execCommand(scommand3).strip() != "":
                count.append('1')
            else:
                count.append('0')			

        if execCommand(vcommand4).strip() in "262144":
            #print "4 " +execCommand(vcommand4).strip()+ " == "+"262144"+" Yes"
            pass
        else:
            #print "4 " +execCommand(vcommand4).strip()+ " == "+"262144"+" No"
            if execCommand(scommand4).strip() != "":
                count.append('1')
            else:
               	count.append('0')		

        if execCommand(vcommand5).strip() in "1048576":
            #print "5 " +execCommand(vcommand5).strip()+ " == "+"1048576"+" Yes"
            pass
        else:
            #print "5 " +execCommand(vcommand5).strip()+ " == "+"1048576"+" No"
            if execCommand(scommand5).strip() != "":
                count.append('1')
            else:
                count.append('0')

        if execCommand(vcommand6).strip() in "2147483648":
            #print "6 " +execCommand(vcommand6).strip()+ " == "+"2147483648"+" Yes"
            pass
        else:
            #print "6 " +execCommand(vcommand6).strip()+ " == "+"2147483648"+" No"
            if execCommand(scommand6).strip() != "":
                count.append('1')
            else:
                count.append('0')

        if execCommand(vcommand7).strip() in "4096":
            #print "7 " +execCommand(vcommand7).strip()+ " == "+"4096"+" Yes"
            pass
        else:
            #print "7 " +execCommand(vcommand7).strip()+ " == "+"4096"+" No"
            if execCommand(scommand7).strip() != "":
                count.append('1')
            else:
                count.append('0')

        if execCommand(vcommand8).strip() in "250 32000 100 128":
            #print "8 " +execCommand(vcommand8).strip()+ " == "+"250 32000 100 128"+" Yes"
            pass
        else:
            #print "8 " +execCommand(vcommand9).strip()+ " == "+"250 32000 100 128"+" No"
            if execCommand(scommand8).strip() != "":
                count.append('1')
            else:
                count.append('0')

        if execCommand(vcommand9).strip() in "6815744":
            #print "9 " +execCommand(vcommand9).strip()+ " == "+"6815744"+" Yes"
            pass
        else:
            #print "9 " +execCommand(vcommand9).strip()+ " == "+"6815744"+" No"
            if execCommand(scommand9).strip() != "":
                count.append('1')
            else:
                count.append('0')

        if execCommand(vcommand10).strip() in "1048576":
            #print "10 " +execCommand(vcommand10).strip()+ " == "+"1048576"+" Yes"
            pass
        else:
            #print "10 " +execCommand(vcommand10).strip()+ " == "+"1048576"+" No"
            if execCommand(scommand10).strip() != "":
                count.append('1')
            else:
                count.append('0')

        if execCommand(vcommand11).strip() in "2097152":
            #print "11 " +execCommand(vcommand11).strip()+ " == "+"2097152"+" Yes"
            pass
        else:
            #print "11 " +execCommand(vcommand11).strip()+ " == "+"2097152"+" No"
            if execCommand(scommand11).strip() != "":
               count.append('1')
            else:
                count.append('0')			

        if '1' not in count:
            print "0"
            print "ExitDesc: Kernel Parameter Validation Successful!"
            log.info('Exitcode: 0')
            log.info('ExitDesc: Kernel Parameter Validation Successful!')
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Kernel Parameter Validation Successful",LogServer,LogDB,LogUser,LogPassword)
        else:
            print "10"
            print "ExitDesc: Kernel Parameter Validation Failed!"
            log.info('Exitcode: 10')
            log.info('ExitDesc: Kernel Parameter Validation Failed!')
            HLStatus.UpdateHLStatus(APID,"Stepid84","Failed","Oracle Kernel Parameter Validation Failed",LogServer,LogDB,LogUser,LogPassword)
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Kernel Parameter Validation Failed",LogServer,LogDB,LogUser,LogPassword)
    except Exception, e:
        print "1"
        print "ExitDesc: {0}".format(e)
        log.info('Exitcode: 1')
        log.info('ExitDesc: {0}'.format(e))
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error",e,LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid84","Failed","Oracle Kernel Parameter Script Failed due to soome exception",LogServer,LogDB,LogUser,LogPassword)
    finally:
        s.close()	
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('Exitcode: 10')
    log.info('ExitDesc: Missing Arguments')
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Missing Arguments",LogServer,LogDB,LogUser,LogPassword)
    HLStatus.UpdateHLStatus(APID,"Stepid84","Failed","Oracle Kernel Parameter Validation Script Failed, Missing Argument",LogServer,LogDB,LogUser,LogPassword)
