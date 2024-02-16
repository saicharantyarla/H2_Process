"""
	Name: Creation of tablespace
	Description: Executed from Framework a script based solution, it will create tablespace
	Team: Software Service Automation
	Inputs: Arguments [Hostname,Osusername,Ospassword,Databasename]
	Output: ExitCode, ExitDesc(Log File)
"""

#!/usr/bin/env python
from sys import path
import sys
from Logger import Logger
import Logger as log
import time
import datetime
from os import system, getcwd, path, makedirs
import paramiko
import os

if len(sys.argv) == 6:
	Execution_Location=sys.argv[1]
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	
	################################### Creating Log File ###############################
	try:
			if os.name == 'nt':
					logdir = os.getcwd()+"\\logs"
			if os.name == 'posix':
					logdir = os.getcwd()+"/logs"

			logfile = "Create_Tablespace_%s.log"%HostName
			log = Logger(logdir,logfile)

			log.info('*************************************************************************')

			log.info('Started Script Execution')

	except Exception, e:
			print "ExitCode: 10"
			print "ExitDesc: Unable to create Logfile {0}".format(logfile)	
	
	
	try:
		def a():				
			Tbs_type=raw_input("""Please Enter option for the TablespaceType
				A:PERMANENT TYPE
				B:UNDO TYPE
				C:TEMPORARY TYPE
				D:Exit:""")
			Tbs_type=Tbs_type.upper()
			if len(Tbs_type) == 1 and Tbs_type.isalpha() == True:
				
				if "A" in Tbs_type or "B" in Tbs_type or "C" in Tbs_type:
					
					dict={'A' : "PERMANENT",
						  'B' : "UNDO" ,
						  'C' : "TEMPORARY" ,
						  'D' : "exit"}

					Tablespacetype=dict[Tbs_type]
					
					return Tablespacetype
				elif "D" in Tbs_type:
					print("User Terminated session")
					exit()
				else:
					print("enter proper input:")
					Tablespacetype=a()
					return Tablespacetype
			else:
				print("enter proper input:")
				Tablespacetype=a()
				return Tablespacetype	
		Tablespacetype=a()
		
		
		
		log.info("Trying to connect the target host %s"%HostName)
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(HostName, username=OSUser, password=OSPassword)
		log.info("The connection is successful")	
		loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
		def Spacecheck():
			command1="""set pages 200;
						select name from v\$datafile;"""
			ucommand1= "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			log.info("The Command is %s"%ucommand1)
			log.info("trying to execute the command")
			stdin, stdout, stderr = dssh.exec_command(ucommand1)
			output1 = stdout.read()
			log.info("The Output is %s "%output1)
			error=stderr.read()
			log.info("The error is %s"%error)	
			if "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
				output1=output1.strip()
				output1=output1.splitlines()
				b=""
				for i in output1:
					i=i.split("/")
					i[1]="/"+i[1]
					if i[1] not in b:
						b=b+i[1]+" "
				log.info("The partitions that are applicable are %s "%b)
				cmd="df -PhTm %s | sed -n '1!p'"%(b)
				stdin, stdout, stderr = dssh.exec_command(cmd)
				output2 = stdout.read()
				log.info("The command is %s"%(cmd))
				log.info("The Output is %s "%output2)
				output2=output2.splitlines()
				Used_inp=[]
				Part_name=[]
				for i in output2:
					i=i.split()
					if "Used" not in i and len(i)>=6 and len(i)!=1 :
						i2=float(i[2])
						i3=float(i[3])
						
						i4=((i3+500)/i2)*100
						Used_inp.append(i4)
						Part_name.append(i[6])
				dct = dict((a, b) for a, b in zip(Used_inp, Part_name))
				Used_space=min(Used_inp)
				partiton_name=dct[Used_space]
				m=[]
				y=(i3/i2)*100
				log.info("The current used space is %s"%y)
				#print(partiton_name)
				for c in output1:
					if partiton_name in c:
						#print (c)
						m.append(c)
				#print(m)		
				m=m[0].split("/")
				m=m[:-1]
				n=""
				c=[]
				#print(m)
				for i in m:
					i=i.strip()
					n=n+i+"/"
				log.info("The used space after adding 500m will be %s"%Used_space)
				log.info("The partiton_name is %s "%n)
				return Used_space,n
			else:
				log.info('Exitcode: 10')
				log.info("ExitDesc: Error occured ,Tablespace creation failed %s"%output2)
				exit()
		

				
		if Tablespacetype=="PERMANENT":
			log.info("Given type is 'PERMANENT'")
			Tablespacename=raw_input("Please enter the Tablespacename to create for PERMANENT type:")
			log.info("Checking tablespace is existing with the given name %s"%Tablespacename)
			command="select tablespace_name from dba_tablespaces where tablespace_name='%s';"%Tablespacename
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			log.info("The Command is %s"%ucommand)
			log.info("trying to execute the command")
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output = stdout.read()
			log.info("The Output is %s "%output)
			output=output.strip()
			error=stderr.read()
			log.info("The error is %s"%error)
			if "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
				if Tablespacename == output:
					log.info("ExitCode:10")
					log.info("ExitDesc:The tablespace name %s that you have provided already exists try another tablespacename"%Tablespacename)
					#print("ExitCode:10")
					print("FAILURE:The tablespace name %s that you have provided already exists try another tablespacename"%Tablespacename)
				else:
					log.info("tablespacename doesnot exists trying to create new tablespace")
					# Function call for further
					log.info("Performing space check on the file system")
					Used_inp1,partiton_name=Spacecheck()
					#print Used_inp1
					#print partiton_name
					if Used_inp1>80:
						flag=raw_input("After adding the tablespace to the partition then the partition size will be %s if you want to continue with the creation enter yes else no:  "%Used_inp)
						flag=flag.upper()
						if flag=="YES":
							log.info("The User entered YES trying to create Tablespace ")
							Datafilename="%s%s_01.dbf"%(partiton_name,Tablespacename)
							command2="create tablespace %s datafile '%s' size 500m autoextend on;"%(Tablespacename,Datafilename)
							ucommand2 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
							log.info("The Command is %s"%ucommand2)
							log.info("trying to execute the command")
							stdin, stdout, stderr = dssh.exec_command(ucommand2)
							output2 = stdout.read()
							log.info("The Output is %s "%output2)
							output2=output2.strip()
							error=stderr.read()
							log.info("The error is %s"%error)
							if "ERROR" not in output2 and "ORA-" not in output2 and "sp-" not in output2:
								log.info("Checking whether the Tablespace or not")
								log.info("The command is %s"%ucommand)
								stdin, stdout, stderr = dssh.exec_command(ucommand)
								output = stdout.read()
								log.info("The Output is %s "%output)
								output=output.strip()
								error=stderr.read()
								log.info("The error is %s"%error)
								if "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
									if Tablespacename == output:
										#print("ExitCode:0")
										print("SUCCESS: Tablespace %s of permanent Type Created successfully"%(Tablespacename,Datafilename))
										log.info("ExitCode:0")
										log.info("ExitDesc: Tablespace %s with Datafilename %s Permanent Type Created successfully"%(Tablespacename,Datafilename))
									else:
										#print("ExitCode:10")
										print("FAILURE:Error Occured Tablespace Creation Failed")
										log.info("ExitCode:10")
										log.info("ExitDesc:Error Occured Tablespace Creation Failed")
								else:
									#print("ExitCode:10")
									print("FAILURE:Error Occured Tablespace Creation Failed")
									log.info("ExitCode:10")
									log.info("ExitDesc:Error Occured Tablespace Creation Failed")
							
							#call a function
						else:
							print ("FAILURE:invalid input user terminated session")
							log.info("invalid input user terminated session")
							# exit from script
							exit()
						
					else:	
						Datafilename="%s%s_01.dbf"%(partiton_name,Tablespacename)
						command2="create tablespace %s datafile '%s' size 500m autoextend on;"%(Tablespacename,Datafilename)
						ucommand2 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
						#print(ucommand2)
						log.info("The Command is %s"%ucommand2)
						log.info("trying to execute the command")
						stdin, stdout, stderr = dssh.exec_command(ucommand2)
						output2 = stdout.read()
						log.info("The Output is %s "%output2)
						output2=output2.strip()
						error=stderr.read()
						log.info("The error is %s"%error)
						if "ERROR" not in output2 and "ORA-" not in output2 and "sp-" not in output2:
							log.info("Checking whether the Tablespace created or not ")
							log.info("The command is: %s"%ucommand)
							stdin, stdout, stderr = dssh.exec_command(ucommand)
							output = stdout.read()
							log.info("The Output is %s "%output)
							output=output.strip()
							error=stderr.read()
							log.info("The error is: %s"%error)
							if "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
								if Tablespacename == output:
									#print("ExitCode:0")
									print("SUCCESS: Tablespace %s with Datafilename %s of permanent Type Created successfully"%(Tablespacename,Datafilename))
									log.info("ExitCode:0")
									log.info("ExitDesc: Tablespace %s with Datafilename %s Permanent Type Created successfully"%(Tablespacename,Datafilename))
								else:
									#print("ExitCode:10")
									print("FAILURE:Error Occured Tablespace Creation Failed")
									log.info("ExitCode:10")
									log.info("ExitDesc:Error Occured Tablespace Creation Failed")						
							else:
								#print("ExitCode:10")
								print("FAILURE:Error Occured Tablespace Creation Failed")
								log.info("ExitCode:10")
								log.info("ExitDesc:Error Occured Tablespace Creation Failed")
						else:
							#print("ExitCode:10")
							print("FAILURE:Error Occured Tablespace Creation Failed")
							log.info("ExitCode:10")
							log.info("ExitDesc:Error Occured Tablespace Creation Failed")

			else:
				#print "ExitCode: 10"
				print "FAILURE: Error occured ,Tablespace creation failed %s"%output
				log.info('Exitcode: 10')
				log.info("ExitDesc: Error occured ,Tablespace creation failed %s"%output)
				
		elif Tablespacetype == "UNDO" or Tablespacetype == "TEMP" or Tablespacetype == "TEMPORARY":
		
			if Tablespacetype == "UNDO":
				log.info("Given type is 'UNDO'")
				command="select tablespace_name from dba_tablespaces where contents='UNDO';"
			elif Tablespacetype == "TEMP" or Tablespacetype == "TEMPORARY":
				log.info("Given type is 'TEMPORARY'")		
				command="select tablespace_name from dba_tablespaces where contents='TEMPORARY';"
			elif TablespaceType == "PERMANENT":
				exit()
			else:
				print("Enter the Proper type TEMPORARY/UNDO/PERMANENT")
				exit()
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			log.info("The Command is %s"%ucommand)
			log.info("trying to execute the command")
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output = stdout.read()
			log.info("The Output is %s "%output)
			if output and  "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
				output=output.strip()
				output=output.splitlines()
				count=len(output)+1
				if Tablespacetype == "UNDO":
					Tablespacename="UNDOTBS_%s"%(count)
				elif Tablespacetype == "TEMP" or Tablespacetype == "TEMPORARY":
					Tablespacename="TEMP_%s"%(count)
				else:
					print("Enter the Proper type TEMPORARY/UNDO/PERMANENT")
					exit()			
					
				log.info("The Tablespace name is %s"%Tablespacename)
				
				Used_inp1,partiton_name=Spacecheck()
				if Used_inp1>80:
					flag=raw_input("After adding the tablespace to the partition then the partition size will be %s if you want to continue with the creation enter yes else no:  "%Used_inp)
					flag=flag.upper()
					if flag=="YES":
						log.info("The User entered YES trying to create Tablespace ")
				
						command_chck="select tablespace_name from dba_tablespaces where tablespace_name='%s';"%Tablespacename
						ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command_chck)
						log.info("The Command is %s"%ucommand)
						log.info("trying to execute the command")
						stdin, stdout, stderr = dssh.exec_command(ucommand)
						output_chck = stdout.read()
						log.info("The Output is %s "%output_chck)
						output_chck=output_chck.strip()
						error=stderr.read()
						log.info("The error is %s"%error)					
						if "ERROR" not in output_chck and "ORA-" not in output_chck and "sp-" not in output_chck:
							if output_chck == Tablespacename:
								log.info("ExitCode:10")
								log.info("ExitDesc: The Tablespace %s already exists"%Tablespacename)
								#print "ExitCode:10"
								print "success: The Tablespace %s already exists"%Tablespacename
							else:
								log.info("The tablespace %s doesnot exists trying to create"%Tablespacename)
							
								if Tablespacetype== "UNDO":
									Datafilename="{0}{1}_01.dbf".format(partiton_name,Tablespacename)
									command3="Create undo tablespace %s datafile '%s' size 500m autoextend on;"%(Tablespacename,Datafilename)
								elif Tablespacetype == "TEMP" or Tablespacetype == "TEMPORARY":
									Datafilename="{0}{1}_01.dbf".format(partiton_name,Tablespacename)
									command3="Create temp tablespace %s tempfile '%s' size 500m autoextend on;"%(Tablespacename,Datafilename)
								else:
									print("Enter the proper Tablespace Type")
									exit()
								ucommand3="%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command3)
								log.info("The Command is %s"%ucommand3)
								log.info("trying to execute the command")
								stdin, stdout, stderr = dssh.exec_command(ucommand3)
								output3 = stdout.read()
								log.info("The Output is %s "%output3)
								if "ERROR" not in output3 and "ORA-" not in output3 and "sp-" not in output3:
									log.info("validating wether the Tablespace is created or not")
									log.info("The command is %s"%ucommand)
									stdin, stdout, stderr = dssh.exec_command(ucommand)
									output_chck = stdout.read()
									log.info("The Output is %s "%output_chck)
									output_chck=output_chck.strip()
									error=stderr.read()
									log.info("The error is %s"%error)					
									if "ERROR" not in output_chck and "ORA-" not in output_chck and "sp-" not in output_chck:
										if output_chck == Tablespacename:								
											#print("ExitCode:0")
											print("success: Tablespace %s with Datafilename %s  of %s Type Created successfully"%(Tablespacename,Datafilename,Tablespacetype))
											log.info("ExitCode:0")
											log.info("ExitDesc: Tablespace %s with Datafilename %s of %s Type Created successfully"%(Tablespacename,Datafilename,Tablespacetype))
										else:
											#print("ExitCode:1")
											print("FAILURE:Error Occured Tablespace Creation Failed")
											log.info("ExitCode:1")
											log.info("ExitDesc:Error Occured Tablespace Creation Failed")										
									else:
										#print("ExitCode:10")
										print("FAILURE:Error Occured Tablespace Creation Failed")
										log.info("ExitCode:10")
										log.info("ExitDesc:Error Occured Tablespace Creation Failed")								
											
								else:
									#print("ExitCode:10")
									print("FAILURE:Error Occured Tablespace Creation Failed")
									log.info("ExitCode:10")
									log.info("ExitDesc:Error Occured Tablespace Creation Failed")							
						else:
							#print("ExitCode:10")
							print("FAILURE:Error Occured Tablespace Creation Failed")
							log.info("ExitCode:10")
							log.info("ExitDesc:Error Occured Tablespace Creation Failed")
					else:
						#print "ExitCode:10"
						print "FAILURE:user terminated the session"
						log.info("ExitCode:10")
						log.info("ExitDesc:User terminated session")
						exit()
				else:
					log.info("The space is available in given partition trying to create Tablespace")
					command_chck="select tablespace_name from dba_tablespaces where tablespace_name='%s';"%Tablespacename
					ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command_chck)
					log.info("The Command is %s"%ucommand)
					log.info("trying to execute the command")
					stdin, stdout, stderr = dssh.exec_command(ucommand)
					output_chck = stdout.read()
					log.info("The Output is %s "%output_chck)
					output_chck=output_chck.strip()
					error=stderr.read()
					log.info("The error is %s"%error)					
					if "ERROR" not in output_chck and "ORA-" not in output_chck and "sp-" not in output_chck:
						if output_chck == Tablespacename:
							log.info("ExitCode:10")
							log.info("ExitDesc: The Tablespace %s already exists"%Tablespacename)
							print "ExitCode:10"
							print "FAILURE: The Tablespace %s already exists"%Tablespacename
						else:
							log.info("The tablespace %s doesnot exists trying to create"%Tablespacename)
						
							if Tablespacetype== "UNDO":
								Datafilename="{0}{1}_01.dbf".format(partiton_name,Tablespacename)
								command3="Create undo tablespace %s datafile '%s' size 500m autoextend on;"%(Tablespacename,Datafilename)
							elif Tablespacetype == "TEMP" or Tablespacetype == "TEMPORARY":
								
								Datafilename="{0}{1}_01.dbf".format(partiton_name,Tablespacename)
								command3="Create temp tablespace %s tempfile '%s' size 500m autoextend on;"%(Tablespacename,Datafilename)
							else:
								print("Enter the proper TablespaceType")
								exit()
							ucommand3="%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command3)
							log.info("The Command is %s"%ucommand3)
							log.info("trying to execute the command")
							stdin, stdout, stderr = dssh.exec_command(ucommand3)
							output3 = stdout.read()
							log.info("The Output is %s "%output3)
							if "ERROR" not in output3 and "ORA-" not in output3 and "sp-" not in output3:
								log.info("validating wether the Tablespace is created or not")
								log.info("The command is %s"%ucommand)
								stdin, stdout, stderr = dssh.exec_command(ucommand)
								output_chck = stdout.read()
								log.info("The Output is %s "%output_chck)
								output_chck=output_chck.strip()
								error=stderr.read()
								log.info("The error is %s"%error)					
								if "ERROR" not in output_chck and "ORA-" not in output_chck and "sp-" not in output_chck:
									if output_chck == Tablespacename:								
										print("ExitCode:0")
										print("ExitDesc: Tablespace %s with Datafilename %s  of %s Type Created successfully"%(Tablespacename,Datafilename,Tablespacetype))
										log.info("ExitCode:0")
										log.info("ExitDesc: Tablespace %s with Datafilename %s of %s Type Created successfully"%(Tablespacename,Datafilename,Tablespacetype))
									else:
										print("ExitCode:1")
										print("ExitDesc:Error Occured Tablespace Creation Failed")
										log.info("ExitCode:1")
										log.info("ExitDesc:Error Occured Tablespace Creation Failed")										
								else:
									print("ExitCode:10")
									print("ExitDesc:Error Occured Tablespace Creation Failed")
									log.info("ExitCode:10")
									log.info("ExitDesc:Error Occured Tablespace Creation Failed")								
										
							else:
								print("ExitCode:10")
								print("ExitDesc:Error Occured Tablespace Creation Failed")
								log.info("ExitCode:10")
								log.info("ExitDesc:Error Occured Tablespace Creation Failed")							
					else:
						print("ExitCode:10")
						print("ExitDesc:Error Occured Tablespace Creation Failed")
						log.info("ExitCode:10")
						log.info("ExitDesc:Error Occured Tablespace Creation Failed")			
			else:
				print("ExitCode:10")
				print("ExitDesc:Error Occured Tablespace Creation Failed")
				log.info("ExitCode:10")
				log.info("ExitDesc:Error Occured Tablespace Creation Failed")

		else:
			print ("ExitCode:10")
			print ("ExitDesc: Enter the proper Tablespace Type as  TEMPORARY/UNDO/PERMANENT")
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter the proper Tablespace Type as  TEMPORARY/UNDO/PERMANENT ")
			
	except Exception, e:
		Status="Failure. Check logs"
		print "ExitCode: 1"
		print "ExitDesc: script failed due to: {0}".format(e)
		log.info('ExitCode: 1')
		log.info('ExitDesc: script failed due to: {0}'.format(e))

else:
	print "Missing Arguments"