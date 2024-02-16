import os.path
import logging as log

def check_1(filename):
	try:
	
		exists=os.path.isfile(filename)
		print (exists)
		if exists:
			print ("hii")
			log.basicConfig(filename=filename, format='%(lineno)s %(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filemode = 'a', level=log.INFO)
			log.info("This is here")
			return"success"
	except Exception as e:
#		print ("Unable to create Logfile {0}".format(filename))
		print ("the exception is %s"%e) 
		
def one():
	#print ("hii")
	return "Hii"