#!/bin/bash
#
# Boost.Python setup script for Travis CI
#
# Prereq:
#     These environment variables should be set.
#
#     TRAVIS_PYTHON_VERSION    e.g. 3.4 
#     BOOST_VERSION            e.g. 1.57.0
#

readonly py_cmd="python${TRAVIS_PYTHON_VERSION}"
readonly py_prefix=$(${py_cmd} -c 'from __future__ import print_function;import sys;print(sys.prefix)')
readonly py_include=$(${py_cmd} -c 'from __future__ import print_function;import distutils.sysconfig;print(distutils.sysconfig.get_python_inc(True))')

readonly tmp_dir=/tmp
readonly work_dir=${tmp_dir}/boost_${BOOST_VERSION//[.]/_}
readonly config_path=${work_dir}/user-config.jam

function download_source() {
    local local_path=${tmp_dir}/boost.tar.gz
    local url_prefix=http://sourceforge.net/projects/boost/files/boost
    local url=$url_prefix/${BOOST_VERSION}/boost_${BOOST_VERSION//[.]/_}.tar.gz/download
    wget -q -O $local_path $url || return 1
    tar xzf $local_path -C ${tmp_dir} || return 1
    return 0
}

function make_user_config() {
    {
        echo "using gcc : : ${CXX} ; "
        echo "using python"
        echo "  : ${TRAVIS_PYTHON_VERSION}"
        echo "  : ${py_cmd}"
        echo "  : ${py_include}"
        echo "  : ${py_prefix}/lib"
        echo "  ; "
    } > ${config_path}
    return $?
}

function run_bootstrap() {
    # see https://github.com/Homebrew/homebrew/blob/master/Library/Formula/boost-python.rb#L77-78
    sed -i 's/using python/#using python/g' ${work_dir}/bootstrap.sh || return 1
    (
        cd ${work_dir} && \
        ./bootstrap.sh --prefix=/usr --libdir=/usr/lib --with-libraries=python \
            --with-python=${py_cmd} --with-python-root=${py_prefix}
    )
    return $?
}

function run_b2() {
    (
        cd ${work_dir} && \
        ./b2 --build-dir=build-${py_cmd} --stagedir=stage-${py_cmd} python=${TRAVIS_PYTHON_VERSION} \
            --prefix=/usr --libdir=/usr/lib -d2 -j2 --layout=tagged --user-config=${config_path} threading=single \
            link=shared address-model=32_64 architecture=x86 pch=off cxxflags='-std=c++11 -Wno-unused-local-typedefs'
    )
    return $?
}


download_source || exit 1
make_user_config || exit 1
run_bootstrap || exit 1
run_b2 || exit 1
exit 0

