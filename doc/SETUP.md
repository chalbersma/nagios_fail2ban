# Install `nagios_fail2ban`

## Backup

* Stash the old stuff. (On Updates Only)

	```
	rm -r /tmp/nagios_fail2ban
	cp -r /opt/nagios_fail2ban /tmp/nagios_fail2ban
	```

## Rollout

### From Release

* Make the Install Dir

	```
	mkdir -p /opt/nagios_fail2ban
	chown nagios:nagios /opt/nagios_fail2ban
	```

* Get check from `ssysrepo1`

	```
	wget -O /tmp/nrpe-sysd.tgz "https://github.com/chalbersma/nagios_fail2ban/archive/1.0.tar.gz"
	```

* Install Check

	```
	cd /opt/nagios_fail2ban
	tar -xvzf /tmp/nagios_fail2ban.tgz --strip 1
	chown -R nagios:nagios /opt/nagios_fail2ban
	```
### From Head

* Optionally you can follow head :

	```
	cd /opt/
	git clone https://github.com/chalbersma/nagios_fail2ban.git
	```
### Setup

* Add the Following to you Command File (or add as a new File) if you're using NRPE:

	```
	# nrpe.d nagios_fail2ban_jail
	command[fail2ban_jail_sshd]=/opt/nagios_fail2ban/check_fail2ban.py -j sshd
	```

* Add the following command to a local machine

	```
	# nagios_fail2ban.cfg
	define command{
		command_name	check_fail2ban_jail
		command_line	/opt/nagios_fail2ban/check_fail2ban.py -j $ARG1$ -c $ARG2$ -w $ARG3$
	}
	```

## Testing

* Test the Script. Using `exampleservice` which should be changed to a logical service

	```
	su -c '/opt/nagios_fail2ban/check_fail2ban.py -j myjail 2>/dev/null' -s /bin/bash nagios
	```

* View the Nagios Interface and ensure the check is being processed as Expected.

## Rollback

### Just this Update

* Move the old code back

	```
	mv /tmp/nagios_fail2ban.old /opt/nagios_fail2ban
	```

* Manually rollback any check changes.

### Remove the Check in Total

* Remove the Check in Total

	```
	rm -r /opt/nagios_fail2ban
	```

* Remove the NRPE Bits. Examle here is for the sample check we setup. There may be more elsewhere.

	```
	rm /etc/nrpe.d/nagios_fail2ban.cfg
	```
