import os
import schedule
import time 
from datetime import datetime


TIME_LIMIT = 1


def get_list_files():
	upload_file_path = os.path.join(os.getcwd(),"tmp")
	if os.path.exists(upload_file_path):
		for (root,dirs,files) in os.walk(upload_file_path,topdown=True):
					return files

def remove_expiry_time(list_file):
	list_file = get_list_files()
	now = time.time() 
	print(f"Scaning expriry file at time now: {datetime.now()}")
	if not list_file:
		print("Nothing to remove!")
	else:	
		for file in list_file:
			path = os.path.join(os.getcwd(), "tmp",file)
			if os.path.exists(path):
				expiry_time = os.stat(path).st_ctime + (TIME_LIMIT* 60)
				if now >= expiry_time:
					os.remove(path)
					print(f"file {file} is expiry time this was deleted")

					
def scan_expiry_files():
	list_file = get_list_files()
	schedule.every(1).minutes.do(remove_expiry_time,list_file)
	while True:
		schedule.run_pending()

		

scan_expiry_files()