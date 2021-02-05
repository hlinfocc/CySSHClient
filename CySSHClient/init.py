#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sqlite3
import sys
import os
import re
import string
########################################################
##  Copyright © 红楼信息hlinfo.net All Rights Reserved
##  2018-11-29
##  Email:service@hlinfo.net
########################################################
####function echo() start######
def echo( param,*args ):
    if len(args)==0:
        print(param)
    else:
        for var in args:
            if var=='':
                print(param,end='')
            else:
                print(param)
####function echo() END#######

####DB conn#######
dbpwd = '/usr/local/CySSHClient/cyssh.db'
#dbpwd = sys.path[0]+'./cyssh.db'
global conn
global db
try:
	#echo(dbpwd)
	conn = sqlite3.connect(dbpwd)
	db = conn.cursor()
except:
	echo("Error: open file %s failed, Permission denied" % (dbpwd))
 	sys.exit(0)
def dbis_writable():
    if not os.access(dbpwd,os.W_OK):
        echo("Warning, database files[%s] do not have writable permissions for current users" % dbpwd)

def create_sshhostlist():
	try:
		create_tb_cmd='''
		CREATE TABLE IF NOT EXISTS "sshhostlist" (
		"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		"host"  TEXT,
		"username"  TEXT,
		"port"  TEXT,
		"iskey"  INTEGER,
		"keypath"  TEXT,
		"hostdesc"  TEXT
		);
		'''
		db.execute(create_tb_cmd)
  		conn.commit()
    		#echo("Create table sshhostlist OK")
  		return True
	except:
		#echo("Create table sshhostlist failed")
		return False
def create_sshkeylist():
	try:
		create_tb_cmd='''
		CREATE TABLE IF NOT EXISTS sshkeylist (
		id  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		keyname  TEXT,
		privatekey  TEXT,
		publickey TEXT
		);
		'''
		db.execute(create_tb_cmd)
  		conn.commit()
    		#echo("Create table sshkeylist OK")
  		return True
	except:
		#echo("Create table sshkeylist failed")
		return False
def chkField_isset():
	try:
		sql='''
		select sql from sqlite_master where type = 'table' and name = 'sshkeylist';
		'''
		db.execute(sql)
  		res = db.fetchall()
    		#echo(res[0][0])
      		#echo(res[0][0].find("publickey"))
        	pkstrisok = res[0][0].find("publickey")
        	if pkstrisok < 0 :
			db.execute("alter table sshkeylist add column publickey TEXT")
  			conn.commit()
     			return True
    		#echo("add column OK")
  		return True
	except:
		#echo("add column failed")
		return False

if __name__ == "__main__":
    	dbis_writable()
	a = create_sshhostlist()
	b = create_sshkeylist()
 	chkField_isset()
	if a and b:
		echo("CySSHClient: init databases successful")
  	else:
		echo("CySSHClient: init databases failed")

#################
db.close()
conn.close()
