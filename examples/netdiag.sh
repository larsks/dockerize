#!/bin/sh

# This builds an image containing the binaries from the iproute, iputils,
# and net-tools packages, along with a few other useful commands.

# tcpdump needs the "tcpdump" user to exist, hence
# the '-u tcpdump'
dockerize -t dockerizeme/netdiag \
	-u tcpdump \
	-a /bin/dash /bin/sh \
	-c /bin/sh \
	--filetools \
	/usr/sbin/tcpdump \
	/usr/bin/curl \
	/usr/sbin/arpd \
	/usr/sbin/bridge \
	/usr/sbin/cbq \
	/usr/sbin/ctstat \
	/usr/sbin/genl \
	/usr/sbin/ifcfg \
	/usr/sbin/ifstat \
	/usr/sbin/ip \
	/usr/sbin/lnstat \
	/usr/sbin/nstat \
	/usr/sbin/routef \
	/usr/sbin/routel \
	/usr/sbin/rtacct \
	/usr/sbin/rtmon \
	/usr/sbin/rtpr \
	/usr/sbin/rtstat \
	/usr/sbin/ss \
	/usr/sbin/tc \
	/usr/bin/ping \
	/usr/bin/ping6 \
	/usr/bin/tracepath \
	/usr/bin/tracepath6 \
	/usr/sbin/arping \
	/usr/sbin/clockdiff \
	/usr/sbin/ifenslave \
	/usr/sbin/ping6 \
	/usr/sbin/rdisc \
	/usr/sbin/tracepath \
	/usr/sbin/tracepath6 \
	/usr/bin/netstat \
	/usr/sbin/arp \
	/usr/sbin/ether-wake \
	/usr/sbin/ifconfig \
	/usr/sbin/ipmaddr \
	/usr/sbin/iptunnel \
	/usr/sbin/mii-diag \
	/usr/sbin/mii-tool \
	/usr/sbin/nameif \
	/usr/sbin/plipconfig \
	/usr/sbin/route \
	/usr/sbin/slattach \
	/usr/bin/host
