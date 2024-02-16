"""
	Name: ServerValidation Check
	Description: Executed from HP OO, Checks whether DB exists
	Team: Software Service Automation
	Inputs: Arguments Source and Targets Hostname
	Output: ExitCode, ExitDesc(Log File)
	
"""
# Modules Initializing #
import datetime
import sys
import socket
import openpyxl

OFol='C:\Python_Logs\ORACLE_Installation';
OFile=OFol + "\\" + 'ServerValidation.txt';
# Variable Mapping #
ActivityName = "Server Validation";
Des = "Checking whether Server exist in Inventory";


try:
	with open(OFile,'w+') as of:
		print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,": Starting Script Execution"
	# Arguments Mapping #
		if len(sys.argv) == 4 :
			
			##Script Variables##
			SHostname = sys.argv[1]
			InvenPath=sys.argv[2]
			SheetName=sys.argv[3]
			
			CIServer = SHostname
			wb=openpyxl.load_workbook(InvenPath)
			sheet = wb.get_sheet_by_name(SheetName)
			
			def excelmatch(hst_nm):
				res="Invalid"
				for row in sheet.iter_rows():
					for cell in row:
						if cell.internal_value == hst_nm:
							res= "Valid"
							break
				return res
			res1=excelmatch(SHostname)
			if res1 == "Valid":
				print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: %s exist in inventory" % (SHostname)
				print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 0 \n"
				print "0"
				print "ExitDesc: %s exist in inventory" % (SHostname)
			else:
				op="%s does not exist in inventory" % (SHostname)
				print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: %s does not exist in inventory" % (SHostname)
				print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1 \n"
				print "10"
				print "ExitDesc: %s does not exist in inventory" % (SHostname)
		
		else:
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1"
			print >>of,"[info]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Missing Arguments"
			print "10"
			print "ExitDesc: Missing Arguments"
except:
	with open(OFile,'a') as of1:
		
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitCode: 1"
		print >>of1,"[error]",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,"ExitDesc: Script Failed due to ",sys.exc_info()[1]
	print "1"
	print "ExitDesc: Script Failed due to ",sys.exc_info()[1]
