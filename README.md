## A simple example

Create a `sed` image:

    dockerize -t sed /bin/sed

Use it:

    $ echo hello world | docker run -i sed s/world/jupiter
    hello jupiter

## A more complicated example

    dockerize -t webserver \
      -e /entrypoint.sh \
      /usr/sbin/thttpd \
      -s /var/www \
      -s entrypoint.sh /entrypoint.sh 0755

