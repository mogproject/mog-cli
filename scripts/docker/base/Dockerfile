FROM ubuntu:12.04

RUN apt-get -qq update
RUN apt-get -qq install software-properties-common python-software-properties
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test; fi
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get -qq update
RUN apt-get -qq install git vim wget gcc g++-4.8
RUN cd /var/tmp && git clone --depth=50 --branch=master git://github.com/mogproject/mog-cli.git mog-cli

