#!/bin/sh

dockerize -t dockerizeme/jq /usr/bin/jq
dockerize -t dockerizeme/xmllint /usr/bin/xmllint
dockerize -t dockerizeme/xmltools \
	/usr/bin/xmllint \
	/usr/bin/xml2  \
	/usr/bin/2xml \
	/usr/bin/tidyp

