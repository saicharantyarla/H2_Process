import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from smptconfig import smtpserver, frommail, tomail

def sendmail(SUBJECT,Execution_Location,HostName,Sid,Status,table):

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


	if "," in Tomail:
		Tomail=Tomail.split(",")
		j=""
		for i in Tomail:
			try:
				client = smtplib.SMTP(smtpserver)
				client.sendmail(FROM, i, message)
				client.quit()
				j=j+","+i
				log.info('Email Sent')
			
			except Exception, e:
				k=k+","+i
				log.info('Email sending failed due to: {0}'.format(e))
				
				
		if j:
			print "Email sent succefully to : %s"%j
		if k:		
			print "Email sending failed to : {0}".format(k)		