"""
	Name: Check_required_packages.py
	Description: It will check required packages are installed or not
	Team: Software Service Automation
	Author: Gaurav Pandey(gaurav.a.pandey@capgemini.com)
	Inputs: Arguments [Hostname,Username,Password,TNSName,Directory_Name,User_Table], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)

"""

# !/usr/bin/env python
from sys import path
import sys
import logging as log
import time
import datetime
from os import system, getcwd, path, makedirs
import socket
import paramiko
import os
import re
# import cx_Oracle as dbc
import ActivityLogger
import HLStatus
# import HLStatus

try:
    filename = "Check_required_packages.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
    filename = "%s\%s" % (filepath, filename)
    if not path.exists(filepath):
        makedirs(filepath)
    log.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=log.DEBUG)
    log.info('*************************************************************************')
    log.info('Started Script Execution')
except Exception, e:
    print "1"
    print "Unable to create Logfile {0}".filename

# Variable Mapping #
ActivityName = "Check_required_packages"
Des = "It will check required packages are installed or not"
s = socket.socket()

try:
    log.info('Input Variables mapping...')
    if len(sys.argv) == 10:
        LogServer = sys.argv[1]
        LogDB = sys.argv[2]
        APID = sys.argv[3]
        LogAccountName = sys.argv[4]
        LogUser = sys.argv[5]
        LogPwd = sys.argv[6]
        ##Script Variables##
        Hostname = sys.argv[7]  # Target HostName
        osuser = sys.argv[8]  # Target Host user name to connect
        ospassword = sys.argv[9]  # Target Host user password to connect

        CIServer = Hostname
        address = Hostname
        port = 22

        count = 0

        # Connectivity Test #
        HLStatus.UpdateHLStatus(APID,"Stepid96","In Progress","Installed Packages Check is In Progress",LogServer,LogDB,LogUser,LogPwd)
        ActivityLogger.InsertActivityLog(APID, CIServer, ActivityName, Des, "Initiated", LogAccountName, "No Error","Connectivity check initiated", LogServer, LogDB, LogUser, LogPwd)
        log.info('Checking connectivity to the host : {0}'.format(Hostname))

        s.connect((address, port))

        ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName, "No Error", "Host is reachable", LogServer, LogDB, LogUser, LogPwd)

        log.info('{0} host is reachable'.format(Hostname))

        command = "rpm -q binutils glibc libstdc++ libaio libXext libXtst libX11 libXau libxcb libXi make sysstat compat-libcap1 compat-libstdc++-33 gcc gcc-c++ glibc-devel ksh libstdc++-devel libaio-devel"
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(Hostname, osuser))
        ## Connection to the remote host ##
        ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName, "No Error","Trying SSH Connection to the host", LogServer, LogDB, LogUser, LogPwd)
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(Hostname, username=osuser, password=ospassword)
        log.info('Succesfully connected  to the host {0} '.format(Hostname))
        ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName, "No Error","SSH Connection succesfull to the host", LogServer, LogDB, LogUser, LogPwd)
        log.info('Executing the command :{0}'.format(command))
        ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName, "No Error","Trying to execute commnd on remote host", LogServer, LogDB, LogUser, LogPwd)
        stdin, stdout, stderr = dssh.exec_command(command)
        output = stdout.read()
        errout = stderr.read()
        lis=[]
        Package_Inst=[]
        Package_Notinst=[]
        Package_update=[]
        pack_name=['binutils-2.20.51.0.2-5.11.e16','glibc-2.12.1-7.e16','libstdc++-4.4.4-13.el6','libaio-0.3.107-10.el6','libXext-1.1','libXtst-1.0.99.2','libX11-1.3','libXau-1.0.5','libxcb-1.5','libXi-1.3','make-3.81-19.el6','sysstat-9.0.4-11.el6','compat-libcap1-1.10-1','compat-libstdc++-33-3.2.3-69.el6','gcc-4.4.4-13.el6','gcc-c++-4.4.4-13.el6','glibc-devel-2.12-1.7.el6','ksh','libstdc++-devel-4.4.4-13.el6','libaio-devel-0.3.107-10.el6']
        package_version=['2.20.51.0.2.5.11','2.12.1.7','4.4.4.13','0.3.107.10','1.1','1.0.99.2','1.3','1.0.5','1.5','1.3','3.81.19','9.0.4.11','1.10.1','33.3.2.3.69','4.4.4.13','4.4.4.13','2.12.1.7','0','4.4.4.13','0.3.107.10']
        
        for i in output.splitlines():
            if "not installed" in i:
                Package_Notinst.append(i)
            elif ".x86_64" in i:
                lis.append(i)
##############################################################################
        def check(indexno,command):
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            output=output.strip()
            errout = stderr.read()
            if "not installed" in output:
                a= "not installed"
                return a
            elif not output :
                a= "not installed"
                return a
            else:
                package=[]
                output=output.replace("-",".")
                output=output.split()
                package.append(output)
                s_vers = [tuple([int(x) for x in n.split('.')]) for n in package[0]]
                #print s_vers

                a=package_version[indexno]
                #print a
                a=a.split()
                aa=[]
                aa.append(a)
                s_vers1=[tuple([int(x) for x in n.split('.')]) for n in aa[0]]
                a=s_vers[0] >= s_vers1[0]
                return a
##############################################################################                
#Binutils
        a= check(0,"rpm -q binutils | cut -d- -f2,3 | sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[0])
        elif a=="not installed":
            Package_Notinst.append(pack_name[0])
            
        else:
            Package_Inst.append(pack_name[0])
                
##############################################################################
#Glibc
        a= check(1,"rpm -q glibc |sed -n 1p  |cut -d- -f3,2|sed 's/.el6.x86_64//'")
        #a= check(1," rpm -q glibc |cut -d- -f3,2|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[1])
        elif a=="not installed":
            Package_Notinst.append(pack_name[1])
        else:
            Package_Inst.append(pack_name[1])
            
##############################################################################
#libstdc++
        a= check(2,"rpm -q libstdc++ | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[2])
        elif a=="not installed":
            Package_Notinst.append(pack_name[2])
        else:
            Package_Inst.append(pack_name[2])
##############################################################################
#libaio
        a= check(3,"rpm -q libaio | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[3])
        elif a=="not installed":
            Package_Notinst.append(pack_name[3])
        else:
            Package_Inst.append(pack_name[3])
##############################################################################
#libXext
        a= check(4," rpm -q libXext | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[4])
        elif a=="not installed":
            Package_Notinst.append(pack_name[4])
        else:
            Package_Inst.append(pack_name[4])
##############################################################################
#libXtst
        a= check(5," rpm -q libXtst  | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[5])
        elif a=="not installed":
            Package_Notinst.append(pack_name[5])
        else:
            Package_Inst.append(pack_name[5])
##############################################################################
#libX11
        a= check(6,"rpm -q libX11| sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[6])
        elif a=="not installed":
            Package_Notinst.append(pack_name[6])
        else:
            Package_Inst.append(pack_name[6])
##############################################################################
#libXau
        a= check(7," rpm -q libXau | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[7])
        elif a=="not installed":
            Package_Notinst.append(pack_name[7])
        else:
            Package_Inst.append(pack_name[7])
##############################################################################
#libxcb
        a= check(8,"rpm -q libxcb | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[8])
        elif a=="not installed":
            Package_Notinst.append(pack_name[8])
        else:
            Package_Inst.append(pack_name[8])
##############################################################################
#libXi 
        a= check(9," rpm -q libXi | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[9])
        elif a=="not installed":
            Package_Notinst.append(pack_name[9])
        else:
            Package_Inst.append(pack_name[9])
##############################################################################
#make 
        a= check(10," rpm -q make | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[10])
        elif a=="not installed":
            Package_Notinst.append(pack_name[10])
        else:
            Package_Inst.append(pack_name[10])
##############################################################################
#sysstat  
        a= check(11,"  rpm -q sysstat | sed -n 1p|cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[11])
        elif a=="not installed":
            Package_Notinst.append(pack_name[11])
        else:
            Package_Inst.append(pack_name[11])
##############################################################################
#compat-libcap1   
        a= check(12,"rpm -q compat-libcap1 | sed -n 1p|cut -d- -f3,4|sed 's/.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[12])
        elif a=="not installed":
            Package_Notinst.append(pack_name[12])
        else:
            Package_Inst.append(pack_name[12])
##############################################################################
# compat-libstdc++-33   
        a= check(13,"rpm -q compat-libstdc++-33 |sed -n 1p | cut -d- -f3,4,5|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[13])
        elif a=="not installed":
            Package_Notinst.append(pack_name[13])
        else:
            Package_Inst.append(pack_name[13])
##############################################################################
# compat-libstdc++-33   
        a= check(13,"rpm -q compat-libstdc++-33 |sed -n 1p | cut -d- -f3,4,5|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[13])
        elif a=="not installed":
            Package_Notinst.append(pack_name[13])
        else:
            Package_Inst.append(pack_name[13])
##############################################################################
# gcc   
        a= check(14," rpm -q gcc |sed -n 1p | cut -d- -f2,3|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[14])
        elif a=="not installed":
            Package_Notinst.append(pack_name[14])
        else:
            Package_Inst.append(pack_name[14])
##############################################################################
# gcc-c++   
        a= check(15," rpm -q gcc-c++ |sed -n 1p | cut -d- -f3,3,4|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[15])
        elif a=="not installed":
            Package_Notinst.append(pack_name[15])
        else:
            Package_Inst.append(pack_name[15])
##############################################################################
# glibc-devel   
        a= check(16,"rpm -q glibc-devel|sed -n 1p | cut -d- -f3,3,4|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[16])
        elif a=="not installed":
            Package_Notinst.append(pack_name[16])
        else:
            Package_Inst.append(pack_name[16])
##############################################################################
# ksh  
        a= check(17," rpm -q ksh |sed -n 1p| cut -d- -f3,2|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[17])
        elif a=="not installed":
            Package_Notinst.append(pack_name[17])
        else:
            Package_Inst.append(pack_name[17])
##############################################################################
# libstdc++-devel   
        a= check(18," rpm -q libstdc++-devel |sed -n 1p |cut -d- -f3,3,4|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[18])
        elif a=="not installed":
            Package_Notinst.append(pack_name[18])
        else:
            Package_Inst.append(pack_name[18])
##############################################################################
# libaio-devel   
        a= check(19,"rpm -q libaio-devel |sed -n 1p |cut -d- -f3,3,4|sed 's/.el6.x86_64//'")
        #print a
        if a==False:
            Package_update.append(pack_name[19])
        elif a=="not installed":
            Package_Notinst.append(pack_name[19])
        else:
            Package_Inst.append(pack_name[19])
##############################################################################
        log.info('Script Execution is successfull, no checking the output')
        ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName, "No Error","Fetching the output", LogServer, LogDB, LogUser, LogPwd)
        if Package_Notinst==[]:
            if Package_update==[]:
                if Package_Inst!=[]:
                    print "0"
                    print "ExitDesc: All given packages are installed"
                    log.info("ExitDesc: All given packages are installed")
                    ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"No Error", "All given packages are installed", LogServer, LogDB, LogUser, LogPwd)
            else:
                print "10"
                print "ExitDesc: Given packages need to Upgrade"
                print ",".join(Package_update)
                log.info('ExitDesc: Given packages need to Upgrade{0}'.format(Package_update))
                #HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Some Packages Needs to Upgrade",LogServer,LogDB,LogUser,LogPwd)
                ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"No Error", "Some packages need to Upgrade", LogServer, LogDB, LogUser, LogPwd)
        else:
            if Package_update==[]:
                print "10"
                print "ExitDesc: Check given packeages which are not installed"
                print ",".join(Package_Notinst)
                log.info('ExitDesc: Check given packeages which are not installed{0}'.format(Package_Notinst))
                #HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Some Packages Needs to Install",LogServer,LogDB,LogUser,LogPwd)
                ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"No Error", "Some packages need to Install", LogServer, LogDB, LogUser, LogPwd)
            else:
                print "10"
                print "ExitDesc: Some Packages need to install and some need to upgrade"

                p= ",".join(Package_Notinst+Package_update)
                print p
                log.info("ExitDesc: Some Packages need to install and some need to upgrade")
                #HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Some Packages Needs to Upgrade",LogServer,LogDB,LogUser,LogPwd)
                ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"No Error", "Some packages need to Install", LogServer, LogDB, LogUser, LogPwd)
    else:
        print "10"
        print "ExitDesc: Missing Argument"
        log.info("ExitDesc: Missing Argument")
        HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Package Check Script Failed because of Missing Arguments",LogServer,LogDB,LogUser,LogPwd)
        ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "No Error","Missing Argument", LogServer, LogDB, LogUser, LogPwd)
        
except Exception, e:
    log.info('Error: {0}'.format(str(e)))
    s.close()
    print "1"
    print "ExitDesc: {0}".format(str(e))
    HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Package Check Script Failed",LogServer,LogDB,LogUser,LogPwd)
    ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error", str(e),LogServer, LogDB, LogUser, LogPwd)

finally:
    s.close()
