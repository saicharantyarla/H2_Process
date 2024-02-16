#!/usr/bin/env python
import os
from datetime import datetime

class CreateTable(object):
	def tableheader(header, separator):
		header=header.split("%s"% separator)
		length=len(header)
		tableheader="</TR>"
		for i in length:
			tableheader+="<TH>"+i+"</TH>"
		tableheader=tableheader+"</TR>"
		return tableheader
		
	def tablebody(output, separator):
		output=output.splitlines()
		count=0
		tablebody=""
		for i in output:
			i=i.split("%s",% separator)
			length=len(i)
			beginning="<tr style='background-color:white;'>"
			for i in length:
				
				if count=0:
					if i and not i.isspace():
						# the string is non-empty
						bodyE2 ="<td style='text-align:center;'> " + i + " </td>"
						count+=1
					else:
						# the string is empty
						i="NULL"
						bodyE2 ="<td style='text-align:center;'> " + i + " </td>"
						count+=1
				else:
					if i and not i.isspace():
						# the string is non-empty
						bodyE2+="<td style='text-align:center;'> " + i + " </td>"
					else:
						# the string is empty
						i="NULL"
						bodyE2 ="<td style='text-align:center;'> " + i + " </td>"
						
			end="</tr>"
			tablebody+=beginning+bodyE2+end
		return tablebody
	def tablecreation(tableheader,tablebody)
		table="<table>"+tableheader+tablebody+"</table>"
		
class HTML(object):
	def htmlheader(SUBJECT,Execution_Location,HostName,Sid,Status,table):
		now = datetime.now()
		dt = now.strftime("%A,%d-%B-%y")
		dt=str(dt)
		
		body ="""
		<html>
		<H2> Database Status for %s </H2>
		<style>
		  table, th, td {
			border: 2px solid cyan;
			}
		th, td {
			padding: 10px;
		}
		th {
			background-color:#f1f1c1;
		}
		body {
			margin-left: 5px;
			margin-top: 5px;
			margin-right: 0px;
			margin-bottom: 10px;
			table {
			border: thin solid #000000;
		}
		</style>

		<TABLE>
		<TR>
		<TH>  Execution Type  </TH>
		<TH>  Server Name  </TH>
		<TH>  SID or Database name  </TH>
		<TH>  Status  </TH>
		<TH>  %s  </TH>

		</TR>
		<TR>
		<TD>  %s  </TD>
		<TD>  %s  </TD>
		<TD>  %s  </TD>
		<TD>  %s  </TD>
		<TD>  %s  </TD>

		</TR> 
		</TABLE>	
		</BODY>
		</HTML>""" %(dt,SUBJECT,Execution_Location,HostName,Sid,Status,table)
			# Prepare actual message
			
		part1="""From: %s 
		To: %s 
		Subject: %s
		Content-Type: multipart/mixed;
		""" %(frommail, tomail, SUBJECT)

		part2 = """Content-Type: text/html
		%s
		""" %body

		log.info("the Html code is %s "%body)
		message = part1 + part2
		
class Mail():
	def sendmail(SMTPSERVER,Tomail,FromMail,message):
		if "," in Tomail:
			Tomail=Tomail.split(",")
			for i in Tomail:
				try:
					client = smtplib.SMTP(smtpserver)
					client.sendmail(FROM, TO, message)
					client.quit()
					print "Email sent"
					log.info('Email Sent')
					
				except Exception, e:
					print "Email sending failed due to: {0}".format(e)
					log.info('Email sending failed due to: {0}'.format(e))
		
		
		
	
		
		
		
	
	


	