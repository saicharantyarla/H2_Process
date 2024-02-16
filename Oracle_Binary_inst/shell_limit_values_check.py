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

dssh = paramiko.SSHClient()
dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
dssh.connect("10.76.64.138", username="oracle", password="oracle123")
#cmd="grep -E 'nproc|nofile|' /etc/security/limits.conf"
cmd="su - root"
dssh.invoke_shell()
stdin, stdout, stderr = dssh.exec_command(cmd)
stdin.write('oracle123')
stdin.flush()

stdin.write('whoami')
stdin.flush()
output = stdout.read()
print(output)
cmd1="whoami"
stdin, stdout, stderr = dssh.exec_command(cmd1)
output1=stdout.read()
print(output1)





out=stdout.read()
err=stderr.read()
print (out)
print("asfh")
print (err)

	