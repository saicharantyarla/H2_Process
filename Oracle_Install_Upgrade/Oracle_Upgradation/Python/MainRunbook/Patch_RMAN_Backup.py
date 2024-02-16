"""
	Name: Patch_RMAN_Backup.py
	Description: Executed from HP OO, to Full_Backup to DISK
	Team: Software Service Automation
	Author: VinayKumar Kalyankar(vinay.kalyankar@capgemini.com)
	Inputs: Arguments [Hostname,Username,Password,DBUser,DBpassword,TNSNames,FRAUsed,FRApath,Channel_No]
	Output: ScriptCode, ScriptDesc(Log File)
	
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
import cx_Oracle as dbc
import ActivityLogger
import HLStatus
import socket

try:
    filename = "Patch_RMAN_Backup.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Upgradation"
    filename = "%s\%s" %(filepath,filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "Unable to create Logfile {0}".format(filename)

# Variable Mapping #
ActivityName = "RMAN Backup for Patch"
Des = "RMAN Backup for Patch"
s = socket.socket()

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 17:
        LogServer = sys.argv[1]
        LogDB = sys.argv[2]
        APID = sys.argv[3]
        LogAccountName = sys.argv[4]
        LogUser=sys.argv[5]
        LogPwd=sys.argv[6]
        ##Script Variables##
        Hostname = sys.argv[7] #Target HostName  	
        osuser = sys.argv[8] #Target Host user name to connect 
        ospassword = sys.argv[9] #Target Host user password to connect
        DbUser = sys.argv[10]	#Target Host user name to connect 
        DbPass = sys.argv[11]	#Target Host user password to connect
        TNSNames = sys.argv[12]	#TNSNames
        FRAUsed = sys.argv[13] #Use Flash Recovery Area [Yes/No]
        FRApath = sys.argv[14] #if FRAUsed == YES Check if the FRA and size are set, if FRAUsed == NO take the input backup path. [Path format <PATH TAKEN AS INPUT>/<DATBASE_NAME>]		
        ChannelNo = sys.argv[15] #No of Channels
        ArchiveDeletion = sys.argv[16] # Condition to delete the archive log 
        ChannelNo = int(ChannelNo)
        CIServer = Hostname
        address = Hostname
        port = 22 
        #Connectivity Test #
        ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        HLStatus.UpdateHLStatus(APID,"Stepid99","In Progress","Oracle Upgradation Pre Check is in Progress which is executing Fetch Invalid Objects script",LogServer,LogDB,LogUser,LogPwd)		
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			
        log.info('{0} host is reachable'.format(Hostname))
        tns_names = []

        def get_cmd(TNSName,DbUser,DbPass,FRAUsed,FRApath,ChannelNo,ArchiveDeletion):

            ChannelAllocation = ""
            if FRAUsed.lower() == 'yes':		
                conn=dbc.connect(dsn=TNSName,user=DbUser,password=DbPass,mode=dbc.SYSDBA)
                cur=conn.cursor()
                log.info('Succesfully connected  to Database for TNS {0} '.format(TNSName))

                query = "select value from v$parameter where name='db_recovery_file_dest'"
                log.info('Executing Query: {0}'.format(query))
                cur.execute(query)
                db_recovery_file_dest = cur.fetchall()
                log.info('db_recovery_file_dest Output: {0}'.format(db_recovery_file_dest))

                query1 = "select value/1024/1024/1024 from v$parameter where name='db_recovery_file_dest_size'"
                log.info('Executing Query: {0}'.format(query1))
                cur.execute(query1)
                db_recovery_file_dest_size = cur.fetchall()
                log.info('db_recovery_file_dest_size Output: {0}'.format(db_recovery_file_dest_size))
		
                if db_recovery_file_dest and db_recovery_file_dest_size:
                    for i in range(ChannelNo):
                        ChannelAllocation += "allocate channel C"+str(i+1)+" type DISK;"
                        if i < ChannelNo-1:
                            ChannelAllocation += "\n"
                else:
                    log.info("ScriptDesc: The FRA option is yes but, db_recovery_file_dest or db_recovery_file_dest_size is not set")
                    print "ScriptCode:10"
                    print "ScriptDesc:The FRA option is given true but, db_recovery_file_dest or db_recovery_file_dest_size is not set."
                    sys.exit()
	    
            elif FRAUsed.lower() == 'no':
                for i in range(ChannelNo):
                    ChannelAllocation += "allocate channel C"+str(i+1)+" type DISK format '"+FRApath+"_%t_s%s_s%p';"	
                    if i < ChannelNo-1:
                        ChannelAllocation += "\n"
	
            ChannelRelease = ""
            for i in range(ChannelNo):
                ChannelRelease += "release channel C"+str(i+1)+";"
                if i < ChannelNo-1:
	                ChannelRelease += "\n"
				
            DeleteArchive = ""
            if ArchiveDeletion.lower() == "yes":
                DeleteArchive = "backup database plus archivelog delete input;"
            elif ArchiveDeletion.lower() == "no":
                DeleteArchive = "backup database plus archivelog;"
	
            command=""". ~/.bash_profile
export ORACLE_SID="""+TNSName+"""
export PATH=$ORACLE_HOME/bin:$PATH
${ORACLE_HOME}/bin/rman <<EOF
connect target /
connect auxiliary /
run {
"""+ChannelAllocation+"""
"""+DeleteArchive+"""
"""+ChannelRelease+"""
}
EOF"""
            return command

        def exec_cmd(Hostname,osuser,ospassword,command):
            count = 0
            log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname,osuser))
            ## Connection to the remote host ##
            dssh = paramiko.SSHClient()
            dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            dssh.connect(Hostname, username=osuser, password=ospassword)
            log.info('Succesfully connected  to the host {0} '.format(Hostname))
            log.info('Executing the command :{0}'.format(command))
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Executing the Backup command",LogServer,LogDB,LogUser,LogPwd)
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            errout = stderr.read()
		
            log.info('Output :{0}'.format(output))
            if output is not None:
                output = output.splitlines(True)
                for out in output:
                    if 'ORA-' not in out or 'TNS-' not in out or 'RMAN-' not in out:
                        count = 1
            if count == 1:
                return "true"
            else:
                return "false"



        if "," in TNSNames:
            TNSNames = TNSNames.split(",")
            for TNSName in TNSNames:
                command = get_cmd(TNSName,DbUser,DbPass,FRAUsed,FRApath,ChannelNo,ArchiveDeletion)
                status = exec_cmd(Hostname,osuser,ospassword,command)
                if status == 'true':
                    tns_names.append(TNSName)

        else:
            command = get_cmd(TNSNames,DbUser,DbPass,FRAUsed,FRApath,ChannelNo,ArchiveDeletion)
            status = exec_cmd(Hostname,osuser,ospassword,command)
            if status == 'true':
                tns_names.append(TNSNames)



        if tns_names:
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","RMAN Backup Successful",LogServer,LogDB,LogUser,LogPwd)
            log.info('RMAN Backup Successful! for the following TNSName: {0}'.format(tns_names))
            log.info('ScriptCode: 0')
            log.info('ScriptDesc: RMAN Backup Successful!')
            print "0"
            print "ExitDesc: RMAN Backup Successful! for the following Databases"
            print "TNSNames: {0}".format(tns_names)
        else:
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","RMAN Backup Failed",LogServer,LogDB,LogUser,LogPwd)
            HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- Take RMAN Backup Script failed",LogServer,LogDB,LogUser,LogPwd)
            log.info('ScriptCode: 10')
            log.info('ScriptDesc: RMAN Backup Failed!')
            print "10"
            print "ExitDesc: RMAN Backup Failed!"
    else:
        print "10"
        print "ExitDesc: Missing Arguments"
        log.info('ExitCode: 10')
        log.info('ExitDesc: Missing Arguments')
except Exception, e:
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error",LogServer,LogDB,LogUser,LogPwd)
    HLStatus.UpdateHLStatus(APID,"Stepid99","Failed","Oracle Upgradation- Take RMAN Backup Script failed",LogServer,LogDB,LogUser,LogPwd)
    log.info('Error: {0}'.format(e))
    print "1"
    print "ExitDesc: {0}".format(e)
    if tns_names:
        print "RMAN Backup Successful for: {0}".format(tns_names)