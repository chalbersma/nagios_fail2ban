# Install `nagios_fail2ban`

## Backup

* Stash the old stuff. (On Updates Only)

	```
	rm -r /tmp/nrpe-sysd.old
	cp -r /opt/nrpe-sysd /tmp/nrpe-sysd
	```

## Rollout

* Make the Install Dir

	```
	mkdir -p /opt/nrpe-sysd
	chown nagios:nagios /opt/nrpe-sysd
	```

* Get check from `ssysrepo1`

	```
	wget -O /tmp/nrpe-sysd.tgz "https://github.com/chalbersma/nrpe-sysd/archive/1.0.tar.gz"
	```

* Install Check

	```
	cd /opt/nrpe-sysd
	tar -xvzf /tmp/nrpe-sysd.tgz --strip 1
	chown -R nagios:nagios /opt/nrpe-sysd
	```

* Add the Following to you Command File (or add as a new File)

	```
	

## Testing

* Test the Script. Using `exampleservice` which should be changed to a logical service

	```
	su -c '/opt/nrpe-sysd/sysd_check.sh -s exampleservice 2>/dev/null' -s /bin/bash nagios
	```

* View the Nagios Interface and ensure the check is being processed as Expected.

## Rollback

### Just this Update

* Move the old code back

	```
	mv /tmp/nrpe-sysd.old /opt/nrpe-sysd
	```

* Manually rollback any check changes.

### Remove the Check in Total

* Remove the Check in Total

	```
	rm -r /opt/nrpe-sysd
	```

* Remove the NRPE Bits. Examle here is for the sample check we setup. There may be more elsewhere.

	```
	rm /etc/nrpe.d/sssd_check.cfg
	```
