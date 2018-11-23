#!/bin/bash

if [ $(id -u) != "0" ];then
	echo "ERROR,You must use root to run^_^"
	exit 1
fi
dqwz=$(dirname `readlink -f $0`)
echo "Install CySSHClient Begin"
if [ ! -d "/usr/local/CySSHClient" ]
then
	\cp -r ${dqwz}/CySSHClient /usr/local/
	chmod +x /usr/local/CySSHClient/CySSHClient.py
	echo "cp ${dqwz}/CySSHClient /usr/local/"
else
	echo "the CySSHClient already exists"
	echo "cp -rf ${dqwz}/CySSHClient/CySSHClient.py /usr/local/CySSHClient/"
	\cp -rf ${dqwz}/CySSHClient/CySSHClient.py /usr/local/CySSHClient/
	echo "The /usr/local/CySSHClient/cyssh.db no update!"
fi

ln -sf /usr/local/CySSHClient/CySSHClient.py /usr/bin/cyssh
echo "install CySSHClient success!"
echo "you can use command 'CySSH' or use command 'CySSH -h' show help"
