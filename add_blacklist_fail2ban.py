#!/usr/bin/env python3

# Checks Fail2Ban in a Nagios Compatible Manner
# 

import argparse
import subprocess
import sys
import time
import requests

if __name__ == "__main__" :



	parser = argparse.ArgumentParser()
	parser.add_argument("-V", "--verbose", action='store_true', help="Be Verbose (breaks Nagios)")
	parser.add_argument("-c", "--critical", help="Over this amount of banned ips is critical (default 50).")
	parser.add_argument("-w", "--warning", help="Over this amount of banned ips is a warning (default 35).")
	parser.add_argument("-m", "--max", help="Only add up to x ips (for performance) (default is 9999).")
	parser.add_argument("-t", "--timeout", help="Timout query to blacklist (default 5s).")
	parser.add_argument("-j", "--jail", help="Which jail to use (Required).", required=True)
	args = parser.parse_args()


	# Defaults & Constants
	CRIT=50
	WARN=35
	VERBOSE=False
	current_time=int(time.time())
	ten_min_ago=current_time - 600

	URL="https://api.blocklist.de/getlast.php?time="+str(ten_min_ago)

	try:
		# Given Global Variables
		if args.verbose :
			VERBOSE=True

		if args.critical :
			CRIT=int(args.critical)

		if args.warning :
			WARN=int(args.warning)

		if args.jail :
			jail=str(args.jail)

		if args.max :
			MAX=int(args.max)
		else :
			MAX=9999

		if args.timeout :
			TIMEOUT=int(args.timeout)
		else :
			TIMEOUT=5
			
		if VERBOSE:
			print("Current Settings. crit: ", CRIT, "warn:", WARN, "jail:", jail)
	except Exception as e :
		response="UNKNOWN: Error with values. Error " + str(e) + " | bannedips=0 "
		response_code=3
	else : 
		# Worked so Let's Try this stuff
		# Grab Banned IPs
		banned_ips_cmd="sudo fail2ban-client status " + jail + " | grep Banned | cut -f 2- -d : | tr ',' ' ' | xargs "
		banned_ips_string=subprocess.check_output([banned_ips_cmd], shell=True, universal_newlines=True).strip("\n")
		banned_ips_array=banned_ips_string.split(" ")
		banned_ips_count=len(banned_ips_array)
		
		perf_string="bans=" + str(banned_ips_count)

		# Get Ban List
		response=requests.get(URL, timeout=TIMEOUT)
		blacklist_ips_string=response.text
		blacklist_ips_array=blacklist_ips_string.split("\n")
		blacklist_actual=list(filter(None, blacklist_ips_array))
		blacklist_actual_count=len(blacklist_actual)

		perf_string=perf_string + ", blacklist_count=" + str(blacklist_actual_count)

		# Get Missing Blacklists
		ips_to_ban = [ ip for ip in blacklist_actual if ip not in banned_ips_array ]
		ips_to_ban_count=len(ips_to_ban)

		for badip in ips_to_ban[0:MAX] :
			if VERBOSE:
				print("Blocking IP : " , badip)
			this_ban_command="sudo fail2ban-client set " + jail + " banip " + badip 
			this_ban_output=subprocess.check_output([this_ban_command], shell=True, universal_newlines=True).strip("\n")
		
		perf_string=perf_string+", ips_to_ban=" + str(ips_to_ban_count)
		
	

		if ips_to_ban_count > CRIT :
			# Critical
			response="CRITICAL: Jail " + str(jail) + " Banned " + str(ips_to_ban_count) + " Potential banning issue. | " + perf_string
			response_code=2
		elif ips_to_ban_count > WARN :
			response="WARNING: Jail " + str(jail) + " Banned " + str(ips_to_ban_count) + " Potential banning issue. | " + perf_string
			response_code=1
		else :
			response="OK: Jail " + str(jail) + " Banned " + str(ips_to_ban_count) + " | " + perf_string
			response_code=0
		
		if VERBOSE:
			print("All Banned IPS", ips_to_ban)
			
	finally:
		print(response)
		sys.exit(response_code)
		
	
	
