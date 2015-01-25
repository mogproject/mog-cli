Testing with Docker
====

- Build base image

```
docker build -t mogproject/ubuntu:base ./base
```

- Python 3.2

```
docker build -t mogproject/ubuntu:python3.2 ./python3.2
```

- Run

```
docker run -it mogproject/ubuntu:python3.2 bash
```

In the container...

```
cd /var/tmp/mog-cli
CC=gcc-4.8 CXX=g++-4.8 BOOST_VERSION=1.57.0 TRAVIS_PYTHON_VERSION=3.2 ./scripts/install_boost_python.sh

ln -s /tmp/boost_1_57_0/boost /usr/local/include/boost
ln -s /tmp/boost_1_57_0/stage-python3.2/lib/* /usr/local/lib/
ldconfig

CC=gcc-4.8 CXX=g++-4.8 python3.2 setup.py test
```
