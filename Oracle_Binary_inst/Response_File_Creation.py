from sys import path
import sys
import os

Response_file_content=['oracle.install.responseFileVersion=/oracle/install/rspfmt_dbinstall_response_schema_v12.1.0','ORACLE.INSTALL.OPTION = INSTALL_DB_SWONLY','UNIX_GROUP_NAME=oinstall','INVENTORY_LOCATION=/u02/app/oraInventory','SELECTED_LANGUAGES=en','ORACLE_HOME=/u02/app/oracle/product/12.1.0.2/db1','ORACLE_BASE=/u02/app/oracle','oracle.install.db.InstallEdition=EE','oracle.install.db.DBA_GROUP=dba','oracle.install.db.OPER_GROUP=dba','echo oracle.install.db.BACKUPDBA_GROUP=dba','oracle.install.db.DGDBA_GROUP=dba','oracle.install.db.KMDBA_GROUP=dba','DECLINE_SECURITY_UPDATES=true']

def create_response_file():
	log.info("Checking home directory of oracle user")
	command ="echo \$HOME" 
	ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
	stdin, stdout, stderr = dssh.exec_command(ucommand)
	output=stdout.read()
	log.info("command is :{0}".format(ucommand))
	log.info("output is : {1}".format(output))
	if('/home/oracle' in output):
		log.info("Trying to create Response file in oracle home directory - /home/oracle")
		command1="""echo oracle.install.responseFileVersion=/oracle/install/rspfmt_dbinstall_response_schema_v12.1.0 >> /home/oracle/db_install.rsp
		echo ORACLE.INSTALL.OPTION = INSTALL_DB_SWONLY >> /home/oracle/db_install.rsp
		echo UNIX_GROUP_NAME=oinstall >> /home/oracle/db_install.rsp
		echo INVENTORY_LOCATION=/u02/app/oraInventory >> /home/oracle/db_install.rsp
		echo SELECTED_LANGUAGES=en >> /home/oracle/db_install.rsp
		echo ORACLE_HOME=/u02/app/oracle/product/12.1.0.2/db1 >> /home/oracle/db_install.rsp
		echo ORACLE_BASE=/u02/app/oracle >> /home/oracle/db_install.rsp
		echo oracle.install.db.InstallEdition=EE >> /home/oracle/db_install.rsp
		echo oracle.install.db.DBA_GROUP=dba >> /home/oracle/db_install.rsp
		echo oracle.install.db.OPER_GROUP=dba >> /home/oracle/db_install.rsp
		echo oracle.install.db.BACKUPDBA_GROUP=dba >> /home/oracle/db_install.rsp
		echo oracle.install.db.DGDBA_GROUP=dba >> /home/oracle/db_install.rsp
		echo oracle.install.db.KMDBA_GROUP=dba >> /home/oracle/db_install.rsp
		echo DECLINE_SECURITY_UPDATES=true >> /home/oracle/db_install.rsp"""
		ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
		stdin, stdout, stderr = dssh.exec_command(ucommand)
		output1=stdout.read()
		er1= stderr.read()
		log.info("command is :{0}".format(ucommand))
		log.info("output is : {1}".format(output1))
		if er1 is None:
			log.info("Checking Response file content")
			file=open('/home/oracle/db_install.rsp','r+')
			file_content=file.readlines()
			log.info("Contents of Response file are : {0}".format(file_content))
			if ( len(file_content) == len(Response_file_content) ):
				print("Response file is created successfully")
				log.info("Response file is created successfully")
			else:
				print("Response file is not created successfully")
				log.info("Response file is not created successfully")
		else:
			print("The error if any is: %s" %er1)
			log.info("The error if any is: %s" %er1)
	else:
		print("/home/oracle is not the home directory of oracle user")
		log.info("/home/oracle is not the home directory of oracle user")
		
			