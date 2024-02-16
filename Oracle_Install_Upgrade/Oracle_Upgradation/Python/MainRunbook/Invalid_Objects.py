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
import cx_Oracle as dbc
import HLStatus
try:
    filename = "Invalid_Objects.log"
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
ActivityName = "Invalid Objects"
Des = "Fetches Invalid Objects"
s = socket.socket()

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 12:
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
        Stepid =sys.argv[11]	#StepId
        CIServer = Hostname
        address = Hostname
        port = 22
        DBSizeList=[]
        #Connectivity Test #
        ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port)) 
			
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPwd)
			
        log.info('{0} host is reachable'.format(Hostname))

        def db_conn(TNSName, DbUser, DbPass):

            query="select owner from dba_objects where status='VALID' group by owner"
            log.info('Trying to connect to Database for TNS {0} '.format(TNSName))
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to connect to TNS Server",LogServer,LogDB,LogUser,LogPwd)
            ## Database Connection String ##
            HLStatus.UpdateHLStatus(APID,Stepid,"In Progress","Oracle Upgradation Pre Check is in Progress which is executing Fetch Invalid Objects script",LogServer,LogDB,LogUser,LogPwd)	
            conn=dbc.connect(dsn=TNSName,user=DbUser,password=DbPass,mode=dbc.SYSDBA)
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Connected to TNS Server",LogServer,LogDB,LogUser,LogPwd)
            cur=conn.cursor()
            log.info('Succesfully connected  to Database for TNS {0} '.format(TNSName))
            log.info('Executing Query:\n{0}'.format(query))
            cur.execute(query)
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Query Executed",LogServer,LogDB,LogUser,LogPwd)
            out = cur.fetchall()
            log.info('Output : {0}'.format(out))
            opout=len(out)
            log.info('Length of Invalid Objects : {0}'.format(opout))
            DBSizeList.append(opout)

            cur.close()
            conn.close()
            return DBSizeList


        if "," in TNSNames:
            TNSNames = TNSNames.split(",")
            for TNSName in TNSNames:
                SizeList = db_conn(TNSName,DbUser, DbPass)

            invalidcount=len(SizeList)

        else:
            SizeList = db_conn(TNSNames,DbUser, DbPass)
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
    HLStatus.UpdateHLStatus(APID,Stepid,"Failed","Oracle Upgradation- Fetching Invalid Object Script failed",LogServer,LogDB,LogUser,LogPwd)