"""
	Name: Oracle_Unzip_Binary
	Description: Executed from HP OO, to unzip the binary
	Team: Software Service Automation
	Inputs: Arguments [HostName,UserName,Password,ZipPath]
	Output: ExitCode, ExitDesc(Log File)	
"""
# Modules Initializing #
import sys
import socket
import ActivityLogger
import paramiko
import logging as log
from os import system,getcwd,path,makedirs
import HLStatus
try:
    filename = "Oracle_Unzip_Binary.log"
    filepath = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
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
ActivityName = "Unzip Binary"
Des = "Unzip all the Binary files available in the folder."
s = socket.socket()
log.info('Input Variables mapping...')
if len(sys.argv) == 11:
    ##Log Variables##
    LogServer = sys.argv[1];
    LogDB = sys.argv[2];   
    APID = sys.argv[3];
    LogAccountName = sys.argv[4]
    LogUser = sys.argv[5]
    LogPassword = sys.argv[6]

    ##Script Variables##
    HostName = sys.argv[7] #HostName  	
    UserName = sys.argv[8] #UserName
    Password = sys.argv[9] #Password
    ZipPath = sys.argv[10] #ZipPath

    CIServer = HostName;
    address = HostName;
    port = 22
    #ProcessID, StepID, Status, Description,DBServerName,DbName,Username,Password
    HLStatus.UpdateHLStatus(APID,"Stepid96","In Progress","Binary Unziping is In Progress.",LogServer,LogDB,LogUser,LogPassword)
    ActivityLogger.InsertActivityLog( APID,CIServer,ActivityName,Des,"Initiated",LogAccountName, "No Error","Connectivity check initiated",LogServer,LogDB,LogUser,LogPassword)
    log.info('Checking connectivity to the host : {0}'.format(HostName))
    try:	
        s.connect((address, port)) 
        log.info('{0} host is reachable'.format(HostName))		
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Host is reachable",LogServer,LogDB,LogUser,LogPassword)
	
        ## Connection to the remote host ##	
        log.info('Trying to take remote session of Host : {0} with the credentials of : {1} '.format(HostName,UserName))					
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying SSH Connection to the host",LogServer,LogDB,LogUser,LogPassword)
		
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dssh.connect(HostName, username=UserName, password=Password)
        
        log.info('Succesfully connected  to the host {0} '.format(HostName))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesful to the host",LogServer,LogDB,LogUser,LogPassword)
        
        log.info('Executing the command...')
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Trying to execute commnd on remote host",LogServer,LogDB,LogUser,LogPassword)

        def execCommand(command):
            stdin, stdout, stderr = dssh.exec_command(command)
            output = stdout.read()
            errout = stderr.read()
            return output+"\n"+errout

        command1 = """DIRECTORY="""+ZipPath+"""
if [ -d "$DIRECTORY" ]; then
  echo "Yes"
else
  echo "No"
fi"""
        command2 = """cd """+ZipPath+"""
for i in `ls`; do unzip $i; done"""
        command3 = """cd """+ZipPath+"""
abc=$(echo `du -s database` | cut -d' ' -f1)
bcd=$(echo `du -s *1of2.zip` | cut -d' ' -f1)
def=$(echo `du -s *2of2.zip` | cut -d' ' -f1)
if [[ $abc -ge $(($bcd+$def)) ]];then echo "Yes"; else echo "No"; fi"""
        command4 = """cd """+ZipPath+"""
DIRECTORY=database
if [ -d "$DIRECTORY" ]; then
  echo "Yes"
else
  echo "No"
fi"""
        command5 = """cd """+ZipPath+"""
rm -rf database"""
        #print "Command1....."
        #print execCommand(command1)
        if execCommand(command1).strip() == "Yes":
            #print "Command2....."
            if execCommand(command4).strip() == "No":
                execCommand(command2)
                if execCommand(command3).strip() == "Yes":
                   #print "Command3....."
                    print "0"
                    print "ExitDesc: Unzipping is successful!"
                    log.info('Exitcode: 0')
                    log.info('ExitDesc: Unzipping is successful!')
                    ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Unzipping is successful!",LogServer,LogDB,LogUser,LogPassword)
                else:
                    print "10"
                    print "ExitDesc: Unzipping is failed!"
                    log.info('Exitcode: 10')
                    log.info('ExitDesc: Unzipping is failed!')
                    ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Unzipping is failed!",LogServer,LogDB,LogUser,LogPassword)
                    HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Binary Unziping is Failed.",LogServer,LogDB,LogUser,LogPassword)
            else:
                if execCommand(command3).strip() == "Yes":
                    print "0"
                    print "ExitDesc: Binaries are already unzipped!"
                    log.info('Exitcode: 0')
                    log.info('ExitDesc: Unzipped folder already exists!')
                    ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Binaries are already unzipped!",LogServer,LogDB,LogUser,LogPassword)
                else:
                    execCommand(command5)
                    execCommand(command2)
                    if execCommand(command3).strip() == "Yes":
                        #print "Command3....."
                        print "0"
                        print "ExitDesc: Binary Unzipping is successful!"
                        log.info('Exitcode: 0')
                        log.info('ExitDesc: Unzipping is successful!')
                        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Unzipping is successful!",LogServer,LogDB,LogUser,LogPassword)
                    else:
                        print "1"
                        print "ExitDesc: Unzipping is failed!"
                        log.info('Exitcode: 1')
                        log.info('ExitDesc: Unzipping is failed!')
                        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Unzipping is failed!",LogServer,LogDB,LogUser,LogPassword)
                        HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Binary Unziping is Failed.",LogServer,LogDB,LogUser,LogPassword)
        else:
            print "10"
            print "ExitDesc: Folder provoded doesnot exists!"
            log.info('Exitcode: 10')
            log.info('ExitDesc: Folder provoded doesnot exists!')
            ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"No Error","Folder provoded doesnot exists!",LogServer,LogDB,LogUser,LogPassword)
            HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Provided Binary location dosn't exist.",LogServer,LogDB,LogUser,LogPassword)
    except socket.error, e:
        print "10"
        print "ExitDesc: {10}".format(e)
        log.info('Exitcode: 10')
        log.info('ExitDesc: {10}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"Error",str(e),LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Socket error",LogServer,LogDB,LogUser,LogPassword)
    except Exception, e:
        print "1"
        print "ExitDesc: {1}".format(e)
        log.info('Exitcode: 1')
        log.info('ExitDesc: {1}'.format(e))
        ActivityLogger.WriteActivityLog(APID,CIServer,ActivityName,Des,"Completed",LogAccountName,"Error",str(e),LogServer,LogDB,LogUser,LogPassword)
        HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Binary Unzip Script failed because of some exceptions",LogServer,LogDB,LogUser,LogPassword)
    finally:
        s.close()
        dssh.close()
else:
    print "10"
    print "ExitDesc: Missing Arguments"
    log.info("Exitcode: 10")
    log.info("ExitDesc: Missing Arguments")
