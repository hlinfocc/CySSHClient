#!/bin/bash

if [ $(id -u) != "0" ];then
	echo "ERROR,You must use root to run^_^"
	exit 1
fi
cp -r ./CySSHClient /usr/local/
chmod +x /usr/local/CySSHClient/CySSHClient.py
ln -s /usr/local/CySSHClient/CySSHClient.py /usr/bin/CySSH
echo "install success!"
echo "you can use command 'CySSH' or use command 'CySSH -h' show help"