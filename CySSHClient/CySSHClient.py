#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sqlite3
import sys
import os
import re
import string
########################################################
##  Copyright © 红楼信息hlinfo.net All Rights Reserved
##  2018-05-21
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
####function echo() end#######
########chk python version#####
if sys.version > '3':
	PY3V = True
else:
	PY3V = False
###########chk is number############
def is_num_by_except(num):
	try:
		'''if num.isdigit():
			#print("is num")
			return True
		else:
			#print("not num")
			return False '''
		int(num)
		return True
	except ValueError:
		print("ERROR: the '%s' is not number" % (num))
		return False
###########getconsole input ############
def cyinput(txt):
	if PY3V:
		return input(txt)
	else:
		return raw_input(txt)
####DB conn#######
dbpwd = sys.path[0]+'/cyssh.db'
#echo(dbpwd)
conn = sqlite3.connect(dbpwd)
db = conn.cursor()

####request console par################
argvlen=len(sys.argv)
#print(m)
#echo("arg1:","")
#echo(sys.argv[0])

if not PY3V:
	reload(sys)
	sys.setdefaultencoding('utf8')

#########Query list start #########
def fun_query_list():
	db.execute("select * from sshhostlist order by id")
	res = db.fetchall()
	#echo(len(res))
	for row in res:
		hid = row[0]
		host = row[1]
		username = row[2]
		hhport = row[3]
		iskey = row[4]
		keypath = row[5]
		hostdesc = row[6]
		#print("ID=%d. -p%s %s@%s,iskey=%d,keypath=%s"% (hid, hhport, username, host, iskey, keypath ))
		echo('\033[1;36;40m','')
		if iskey == 0:
			echo("ID=%d【%s】\t -p%s %s@%s"% (hid,hostdesc, hhport, username, host))
		else:
			echo("ID=%d【%s】\t -p%s %s@%s -i %s"% (hid,hostdesc, hhport, username, host, keypath))
		echo('\033[0m','')
#########Query list end #########
######### function query one by ID begin############
def fun_queryoneById(hostid):
	sql0="select * from sshhostlist where id=%s" % (hostid)
	#db.execute('select * from sshhostlist where hid=%d',hostid)
	db.execute(sql0)
	res = db.fetchall()
	for row in res:
		hid = row[0]
		host = row[1]
		username = row[2]
		hhport = row[3]
		is_key = row[4]
		keypath = row[5]
		hostdesc = row[6]
		if is_key == 0:
			echo("正在尝试登录 ID=%d【%s】\t -p%s %s@%s"% (hid,hostdesc, hhport, username, host))
			cmd_pwd="ssh -p%s %s@%s" % (hhport, username, host)
			os.system(cmd_pwd)
			sys.exit(0)
    	else:
			echo("正在尝试登录 ID=%d【%s】\t -p%s %s@%s -i %s"% (hid,hostdesc, hhport, username, host, keypath))
			cmd_keypath="ssh -p%s %s@%s -i %s" % (hhport, username, host,keypath)
			os.system(cmd_pwd)
			sys.exit(0)
######### function query one by ID END############
##############接收ID,查询一条数据###############
def inputid_queryone():
	inputhostid=cyinput("请输入需要登录的主机ID号:")
	#echo(inputhostid)
	#判断是否为数字
	rs_isnum=is_num_by_except(inputhostid)
	#echo(rs_isnum)
	if rs_isnum:
		#echo("输入是数字")
		fun_queryoneById(inputhostid)
	else:
		echo("ERROR：Please enter a number^_^")
	#print("输入的ID为：")
	#print(inputhostid)
########### input ID query one by id end########
############ add one host info start###########
def add_hostinfo():
	host=cyinput("please enter hostname(domain or IP):")
	username=cyinput("Please enter username[default:root]:")
	hport=cyinput("Please enter Port[default:22]:")
	iskeyok=cyinput("是否SSH证书登录[Y/N]:")
	hostdesc=cyinput("请输入主机描述:")
	iskey=0
	keypath=''
	if iskeyok == 'Y' or iskeyok == 'y' or iskeyok== 'yes':
		iskey=1
		keypath=cyinput("请输入ssh证书完整路径[包含证书文件名]:")
	else:
		iskey=0
	while len(host)==0:
		host=cyinput("please enter hostname(domain or IP):")
	if len(username) == 0:
		username='root'
	if len(hport) == 0 :
		hport='22'
	if iskey == 1:
		keypath=cyinput("请输入ssh证书完整路径[包含证书文件名]:")
		keypath_TF=True
		while keypath_TF:
			if os.path.isfile("keypath"):
				break
			else:
				keypath=cyinput("请输入正确的ssh证书完整路径[包含证书文件名]:")
				if os.path.isfile("keypath"):
					keypath_TF=False
					break
	#######commit####
	sql_add = "INSERT INTO sshhostlist(host,username, port, iskey, keypath,hostdesc) VALUES ('%s', '%s', '%s', %s, '%s', '%s' )" % (host, username, hport, iskey, keypath,hostdesc)
	echo("sql_add:")
	#echo(sql_add)
	try:
	   db.execute(sql_add)
	   conn.commit()
	   echo("add host info success!")
	except:
	   conn.rollback()
########### add one host info end###########
########### fun delete host by id start########
def delhostbyid(hid):
	#判断是否为数字
	del_isnum=is_num_by_except(hid)
	if del_isnum:
		sql_del="delete from sshhostlist where id=%s" % (hid)
		#echo(sql_del)
		try:
		   db.execute(sql_del)
		   conn.commit()
		   echo("delete host[ID=%d] success!"% (hid))
		except:
		   conn.rollback()
	else:
		echo("ERROR：Please enter a number^_^")
########### fun delete host by id end########
############### help start ##########################
def _help():
	echo("Usage: %s [Options]" % (sys.argv[0]))
	echo("Options:")
	echo("	-?,-h,-help \t :this help")
	echo("	-add,add \t :add a host info")
	echo("	-d,del \t :del a host info")
############### help end ##########################
if argvlen==1:
	fun_query_list()
	inputid_queryone()
else:
	for ii in range(1,argvlen):
		#echo("args:%s" % (sys.argv[ii]))
		if sys.argv[ii] == '-?' or sys.argv[ii] == '-h' or sys.argv[ii] == '-help' or sys.argv[ii] == '--help' :
			_help()
		elif sys.argv[ii] == '-add' or sys.argv[ii] == 'add':
			add_hostinfo()
		elif sys.argv[ii] == '-d' or sys.argv[ii] == 'del':
			fun_query_list()
			del_hostid=cyinput("请输入需要删除的主机ID号:")
			#######
			#判断是否为数字
			rsdel_isnum=is_num_by_except(del_hostid)
			if rsdel_isnum:
				#echo("输入是数字")
				delhostbyid(del_hostid)
			else:
				echo("ERROR：Please enter a number^_^")
		else:
			echo("Usage: %s -h" % (sys.argv[0]))
			fun_query_list()
			inputid_queryone()
#################
db.close()
conn.close()
