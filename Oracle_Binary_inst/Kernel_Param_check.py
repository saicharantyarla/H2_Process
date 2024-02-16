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

from datetime import date
from datetime import datetime

try:
	exists=os.path.isfile(filename)
	print (exists)
	if exists:
		log.basicConfig(filename=filename, format='%(lineno)s %(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filemode = 'a', level=log.INFO)
		log.info("This is here")
		return"success"
except Exception as e:
	print ("the exception is %s"%e)
	
try:
	def rpm_package_availability(HostName,OSUser,OSPassword):
	
		log.info("Trying to connect the target host %s"%HostName)
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(HostName, username=OSUser, password=OSPassword)
		log.info("The connection is successful")	
		#loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid	
		cmd="rpm -q binutils glibc glibcc libstdc++ libaio libXext libXtst libX11 libXau libxcb libXi make sysstat compat-libcap1 compat-libstdc++-33 gcc gcc-c++ glibc-devel ksh libstdc++-devel libaio-devel"
		
		log.info("trying to execute the command")
		stdin, stdout, stderr = dssh.exec_command(cmd)
		log.info("The Command is %s"%cmd)
		output = stdout.read()
		log.info("The Output is %s "%output)
		error=stderr.read()
		z=output
		if error:
			log.info("The error is %s"%error)
			return "Failure"
		elif "sp-" not in z:
			z=z.splitlines()
			k=[]
			Package_Notinst=[]
			Package_32bit=[]
			for i in z:
				if not i.endswith("i686") and not i.endswith("not installed") and not i.startswith("#"):
					k.append(i)
				if i.endswith("not installed"):
					Package_Notinst.append(i)		
				if i.endswith("i686"):
					Package_32bit.append(i)
			package=["binutils-","glibc-","libstdc++-","libaio-","libXext-","libXtst-","libX11-","libXau-","libxcb-","libXi-","make-","sysstat-","compat-libcap1-","compat-libstdc++-","gcc-","gcc-c++-","glibc-devel-","ksh-","libstdc++-devel-","libaio-devel-"]
			package_version=['2.20.51.0.2.5.11','2.12.1.7','4.4.4.13','0.3.107.10','1.1','1.0.99.2','1.3','1.0.5','1.5','1.3','3.81.19','9.0.4.11','1.10.1','33.3.2.3.69','4.4.4.13','4.4.4.13','2.12.1.7','0','4.4.4.13','0.3.107.10']
			
			version=[]
			count=0
			if len(k)==len(package):
				print ("Lenghts are equal")
				for i,j in zip(package,k):
					j=j.split(i)
					version.append(j[1])
				if len(version)==len(package_version):
					for i,j in zip(version,package_version):
						i=''.join(e for e in i if e.isalnum())
						j=''.join(e for e in j if e.isalnum())
						print("the is value is %s and j value is %s"%(i,j))
						
						if isfloat(i)==True and isfloat(j)==True and i>=j:
							count+=1
				
				
				if count==len(package):
					print(" All given packages are installed")
					log.info("All given packages are installed")
					return "success"
			else:
				print("Insufficient packages")
				log.info("Insufficient packages")
				return "Failure"
			
			if Package_Notinst:
				print ("Check given packages which are not installed \n %s"%Package_Notinst)
				log.info("Check given packages which are not installed \n %s"%Package_Notinst)
				return "Failure"
			if Package_32bit:
				print("Given packages need to Upgrade \n %s "%Package_32bit)
				log.info("Given packages need to Upgrade \n %s "%Package_32bit)
				return "Failure"
		
		else:
			print("Exitcode:10")
			print("ExitDesc:Error Occured check output")
			log.info("Exitcode:10")
			log.info("Error Occured check output")
			return "Failure"
			
	def Kernel_Param_Check1(HostName,OSUser,OSPassword):
		log.info("Kernel Parameter check")
		log.info("Trying to connect the target host %s"%HostName)
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(HostName, username=OSUser, password=OSPassword)
		log.info("The connection is successful")	
		#loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid	
		cmd="grep -E 'net.ipv4.ip_local_port_range|net.core.rmem_default|net.core.rmem_max|net.core.wmem_default|net.core.wmem_max|kernel.shmmax| kernel.shmmni|kernel.sem|fs.file-max|fs.aio-max-nr|kernel.shmall' /etc/sysctl.conf"
		Ker_para=["net.ipv4.ip_local_port_range =","net.core.rmem_default =","net.core.rmem_max =","net.core.wmem_default =","net.core.wmem_max =","kernel.shmmax =","kernel.shmmni =","kernel.sem =","fs.file-max =","kernel.shmall =","fs.aio-max-nr ="]
		Param_values=["900065500","262144","4194304","262144","1048576","2147483648","4096","25032000100128","6815744","1048576","2097152"]
		
		
		log.info("trying to execute the command")
		stdin, stdout, stderr = dssh.exec_command(cmd)
		log.info("The Command is %s"%cmd)
		output = stdout.read()
		log.info("The Output is %s "%output)
		error=stderr.read()
		z=output
		if error:
			log.info("The error is %s"%error)
			print ("The error is %s"%error)
			return"Failure"
		elif "sp-" not in z:
			z=z.splitlines()
			k=[]
			values=[]
			count=0
			values_Na=[]
			for i in z:
				if not i.startswith("#"):
					k.append(i)
			if len(Ker_para)==len(k):
				for i,j in zip(Ker_para,k):
					j=j.split(i)
					values.append(j[1])
				if len(values)==len(Param_values):
					for i,j in zip(values,Param_values):
						i=i.strip()
						j=j.strip()
						if int(i)>=int(j):
							count=count+1
						else:
							values_Na.append(i)
				if count==len(Param_values):
					print("Param_values check successful")
					return "success"
			else:
				print("Insufficient Parameters")
				log.info("Insufficient Parameters")
				return "success"
				
			if values_Na:
				print("The parameters %s values are low"%values_Na)
				log.info("The parameters %s values are low"%values_Na)
				return "failure"
				
	def shell_limit_check(HostName,OSUser,OSPassword):
		log.info("checking the shell limits")
		log.info("Trying to connect the target host %s"%HostName)
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(HostName, username=OSUser, password=OSPassword)
		log.info("The connection is successful")	
		cmd="grep -E 'nproc|nofile|stack| /etc/security/limits.conf"
		log.info("The command is %s"%cmd)
		stdin, stdout, stderr = dssh.exec_command(cmd)
		log.info("The Command is %s"%cmd)
		output = stdout.read()
		log.info("The Output is %s "%output)
		error=stderr.read()
		if error:
			log.info("The error is %s"%error)
			print ("The error is %s"%error)
			return "Failure"
		elif "sp-" not in output:
			
		
		
			
except Exception as e:
	print ("the exception is %s"%e)
	exit()
			
					

