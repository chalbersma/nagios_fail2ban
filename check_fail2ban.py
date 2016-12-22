#!/usr/bin/env python3

# Checks Fail2Ban in a Nagios Compatible Manner
# 

import argparse
import subprocess
import sys

if __name__ == "__main__" :

	parser = argparse.ArgumentParser()
	parser.add_argument("-V", "--verbose", action='store_true', help="Be Verbose (breaks Nagios)")
	parser.add_argument("-c", "--critical", help="Over this amount of banned ips is critical (default 50).")
	parser.add_argument("-w", "--warning", help="Over this amount of banned ips is a warning (default 35).")
	parser.add_argument("-j", "--jail", help="Which jail to use (Required).", required=True)

	args = parser.parse_args()

	# Defaults & Constants
	CRIT=50
	WARN=35
	VERBOSE=False

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
			
		if VERBOSE:
			print("Current Settings. crit: ", CRIT, "warn:", WARN, "jail:", jail)
	except Exception as e :
		response="UNKNOWN: Error with values. Error " + str(e) + " | bannedips=0 "
		response_code=3
	else : 
		# Worked so Let's Try this stuff
		# Grab Banned IPs
		banned_ips_cmd="sudo fail2ban-client status " + jail + " | grep Banned | cut -f 2 -d : | tr ',' ' ' | xargs "
		banned_ips_string=subprocess.check_output([banned_ips_cmd], shell=True, universal_newlines=True).strip("\n")
		banned_ips_array=banned_ips_string.split(" ")
		banned_ips_count=len(banned_ips_array)
		
		perf_string="bannedips=" + str(banned_ips_count)
	
		if banned_ips_count > CRIT :
			# Critical
			response="CRITICAL: Jail " + str(jail) + " Banned " + str(banned_ips_count) + " Potential banning issue. | " + perf_string
			response_code=2
		elif banned_ips_count > WARN :
			response="WARNING: Jail " + str(jail) + " Banned " + str(banned_ips_count) + " Potential banning issue. | " + perf_string
			response_code=1
		else :
			response="OK: Jail " + str(jail) + " Banned " + str(banned_ips_count) + " | " + perf_string
			response_code=0
		
		if VERBOSE:
			print("All Banned IPS", banned_ips_string)
			
	finally:
		print(response)
		sys.exit(response_code)
		
	
	
