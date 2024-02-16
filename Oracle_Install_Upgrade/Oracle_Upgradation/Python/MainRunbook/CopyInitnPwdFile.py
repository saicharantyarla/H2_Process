"""
	Name: Oracle_copy_pfile_and_pwdfile
	Description: Executed from HPOO, to copy pfile and passwd file to 12G home from 11G home
	Team: Software Service Automation
	Author: Vikrant Kumar(vikrant.a.kumar@capgemini.com)
	Inputs: Arguments [Hostname,Username,Password,LocalPath,RemotePath], LogFileLoc
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
    filename = "Oracle_copy_pfile_and_pwdfile.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Upgradation"
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
ActivityName = "Oracle_copy_pfile_and_pwdfile"
Des = "Copy pfile and passwd file to 12G home from 11G home"
s = socket.socket()

log.info('Input Variables mapping...')
if len(sys.argv) == 13:
    #LogVariable Mapping
    LogServer = sys.argv[1]
    LogDB = sys.argv[2]
    APID = sys.argv[3]
    LogAccountName = sys.argv[4]
    LogUser = sys.argv[5]
    LogPassword = sys.argv[6]

    ##Script Variables##
    HostName = sys.argv[7] #Server HostName  	
    UserName = sys.argv[8] #Server User Name 
    Password = sys.argv[9] #Server Password
    LocalPath = sys.argv[10] #Source Path
    RemotePath = sys.argv[11] #Target Path
    DBName = sys.argv[12] #Database Name

    CIServer = HostName
    address = HostName
    port = 22

    #Connectivity Test #		
    ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPassword)
    log.info('Checking connectivity to the host : {0}'.format(HostName))
    try:
        s.connect((address, port)) 

        log.info('{0} host is reachable'.format(HostName))
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPassword)			
        HLStatus.UpdateHLStatus(APID,"Stepid100","In Progress","Oracle Upgradation Environment Setup is in Progress which is executing Copy Init and Password File script",LogServer,LogDB,LogUser,LogPassword)	 
        ## Connection to the remote host ##
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying SSH Connection to the host",LogServer,LogDB,LogUser,LogPassword)
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(HostName,UserName))        
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(HostName, username = UserName, password = Password)

        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesfull to the host",LogServer,LogDB,LogUser,LogPassword)
        log.info('Succesfully connected  to the host {0} '.format(HostName))

        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to execute commnd on remote host",LogServer,LogDB,LogUser,LogPassword)
        log.info('Executing the command...')

        def execCommand(command):
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            errout = stderr.read()
            log.info('Output :{0}'.format(output))
            return output+"\n"+errout

        command1 = """DIRECTORY1={0}/dbs
DIRECTORY2={1}/dbs
if [ -d "$DIRECTORY1" -a -d "$DIRECTORY2" ]; then
  echo "Yes"
else
  echo "No"
fi""".format(LocalPath,RemotePath)

        command2 = """cd {0}/dbs
File1=init{1}.ora
File2=orapw{1}
if [ -f "$File1" -a -f "$File2" ]; then
  echo "Yes"
else
  echo "No"
fi""".format(LocalPath,DBName)

        command3 = """cd {0}/dbs
cp init{2}.ora {1}/dbs
cp orapw{2} {1}/dbs
""".format(LocalPath,RemotePath,DBName)

        command4 = """cd {0}/dbs
File1=init{1}.ora
File2=orapw{1}
if [ -f "$File1" -a -f "$File2" ]; then
  echo "Yes"
else
  echo "No"
fi""".format(RemotePath,DBName)

        #print "Command1..."
        #print command1
        #print "=========================="
        if 	execCommand(command1).strip() == "Yes":
            #print "Command2..."
            #print command2
            #print "========================="
            if execCommand(command2).strip() == "Yes":
                #print "Command3..."
                #print "========================="
                execCommand(command3)
                if execCommand(command4).strip() == "Yes":
                    print "0"
                    print "ExitDesc: File Copy is successful!"
                    log.info('Exitcode: 0')
                    log.info('ExitDesc: File Copy is Successful!')
                    ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","File Copy is Successful!",LogServer,LogDB,LogUser,LogPassword)
                else:
                    print "1"
                    print "ExitDesc: File Copy is failed!"
                    log.info('Exitcode: 1')
                    log.info('ExitDesc: File Copy is failed!')
                    ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","File Copy is failed!",LogServer,LogDB,LogUser,LogPassword)
                    HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Copy init and Password file Script failed",LogServer,LogDB,LogUser,LogPassword)	
            else:
                print "10"
                print "ExitDesc: init"+DBName+".ora and/or orapw"+DBName+" files doesnot exist in the given local path!"
                log.info('Exitcode: 10')
                log.info('ExitDesc: init'+DBName+'.ora and orapw'+DBName+' files doesnot exist in the given local path!')
                ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","initcgsi.ora and/or orapwcgsi files doesnot exist in the given local path!",LogServer,LogDB,LogUser,LogPassword)            
                HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Copy init and Password file Script failed",LogServer,LogDB,LogUser,LogPassword)
        else:
            print "10"
            print "ExitDesc: Folder provoded doesnot exist!"
            log.info('Exitcode: 10')
            log.info('ExitDesc: Folder provoded doesnot exist!')
            ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Folder provoded doesnot exists!",LogServer,LogDB,LogUser,LogPassword)
            HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Copy init and Password file Script failed",LogServer,LogDB,LogUser,LogPassword)	
    except socket.error, e:
        print "10"
        print "ExitDesc: {0}".format(e)
        log.info('Exitcode: 10')
        log.info('ExitDesc: {0}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"Error",str(e),LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Copy init and Password file Script failed",LogServer,LogDB,LogUser,LogPassword)			
    except paramiko.SSHException, e:
        print "10"
        print "ExitDesc: {0}".format(e)
        log.error('Exitcode: 10')
        log.error('ExitDesc: {0}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error",str(e),LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Copy init and Password file Script failed",LogServer,LogDB,LogUser,LogPassword)			
    except Exception, e:
        print "10"
        print "ExitDesc: {0}".format(e)
        log.error('Exitcode: 10')
        log.error('ExitDesc: {0}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error",str(e),LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Copy init and Password file Script failed",LogServer,LogDB,LogUser,LogPassword)		
    finally:
        s.close()
        dssh.close()
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info('Exitcode: 10')
    log.info('ExitDesc: Missing Arguments')