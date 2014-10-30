#!/bin/bash
cd `dirname $0`

VERSION=0.0.1
ITERATION=1

fpm -s dir -t rpm \
  -n ganglia-gmond-modules-python-plugins \
  -v "$VERSION" --iteration "$ITERATION" \
  -C ./ganglia-gmond-modules-python-plugins \
  -d ganglia-gmond-modules-python \
  --vendor 'liulantao@gmail.com' \
  --description 'Ganglia Python Plugins' \
  --url 'https://github.com/Lax' \
  --rpm-defattrfile 755 \
  --directories etc/ganglia/conf.d/ \
  --directories usr/lib64/ganglia/python_modules/ \
  ./
