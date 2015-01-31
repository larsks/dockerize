#!/bin/sh

# This creates a minimal webserver using thttpd.

dockerize -t dockerizeme/thttpd \
	-a /var/www/thttpd /var/www \
	-e '/usr/sbin/thttpd -D' \
	-c '-d /var/www' \
	/usr/sbin/thttpd
