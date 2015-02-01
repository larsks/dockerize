#!/bin/sh

# build an image with tar and the necessary tools to support
# most compresed archives
dockerize -t dockerizeme/tar \
	-e /bin/tar \
	/bin/tar /bin/xz /bin/bzip2 /bin/gzip

