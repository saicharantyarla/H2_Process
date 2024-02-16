"""
	Name: ComparePreandPostInvalidObj.py
	Description: Executed from HP OO, to compare Pre and Post Check
	Team: Software Service Automation
	Author: Sravani
	Inputs: Arguments [Hostname,PreValue,PostValue], LogFileLoc
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
import ActivityLogger
import HLStatus
import re


try:
    filename = "ComparePreandPostInvalidObj.txt"
    filepath = 'C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Upgradation'
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
ActivityName = "ComparePreandPostInvalidObj"
Des = "Compares Prechecks and Post checks invalid objects"
a=0

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 10:
        LogServer = sys.argv[1]
        LogDB = sys.argv[2]
        APID = sys.argv[3]
        LogAccountName = sys.argv[4]
        LogUser=sys.argv[5]
        LogPwd=sys.argv[6]
        ##Script Variables##
        Hostname=sys.argv[7]
        PreValue=sys.argv[8]
        PostValue=sys.argv[9]
        CIServer=Hostname		
        PreValueList=re.split('[\n ]',PreValue)
        PostValueList=re.split('[\n ]',PostValue)
        PreValueLen=len(PreValueList)
        AffTNSList=[]
        UnAffTNSList=[]		
        AffStr=""
        UnAffStr=""
        ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Comparing thr Pre and Pst Value",LogServer,LogDB,LogUser,LogPwd)	
        HLStatus.UpdateHLStatus(APID,"Stepid102","In Progress","Oracle Post Check is in Progress which is executing Compare pre and post Invalid Objects Count script",LogServer,LogDB,LogUser,LogPwd)	
        log.info('Comparing the Pre and Post Value')
        PreLen=len(PreValueList)
        i=0
        while i < PreValueLen:  
            
            if  int(PreValueList[i+1]) < int(PostValueList[i+1]):
                AffTNSList.append(PreValueList[i])
            else:
                UnAffTNSList.append(PreValueList[i])
            i=i+2
        AffStr=",".join(AffTNSList)
        UnAffStr=",".join(UnAffTNSList)
        print "0"
        log.info('ExitCode:0')
        if len(AffTNSList) == 0:
            print "ExitDesc: Invalid Objects is lesser or equal after applying the Patch"
            log.info('Info: Invalid Objects is lesser or equal after applying the Patch')
            ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Invalid Objects is lesser or equal after applying the Patch",LogServer,LogDB,LogUser,LogPwd)
        else:
            if len(UnAffTNSList) == 0:
                print "ExitDesc: Invalid objects have increased after applying Patch for following TNSNames: %s" %(AffStr)
                log.info('Info: Invalid objects have increased after applying Patch for following TNSNames:{0}'.format(AffStr))
            else:
                print "ExitDesc: Invalid objects have increased after applying Patch to the following TNSNames: %s while unaffected TNSNAmes are: %s" %(AffStr,UnAffStr)
                log.info('Invalid objects have increased after applying Patch to the following TNSNames: {0} while unaffected TNSNAmes are: {1}'.format(AffStr,UnAffStr))
            ActivityLogger.WriteActivityLog( APID	,CIServer,ActivityName,Des,"Completed",LogAccountName, "No Error","Some TNSNAMEs are affected.Check the logs.",LogServer,LogDB,LogUser,LogPwd)	
    else:
        print "1"
        print "ExitDesc: Missing Arguments"
        log.info('Exitcode: 1')
        log.info('ExitDesc: Missing Arguments')
        
except Exception, e:
    log.info('Error: {0}'.format(e))
    print "1"
    print "ExitDesc: {0}".format(e)
    ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"Completed",LogAccountName, "Error","Exception faced with script.Check Logs",LogServer,LogDB,LogUser,LogPwd)	
    HLStatus.UpdateHLStatus(APID,"Stepid102","Failed","Oracle Post Check- Compare pre and post object count Script failed",LogServer,LogDB,LogUser,LogPwd)