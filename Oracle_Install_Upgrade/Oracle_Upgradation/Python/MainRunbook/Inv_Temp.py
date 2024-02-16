"""
	Name: Invalid_Objects.py
	Description: Executed from HP OO, To Capture Invalid Objects
	Team: Software Service Automation
	Author: Vinaykumar Kalyankar(Vinay.Kalyankar@capgemini.com)
	Inputs: Arguments [Hostname,DBUsername,DBPassword,TNSName], LogFileLoc
	Output: ScriptCode, ScriptDesc(Log File)
	
"""

#!/usr/bin/env python
from sys import path
import sys
import logging as log
import time
import datetime
from os import system,getcwd,path,makedirs
import ActivityLogger
import socket
import paramiko
import re
import HLStatus
try:
    filename = "Invalid_Objects_POST.log"
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
ActivityName = "Invalid Objects Task"
Des = "Invalid Objects Task"
s = socket.socket()

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 13:
        LogServer = sys.argv[1]
        LogDB = sys.argv[2]
        APID = sys.argv[3]
        LogAccountName = sys.argv[4]
        LogUser=sys.argv[5]
        LogPwd=sys.argv[6]
        ##Script Variables##
        Hostname = sys.argv[7]  #Target HostName  	
        OsUser = sys.argv[8]	#Target Database user to connect to listener
        OsPass = sys.argv[9]	#Target Database user password to connect to listener
        OraHomes =sys.argv[10]	#Target TNS Name
        TNSNames=sys.argv[11]
        Stepid=sys.argv[12]
        CIServer = Hostname
        address = Hostname
        port = 22
        DBSizeList=[]
        #Connectivity Test #
        ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        HLStatus.UpdateHLStatus(APID,Stepid,"In Progress","Oracle Post Check- Fetch Invalid objects script is getting executed.",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			
        log.info('{0} host is reachable'.format(Hostname))

        def db_conn(OraHome,Hostname,OUser,OsPass):
            command = """. ~/.bash_profile 
export ORACLE_HOME={0}
export ORACLE_PATH={0}\bin:$PATH
sqlplus / as sysdba <<EOF
select owner from dba_objects where status='VALID' group by owner;
exit;
EOF""".format(OraHome)
            dssh = paramiko.SSHClient()
            dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            dssh.connect(Hostname, username=OsUser, password=OsPass)
            log.info('Succesfully connected  to Server')
            log.info("Executing the command...\n{}".format(command))        
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            error = stderr.read()
            log.info('Output : {0}'.format(output))
            output=output.split("\n")
            r=re.compile(".* rows selected.")
            matchLi=filter(r.match,output)
            log.info('Matchedline : {0}'.format(matchLi))			
            if len(matchLi) == 0:
                r1=re.compile("no rows selected")
                matchLi1=filter(r1.match,output)
                if len(matchLi1) == 0:
                    log.info('Matchedline : Only one row selected')
                    return 1
                else:
                    log.info('Matchedline : {0}'.format(matchLi1))
                    return 0
            else:							
                line=matchLi[0]
                n=line.split("rows selected")
                return n[0]

        if "," in OraHomes:
            OraHomes = OraHomes.split(",")
            for OraHome in OraHomes:
                SizeList = db_conn(OraHome,Hostname,OsUser,OsPass)
            invalidcount=len(SizeList)

        else:
            SizeList = db_conn(OraHomes,Hostname,OsUser,OsPass)
            if SizeList == 0:
                SizeList=""
            invalidcount=len(SizeList)

        log.info('Total count of Invalid Objects : {0}'.format(invalidcount))
        if invalidcount == 0:
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Invalid Object doesnt Exist",LogServer,LogDB,LogUser,LogPwd)
            log.info('0')
            log.info('ExitDesc:Invalid Object doesnt Exist')
            print "0"
            print "ExitDesc: Invalid Object doesnt Exist"	

        else:
            log.info('0')
            log.info('ExitDesc:Invalid Object  Exist')
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Invalid Object  Exist",LogServer,LogDB,LogUser,LogPwd)
            print "0"
            print "ExitDesc: Invalid Object  Exist"	

            if isinstance(TNSNames, list):
                le=len(TNSNames)
                for i in range(le):
                    print TNSNames[i],SizeList[i]

            else:
                SizeList = str(SizeList).translate(None, "[( ',	)]")
                print TNSNames,SizeList
				
    else:
        log.info('10')
        log.info('ExitDesc:Missing Arguments')
        print "10"
        print "ExitDesc: Missing Arguments"

except Exception, e:
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error",LogServer,LogDB,LogUser,LogPwd)
    log.info('Error: {0}'.format(e))
    print "1"
    print "ExitDesc: Script Failed. Look into logs for more details."
    HLStatus.UpdateHLStatus(APID,Stepid,"Failed","Oracle Post Check- Fetch Invalid objects script failed.",LogServer,LogDB,LogUser,LogPwd)