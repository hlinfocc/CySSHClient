#!/bin/bash

if [ $(id -u) != "0" ];then
	echo "ERROR,You must use root user to run^_^"
	exit 1
fi

if [ command -v pip > /dev/null 2>&1 ]
then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py

fi
if [ ! python -c "import PrettyTable" >/dev/null 2>&1 ]
then
	pip install PrettyTable
fi

dqwz=$(dirname `readlink -f $0`)
echo "Install CySSHClient Begin"
if [ ! -d "/usr/local/CySSHClient" ]
then
	\cp -r ${dqwz}/CySSHClient /usr/local/
	chmod +x /usr/local/CySSHClient/CySSHClient.py
	echo "cp ${dqwz}/CySSHClient /usr/local/"
else
	echo "the CySSHClient already exists, skip update your data"
	echo "cp -rf ${dqwz}/CySSHClient/CySSHClient.py /usr/local/CySSHClient/"
	\cp -rf ${dqwz}/CySSHClient/CySSHClient.py /usr/local/CySSHClient/
	\cp -rf ${dqwz}/CySSHClient/init.py /usr/local/CySSHClient/
fi

python /usr/local/CySSHClient/init.py

ln -sf /usr/local/CySSHClient/CySSHClient.py /usr/bin/cyssh
echo "install CySSHClient successful!"
echo "you can use command 'cyssh' or use command 'cyssh -h' show help"
