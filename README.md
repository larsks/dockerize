# Dockerize

Dockerize will pack up your dynamically linked ELF binaries and all
their dependencies and turn them into a Docker image.

Some example images built with this tool are available from:

- https://hub.docker.com/u/dockerizeme/

## Synopsis

    usage: dockerize [-h] [--tag TAG] [--cmd CMD] [--entrypoint ENTRYPOINT]
                     [--no-build] [--output-dir OUTPUT_DIR] [--add-file SRC DST]
                     [--symlinks SYMLINKS] [--user USER] [--group GROUP]
                     [--filetools] [--verbose] [--debug] [--version]
                     ...

    positional arguments:
      paths

    optional arguments:
      -h, --help            show this help message and exit
      --add-file SRC DST, -a SRC DST
                            Add file <src> to image at <dst>
      --symlinks SYMLINKS, -L SYMLINKS
                            One of preserve, copy-unsafe, skip-unsafe, copy-all
      --user USER, -u USER  Add user to /etc/passwd in image
      --group GROUP, -g GROUP
                            Add group to /etc/group in image
      --filetools           Add common file manipulation tools
      --version             show program's version number and exit

    Docker options:
      --tag TAG, -t TAG     Tag to apply to Docker image
      --cmd CMD, -c CMD
      --entrypoint ENTRYPOINT, -e ENTRYPOINT

    Output options:
      --no-build, -n        Do not build Docker image
      --output-dir OUTPUT_DIR, -o OUTPUT_DIR

    Logging options:
      --verbose
      --debug

## A simple example

Create a `sed` image:

    dockerize -t sed /bin/sed

Use it:

    $ echo hello world | docker run -i sed s/world/jupiter
    hello jupiter

## A more complicated example

Create an image named `thttpd`:

    dockerize -t thttpd \
      -a /var/www/thttpd /var/www \
      --entrypoint '/usr/sbin/thttpd -D' \
      --cmd '-d /var/www' \
      /usr/sbin/thttpd

Serve default content:

    docker run thttpd

Serve your own content:

    docker run -v /my/content:/var/www thttpd

