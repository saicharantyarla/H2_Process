"""
	Name: create_pfile.py
	Description: Executed from HP OO, To Create PFile from SPFile
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
import cx_Oracle as dbc
import HLStatus
try:
    filename = "create_pfile.log"
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
ActivityName = "Create PFile from SPFile"
Des = "Create PFile from SPFile"
s = socket.socket()

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 11:
        LogServer = sys.argv[1]
        LogDB = sys.argv[2]
        APID = sys.argv[3]
        LogAccountName = sys.argv[4]
        LogUser=sys.argv[5]
        LogPwd=sys.argv[6]
        ##Script Variables##
        Hostname = sys.argv[7]  #Target HostName  	
        DbUser = sys.argv[8]	#Target Database user to connect to listener
        DbPass = sys.argv[9]	#Target Database user password to connect to listener
        TNSNames =sys.argv[10]	#Target TNS Name
        CIServer = Hostname
        address = Hostname
        port = 22
        count=0
        TNS=""
        #Connectivity Test #
        ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
        HLStatus.UpdateHLStatus(APID,"Stepid100","In Progress","Oracle Upgradation Environment Setup is in Progress which is executing Create Pfile script",LogServer,LogDB,LogUser,LogPwd)	 	
        log.info('{0} host is reachable'.format(Hostname))

        def db_conn(TNSName, DbUser, DbPass):

            query="create pfile from spfile"
            log.info('Trying to connect to Database for TNS {0} '.format(TNSName))
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to connect to TNS Server",LogServer,LogDB,LogUser,LogPwd)
            ## Database Connection String ##
            conn=dbc.connect(dsn=TNSName,user=DbUser,password=DbPass,mode=dbc.SYSDBA)
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Connected to TNS Server",LogServer,LogDB,LogUser,LogPwd)
            cur=conn.cursor()
            log.info('Succesfully connected  to Database for TNS {0} '.format(TNSName))
            log.info('Executing Query:\n{0}'.format(query))
            cur.execute(query)
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Query Executed",LogServer,LogDB,LogUser,LogPwd)
            cur.close()
            conn.close()
            return "True"


        if "," in TNSNames:
            TNSNames = TNSNames.split(",")
            for TNSName in TNSNames:
                status = db_conn(TNSName,DbUser, DbPass)
                if status == "True":
                    TNS = TNS+TNSName+","
                    count = count+1

        else:
            status = db_conn(TNSNames,DbUser, DbPass)
            count = count+1


        if count > 0:
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","PFile Creation Succesfull",LogServer,LogDB,LogUser,LogPwd)
            log.info('0')
            log.info('ExitDesc:PFile Creation Succesfull')
            print "0"
            print "ExitDesc: PFile Creation Succesfull"	

        else:
            log.info('1')
            log.info('ExitDesc:PFile Creation Failed')
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","PFile Creation Failed",LogServer,LogDB,LogUser,LogPwd)
            HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Create PFile Script failed",LogServer,LogDB,LogUser,LogPwd)	
            print "1"
            print "ExitDesc: PFile Creation Failed"	

        if TNS:
            TNS=TNS.rstrip(",")
            print TNS
			
    else:
        log.info('10')
        log.info('ExitDesc:Missing Arguments')
        print "10"
        print "ExitDesc: Missing Arguments"

except Exception, e:
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Error",LogServer,LogDB,LogUser,LogPwd)
    HLStatus.UpdateHLStatus(APID,"Stepid100","Failed","Oracle Upgradation- Create PFile Script failed",LogServer,LogDB,LogUser,LogPwd)	
    log.info('Error: {0}'.format(e))
    print "1"
    print "ExitDesc: Script Failed. Look into logs for more details."
    if TNS:
        TNS=TNS.rstrip(",")
        print TNS