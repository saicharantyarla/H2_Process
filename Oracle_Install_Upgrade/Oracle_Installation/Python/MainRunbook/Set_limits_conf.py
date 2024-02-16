"""
	Name: Validating parameters in limits.conf file
	Description: Executed from HP OO, Estimate datafile size in oracle
	Team: Software Service Automation
	Inputs: Arguments [LogServer,LogDB,ORACLEServer,APID,LogAccountName,LogUser,LogPwd,ORACLEServer,ORACLESeUsername,ORACLESePassword], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
"""

# Modules Initializing #
import datetime
import sys
import socket
import cx_Oracle as dbc
import ActivityLogger
import HLStatus
import paramiko

OFol = "C:\Python_Logs\Oracle_Upgrade_Install\Oracle_Installation"
OFile = OFol + "\\" + 'Shelllimits.log'
# Variable Mapping #
ActivityName = "Validating parameters in limits.conf file"
Des = " Validating parameters in limits.conf file"
a = 0
s = socket.socket()

try:
	with open(OFile, 'w+') as of:
		print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Starting Script Execution"
		# Arguments Mapping #

		if len(sys.argv) == 10:
			##Log Variables##
			LogServer = sys.argv[1]
			LogDB = sys.argv[2]
			APID = sys.argv[3]
			LogAccountName = sys.argv[4]
			LogUser = sys.argv[5]
			LogPwd = sys.argv[6]

			##Script Variables##
			ORACLEServer = sys.argv[7]  # Target ORACLEServer
			ORACLESeUsername=sys.argv[8] #
			ORACLESePassword=sys.argv[9]
			#DbUser = sys.argv[10]  # Target Database user to connect to listener
			#ORACLEDBPassword = sys.argv[11]  # Target Database user password to connect to listener
			   
			CIServer = ORACLEServer
			address = ORACLEServer
			port = 22
			
			# Connectivity Test #
			HLStatus.UpdateHLStatus(APID,"Stepid96","In Progress","Oracle Limits.conf file Parameter set is In Progress",LogServer,LogDB,LogUser,LogPwd)
			ActivityLogger.InsertActivityLog(APID, CIServer, ActivityName, Des, "Initiated", LogAccountName, "No Error", "Connectivity check initiated", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ": Checking connectivity for", ORACLEServer

			s.connect((address, port))

			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "In Progress", LogAccountName,"No Error", "Host is reachable", LogServer, LogDB, LogUser, LogPwd)
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ":", ORACLEServer, "is reachable "
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Estimate datafile size "

			## Database Connection String ##
				
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(ORACLEServer, username=ORACLESeUsername, password=ORACLESePassword)
			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","SSH Connection succesfull to the host",LogServer,LogDB,LogUser,LogPwd)

			#log.info('Executing the command :{0}'.format(command))
			ActivityLogger.WriteActivityLog( APID,CIServer,ActivityName,Des,"In Progress",LogAccountName, "No Error","Validating the limits.conf file",LogServer,LogDB,LogUser,LogPwd)
			#print "hi"

			command1="grep -E 'oracle' /etc/security/limits.conf | grep soft | grep nproc | awk '{print $4}'"	
			stdin, stdout, stderr = dssh.exec_command(command1)
			output1 = stdout.read()
			errout = stderr.read()
			
			if not output1:
                                command1 = 'echo "oracle  soft    nproc   2047" >>  /etc/security/limits.conf'
                                stdin, stdout, stderr = dssh.exec_command(command1)
                                output1 = stdout.read()
                                errout = stderr.read()
                        else:  
                                output1=int(output1)
			#print output1
			#
			type(output1)
			if output1 != 2047:
				command2="grep -E 'oracle' /etc/security/limits.conf | grep soft | grep nproc | sed -i 's/'$(awk '{print $4}')'/2047/' /etc/security/limits.conf"
				stdin, stdout, stderr = dssh.exec_command(command2)
				output2 = stdout.read()
				errout = stderr.read()
				#print "oracle soft nproc value has been changed"

			command3="grep -E 'oracle' /etc/security/limits.conf | grep hard | grep nproc | awk '{print $4}'"
			stdin, stdout, stderr = dssh.exec_command(command3)
			output3 = stdout.read()
			
			if not output3:
                                command3 = 'echo "oracle  hard    nproc   16384" >>  /etc/security/limits.conf'
                                stdin, stdout, stderr = dssh.exec_command(command3)
                                output3 = stdout.read()
                                errout = stderr.read()
                        else:  
                                output3=int(output3)
			errout = stderr.read()			
			#print output3
			if output3 != 16384:
				command4="grep -E 'oracle' /etc/security/limits.conf | grep hard | grep nproc | sed -i 's/'$(awk '{print $4}')'/16384/' /etc/security/limits.conf"
				stdin, stdout, stderr = dssh.exec_command(command4)
				output4 = stdout.read()
				errout = stderr.read()
				#print "oracle hard nproc value has been changed"
		
			command5="grep -E 'oracle' /etc/security/limits.conf | grep soft | grep nofile | awk '{print $4}'"
			stdin, stdout, stderr = dssh.exec_command(command5)
			output5 = stdout.read()
			if not output5:
                                command5 = 'echo "oracle  soft    nofile  1024" >>  /etc/security/limits.conf'
                                stdin, stdout, stderr = dssh.exec_command(command5)
                                output5 = stdout.read()
                                errout = stderr.read()
                        else:  
                                output5=int(output5)
			errout = stderr.read()			
			#print output5
			if output5 != 1024:
				command6="grep -E 'oracle' /etc/security/limits.conf | grep soft | grep nofile | sed -i 's/'$(awk '{print $4}')'/1024/' /etc/security/limits.conf"
				stdin, stdout, stderr = dssh.exec_command(command6)
				output6 = stdout.read()
				#output6 = int(output6)
				errout = stderr.read()
				#print "oracle soft nofile value has been changed"

			command7="grep -E 'oracle' /etc/security/limits.conf | grep hard | grep nofile | awk '{print $4}'"
			stdin, stdout, stderr = dssh.exec_command(command7)
			output7 = stdout.read()
			if not output7:
                                command7 = 'echo "oracle  hard    nofile  65536" >>  /etc/security/limits.conf'
                                stdin, stdout, stderr = dssh.exec_command(command7)
                                output7 = stdout.read()
                                errout = stderr.read()
                        else:  
                                output7=int(output7)
			errout = stderr.read()			
			#print output7
			if output7 != 65536:
				command8="grep -E 'oracle' /etc/security/limits.conf | grep hard | grep nofile | sed -i 's/'$(awk '{print $4}')'/65536/' /etc/security/limits.conf"
				stdin, stdout, stderr = dssh.exec_command(command8)
				output8 = stdout.read()
				#output8 = int(output8)
				errout = stderr.read()
				#print "oracle hard nofile value has been changed"

			command9="grep -E 'oracle' /etc/security/limits.conf | grep soft | grep stack | awk '{print $4}'"
			stdin, stdout, stderr = dssh.exec_command(command9)
			output9 = stdout.read()
			if not output9:
                                command9 = 'echo "oracle  soft    stack   10240" >>  /etc/security/limits.conf'
                                stdin, stdout, stderr = dssh.exec_command(command9)
                                output9 = stdout.read()
                                errout = stderr.read()
                        else:  
                                output9=int(output9)
			errout = stderr.read()			
			#print output9
			if output9 != 10240:
				command10="grep -E 'oracle' /etc/security/limits.conf | grep soft | grep stack | sed -i 's/'$(awk '{print $4}')'/10240/' /etc/security/limits.conf"
				stdin, stdout, stderr = dssh.exec_command(command10)
				output10 = stdout.read()
				#output10 = int(output10)
				errout = stderr.read()
			#print "oracle soft stack value has been changed"
		
			command11="grep -E 'oracle' /etc/security/limits.conf | grep hard | grep stack | awk '{print $4}'"
			stdin, stdout, stderr = dssh.exec_command(command11)
			output11 = stdout.read()
			if not output11:
                                command11 = 'echo "oracle  hard    stack   10240" >>  /etc/security/limits.conf'
                                stdin, stdout, stderr = dssh.exec_command(command11)
                                output11 = stdout.read()
                                errout = stderr.read()
                        else:  
                                output11=int(output11)
			errout = stderr.read()			
			#print output11
			if output11 != 10240:
				command12="grep -E 'oracle' /etc/security/limits.conf | grep hard | grep stack | sed -i 's/'$(awk '{print $4}')'/10240/' /etc/security/limits.conf"
				stdin, stdout, stderr = dssh.exec_command(command12)
				output12 = stdout.read()
				#output12 = int(output12)
				errout = stderr.read()
				#print output12
				#print "oracle hard stack value has been changed"


			op = "The file limits.conf has successfuly checked and modified"
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%s" % (op)
			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"No Error", op, LogServer, LogDB, LogUser, LogPwd)
			
			#HLStatus.UpdateHLStatus(APID,"Stepid26","Completed","Validating limits.conf file completed successfully.")
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 0 \n"
			print "0"
			print "ExitDesc: %s" % (op)
              
		else:
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 10"
			print >> of, "[info]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Missing Arguments"
			ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName,"Error", op, LogServer, LogDB, LogUser, LogPwd)
			HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Limits.conf script failed Missing Argument",LogServer,LogDB,LogUser,LogPwd)
			print "10"
			print "ExitDesc: Missing Arguments" 
except socket.error:
	with open(OFile,'a') as of1:
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Limits.conf script failed Socket Error",LogServer,LogDB,LogUser,LogPwd)
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1"
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Connectivity to server %s failed" %address
        print "1"
        print "ExitDesc: Connectivity to server %s failed" %address

except:
	with open(OFile, 'a') as of1:
		ActivityLogger.WriteActivityLog(APID, CIServer, ActivityName, Des, "Completed", LogAccountName, "Error","Check the Log for error", LogServer, LogDB, LogUser, LogPwd)
		# HLStatus.UpdateHLStatus(APID,"Stepid26","Failed","Validating limits.conf file failed.")
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitCode: 1"
		print >> of1, "[error]", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	print "1"
	print "ExitDesc: Script Failed due to ", sys.exc_info()[1]
	HLStatus.UpdateHLStatus(APID,"Stepid96","Failed","Oracle Limits.conf script failed any Exception",LogServer,LogDB,LogUser,LogPwd)

finally:
	s.close()
	
