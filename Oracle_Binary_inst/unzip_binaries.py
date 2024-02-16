from sys import path
import sys
from os import system, getcwd, path, makedirs
import os
if len(sys.argv) == 2:
	binaries_location=sys.argv[1]
def unzip_binary():
		####Check if the software files are already unzipped.######
		log.info("Check if the software files are already unzipped")
		cmd="ls -ltr %s"%(binaries_location)
		stdin, stdout, stderr = dssh.exec_command(cmd)
		log.info("The Command is %s"%(cmd))
		out=stdout.read()
		a=binaries_location.split('/')
		if (a[-1] not in out):
			log.info(" trying to unzip!")
			cmd1="""unzip linuxamd64_12102_database_1of2.zip
			unzip linuxamd64_12102_database_2of2.zip"""
			stdin, stdout, stderr = dssh.exec_command(cmd1)
			log.info("The Command is %s"%(cmd1))
			out1=stdout.read()
			out2=stderr.read()
			if ('' in out2):
				print("unziped successfully")
				log.info("ExitDesc:unziped successfully")
			else:
				print("unziped unsuccessfully,check logs")
				log.info("ExitDesc:unziped unsuccessfully")
			
		else:
			print("software files are already unzipped")
			log.info("ExitDesc:software files are already unzipped")
 

		
		
		