#!/bin/bash
# This script installs needed dependencies for PerEyevaSee to function.
pwd=$(pwd)
if [ [ $EUID -nq 0 ] ]
then
	echo "Run this script with root"
	exit 1
fi
git --version > /dev/null
if [ $? -ne 0 ]
then
apt-get install git
fi
easy_install --version > /dev/null
if [ $? -ne 0 ]
then
apt-get install python-setuptools
fi

mkdir temp
echo "Made temp dir that will be deleted after after this script is done"
cd temp
git clone git://github.com/gfxmonk/python-readability.git
cd python-readability
python setup.py install 
easy_install BeautifulSoup
easy_install html2text
easy_install stripogram
easy_install beautifulsoup4
rm -rf $pwd/temp
