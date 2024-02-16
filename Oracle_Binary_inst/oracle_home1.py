from sys import path
import sys
from os import system, getcwd, path, makedirs
import os

if len(sys.argv) == 3:
	oracle_home =sys.argv[1]
	input_path=sys.agrv[2]
	
	def Input_oracleHome():
		####Check oracle user has write permission on the ORACLE HOME######
		
		log.info("Check oracle user has write permission on the ORACLE HOME")
		partition_name=oracle_home.split('/')
		cmd="cd \/%s"%(partition_name[0])
		log.info("The Command is %s"%(cmd))
		stdin, stdout, stderr = dssh.exec_command(cmd)
		output = stderr.read()
		if "ERROR" not in output and "sp-" not in output:
			log.info("No error found, create a sample file")
			file_name=partition_name+'/'+'sample.txt'
			cmd1="touch %s"%(file_name)
			stdin, stdout, stderr = dssh.exec_command(cmd1)
			output1 = stderr.read()
			
			#####Check for available storage#########
			
			if "ERROR" not in output1 and "Permission denied" not in output1 and "sp-" not in output1:
				log.info("No error found, Check for available storage")
				cmd2="df –h \/{0}".format(partition_name)
				Hcmd = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(cmd2)
				stdin, stdout, stderr = dssh.exec_command(Hcmd)
				output2=stdout.read()
				out=output2.split()
				space=out[3].replace('G','')
					if (space > 8):
						
						##Create the directories in which oracle software is installed##
						
						if (os.path.exists(input_path)):
							print("path already exist")
						else:
							cmd3="mkdir -p %s"%(input_path)
							log.info("The Command is %s"%(cmd3))
						
					else:
						print("available is space is less than 8GB,File system has to be extended")
						log.info("ExitDesc:available is space is less than 8GB,File system has to be extended")
				
			else:
				print(" write permission denied on the oracle home")
				log.info("ExitDesc: write permission denied on the oracle home")
		else:
			print("This oracle user do not have the write permission on the oracle home")
			log.info("ExitDesc: This oracle user do not have the write permission on the oracle home")
			
			