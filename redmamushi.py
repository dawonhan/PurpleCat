#!/usr/bin/env python3
#RUN: ./<FILENAME> os=<OS>
import sys
import subprocess
import os
ppos = sys.argv[1]

#ACTIONS TAKEN ON SYSTEM
REPORT_FIELD = ["ART TEST:", "DETECTION RESULT:", "LOG:"]
REPORT = []

os.system("touch REPORT.txt")
def authlog_readlines(num):
	#num = number of lines to read
	f = open("/var/log/auth.log", "r")
	list_f = f.readlines()
	lines = len(list_f) - num
	tail_lines = list_f[lines:]
	return tail_lines

def anylog_readlines(num, type):
	#num = number of lines to read
	#type = which log file in /var/log/
	f = open(f"/var/log/{type}", "r")
	list_f = f.readlines()
	lines = len(list_f) - num
	tail_lines = list_f[lines:]
	return tail_lines

def match_log(num, case_match):
	loglines = authlog_readlines(num)
#	print(loglines)
	result = "NONE"
	for line in loglines:
		if case_match in line:
			result = line
	return result

def match_anylog(num, case_match, logfile):
	loglines = anylog_readlines(num, logfile)
	print(loglines)
	result = "NONE"
	for line in loglines:
		if case_match in line:
			result = line
	return result

def create_account():
	user_add = "useradd -M -N -r -s /bin/bash -c evil_account joe_exotic"
	os.system(user_add)
	result = match_log(2, "useradd")
	REPORT.append(f"{REPORT_FIELD[0]} T1136\n{REPORT_FIELD[1]} {result}")
	os.system("userdel joe_exotic")

def create_account_root():
	user_add = "useradd -o -u 0 -g 0 -M -d /root -s /bin/bash carole_baskin"
	#user_pass = "echo 'ikilledmyhusband' | passwd --stdin carole_baskin"
	os.system(user_add)
	result = match_log(2, "name=carole_baskin, UID=0, GID=0")
	REPORT.append(f"{REPORT_FIELD[0]} T1136\n{REPORT_FIELD[1]} {result}")
	os.system("userdel -f carole_baskin > /dev/null 2>&1")

def set_uid_gid():
    set_uid = "sudo touch ./src/john_finlay"
    os.system(set_uid)

    change_own = "sudo chown root ./src/john_finlay"
    os.system(change_own)

    change_mod = "sudo chmod u+s ./src/john_finlay > /dev/null 2>&1" 
    os.system(change_mod)

    change_gid = "sudo chmod g+s ./src/john_finlay > /dev/null 2>&1"
    result = match_log(10, "COMMAND=/usr/bin/chmod u+s ./src/john_finlay")
    result_2 = match_log(10, "COMMAND=/usr/bin/chmod g+s ./src/john_finlay") 

    REPORT.append(f"{REPORT_FIELD[0]} T1166\n{REPORT_FIELD[1]} {result}")
    os.system("sudo rm ./src/john_finlay > /dev/null 2>&1")

def create_hidden_stuff():
    # T1158 - Hidden Files and Directories
    hidden_directory = "mkdir /var/tmp/.Bhagavan"
    hidden_file = 'echo "It’s not a job, it’s a lifestyle. -Bhagavan Doc Antle" > /var/tmp/.Bhagavan/.Doc_Antle'
    
    os.system(hidden_directory)    
    if os.path.exists('/var/tmp/.Bhagavan'):
        REPORT.append(f"{REPORT_FIELD[0]} T1158\n{REPORT_FIELD[1]} Hidden directory .Bhagavan was successfully created and detected\n")
    else:
        REPORT.append(f"{REPORT_FIELD[0]} T1158\n{REPORT_FIELD[1]} Hidden directory was not successfully created\n")
        
    os.system(hidden_file)
    if os.path.exists('/var/tmp/.Bhagavan/.Doc_Antle'):
        REPORT.append(f"{REPORT_FIELD[0]} T1158\n{REPORT_FIELD[1]} Hidden file .Doc_Antle was successfully created and detected\n")
    else:
        REPORT.append(f"{REPORT_FIELD[0]} T1158\n{REPORT_FIELD[1]} Hidden file .Doc_Antle was not successfully created\n")

    os.system('rm -rf /var/tmp/.Bhagavan/')

def issa_trap():
    #T1154 - Trap: Trap command allows programs and shells to specify commands that will be executed
    #upon receiving interrupt signals. 
    os.system("chmod +x ./src/trap.sh")
    run_trap = "./src/trap.sh"
    os.system(run_trap)
    result = match_log(5, "delete user") 
    REPORT.append(f"{REPORT_FIELD[0]} T1554 0 TRAP\n{REPORT_FIELD[1]} {result}") 

def t1215_test():
	os.system("cd ./src && sudo insmod t1215_test.ko")
	run_log = match_anylog(4, "Hello, K3r#3L", "kern.log")
	exit_log = match_anylog(2, "Goodbye, k3RnE1", "kern.log")
	REPORT.append(f"{REPORT_FIELD[0]} T1215:Kernel Modules and Extension\n{REPORT_FIELD[1]}\n{run_log}\n{exit_log}")
	os.system("sudo rmmod t1215_test")

if __name__ == "__main__":
	#ADD TEST FUNCTIONS HERE
	create_account()
	create_account_root()
	set_uid_gid()
	create_hidden_stuff()
	issa_trap()
	t1215_test()

	#PRINTING OUT THE RESULTS
	with open('REPORT.txt', 'w') as f:
		for item in REPORT:
			f.write(item+"\n")
