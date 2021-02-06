#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sqlite3
import sys
import os
import re
import string
import prettytable as ptb
import getpass
########################################################
##  Copyright © 红楼信息hlinfo.net All Rights Reserved
##  2018-05-21
##  Email:service@hlinfo.net
########################################################

########chk python version#####
if sys.version > '3':
    PY3V = True
else:
    PY3V = False
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
    except (ValueError,TypeError):
        print("ERROR: the '%s' is not number" % (num))
        return False
########## function : string2int ###############
def string2int(s):
    try:
            return int(s)
    except (ValueError,TypeError):
            print("ERROR: the '%s' is not number" % (s))
            sys.exit(0)
###########get console input ############
def cyinput(txt):
    if PY3V:
        try:
            return input(txt)
        except (KeyboardInterrupt,TypeError):
            echo("\nNo information was entered^_^")
    else:
        try:
            return raw_input(txt)
        except (KeyboardInterrupt,TypeError):
            echo("\nNo information was entered^_^")
####DB conn#######
dbpwd = sys.path[0]+'/cyssh.db'
#echo(dbpwd)
global conn
global db
try:
    conn = sqlite3.connect(dbpwd)
    db = conn.cursor()
except:
    echo("Error: open file %s failed, Permission denied" % (dbpwd))
    sys.exit(0)

######### check databases file is have writable ##########
def dbis_writable():
    if not os.access(dbpwd,os.W_OK):
        username = getpass.getuser()
        echo("Error: database files[%s] do not have writable permissions for current users[%s]" % (dbpwd,username))
        sys.exit(0)
####request console parameter################
argvlen=len(sys.argv)
#print(m)
#echo("arg1:","")
#echo(sys.argv[0])

if not PY3V:
    reload(sys)
    sys.setdefaultencoding('utf8')
########### function:pemkey_read4db###############
def pemkey_read4db(keyid):
    sql1="select privatekey,keyname from sshkeylist where id=%d" % (string2int(keyid))
    db.execute(sql1)
    res = db.fetchall()
    now_user = getpass.getuser()
    pvkdir=''
    if now_user == 'root':
        pvkdir='/root/.cyssh/'
    else:
        pvkdir='/home/%s/.cyssh/' % now_user

    if not os.path.exists(pvkdir):
        os.makedirs(pvkdir)
    #pvkpath="/tmp/hlinfosshpvkey-%s.pem" % now_user
    rsnamekey = {}
    for row in res:
        privatekey = row[0]
        keyname = row[1]
        #fi = open(pvkpath, "w+")
        pvkpath = pvkdir + keyname + keyid
        with open(pvkpath, 'w+') as fi:
            o = fi.write(privatekey)
        if not PY3V:
                o=1
        if o > 0:
            rsnamekey['keypath'] = pvkpath
            rsnamekey['keyname'] = keyname
            cmd_chmod="chmod 600 %s" % pvkpath
            os.system(cmd_chmod)
            return (True,pvkpath,keyname)
        else:
            return (False,"","")
########### function:pemkey_read4db  END ###############
########### function:pemkey_write2db ##################
def pemkey_write2db(keypath,pubKeypath):
    if not os.access(keypath,os.R_OK):
        echo("Warning: The file[%s] do not have readable permissions for current users" % keypath)
    filename = os.path.basename(keypath)
    with open(keypath, 'r+') as fo:
        privateData = fo.read(-1)
    if privateData.strip() == '':
        echo("error:%s content is null" % filename)
        sys.exit(0)
    pubdata=''
    if os.access(pubKeypath,os.R_OK):
        with open(pubKeypath, 'r+') as fo:
            pubdata = fo.read(-1)
        if pubdata.strip() == '':
            pubfilename = os.path.basename(pubKeypath)
            echo("error:%s.pub content is null,skip public Key save" % pubfilename)
            sys.exit(0)
    if len(pubdata) == 0:
        sql_addkey="insert into sshkeylist(keyname,privatekey) values ('%s','%s')" % (filename,privateData)
    else:
        sql_addkey = "insert into sshkeylist(keyname,privatekey,publickey) values ('%s','%s','%s')" % (filename, privateData,pubdata)
    try:
        db.execute(sql_addkey)
        lastrowid=db.lastrowid
        conn.commit()
        #echo("add host info success!")
        return lastrowid
    except:
        conn.rollback()
        #echo("add host info is failed!")
        return False
########### function:pemkey_write2db END ##################
#########Fun:checkIdentityFile  begin #########
def checkIdentityFile(kid):
    sql_delkcount = "select count(*) from sshkeylist where id=%d" % (string2int(kid))
    db.execute(sql_delkcount)
    keycount4hostdb = db.fetchall()[0]
    if keycount4hostdb > 0:
        return True
    else:
        return False
#########Fun:checkIdentityFile end #########
#########Fun:query sshkey list begin #########
def fun_query_sshkey_list():
    db.execute("select * from sshkeylist order by id")
    res = db.fetchall()
    #echo(len(res))
    keytb = ptb.PrettyTable()
    keytb.field_names = ["ID", "KeyName"]
    for row in res:
        kid = row[0]
        keyname = row[1]
        privatekey = row[2]
        keytb.add_row(["%s" % kid,"%s" % keyname])
    echo('\033[1;44;37m','')
    echo(keytb)
    echo('\033[0m','')
#########Fun:query sshkey list END#########
############ function : fun_sshkey_file_add begin#########
def fun_sshkey_file_add():
    try:
        thisUser = getpass.getuser()
        defaultPath="/home/%s/.ssh/id_rsa" % thisUser
        if thisUser == "root":
            defaultPath = "/root/.ssh/id_rsa"
        echo("默认密钥对[私钥]位于：%s" % defaultPath)
        echo("如果您的私钥不是默认路径或默认名字请输入实际的路径和名字。")
        keypath=cyinput("请输入ssh密钥对完整路径[包含证书文件名,如 ~/.ssh/id_rsa]:")
        if len(keypath) == 0:
            if not(os.path.isfile(keypath)):
                keypath=cyinput("请输入ssh密钥对私钥完整路径[包含证书文件名]:")
                keypath_TF=True
                while keypath_TF:
                    if os.path.isfile(keypath):
                        break
                    else:
                        keypath=cyinput("请输入正确的ssh密钥对私钥完整路径[包含证书文件名]:")
                        if os.path.isfile(keypath):
                            keypath_TF=False
                            break
        pubKeypath=""
        isdefPubPath = cyinput("请确认公钥路径是否和私钥路径一致[default:Y]?[Y/N]:")
        if len(isdefPubPath) == 0:
            isdefkeyok = 'y'
        isdefkeyok.lower()
        if isdefkeyok == 'y' or isdefkeyok == 'yes':
            pubKeypath = "%s.pub" % keypath
        else:
            pubKeypath = cyinput("请输入公钥证书完整路径[包含证书文件名,通常以.pub结尾,如 ~/.ssh/id_rsa.pub]:")
            if len(pubKeypath) == 0:
                if not (os.path.isfile(pubKeypath)):
                    pubKeypath = cyinput("请输入ssh密钥对公钥完整路径[包含证书文件名,通常以.pub结尾]:")
                    pubkeypath_TF = True
                    while pubkeypath_TF:
                        if os.path.isfile(pubKeypath):
                            break
                        else:
                            pubKeypath = cyinput("请输入正确的ssh密钥对公钥完整路径[包含证书文件名,通常以.pub结尾]:")
                            if os.path.isfile(pubKeypath):
                                pubkeypath_TF = False
                                break
        #######commit####
        rs_add=pemkey_write2db(keypath,pubKeypath)
        if rs_add:
            echo("add sshkey pem file successful")
        else:
            echo("add sshkey pem file failed,please try again")
        sys.exit(0)
    except:
        echo("发生异常：")
######### function : fun_sshkey_file_add END#########
#########Fun:checkHostExists begin #########
def checkHostExists(id):
    sql_delkcount = "select count(*) from sshhostlist where id=%d" % (string2int(id))
    db.execute(sql_delkcount)
    rscount4hostdb = db.fetchall()[0]
    if rscount4hostdb > 0:
        return True
    else:
        return False
#########Fun:checkHostExists end #########
#########Query list start #########
def fun_query_list():
    db.execute("select * from sshhostlist order by id")
    res = db.fetchall()
    #echo(len(res))
    htb = ptb.PrettyTable()
    htb.field_names = ["ID", "description","port","host","ssh identity_file"]
    for row in res:
        hid = row[0]
        host = row[1]
        username = row[2]
        hhport = row[3]
        iskey = row[4]
        keypathid = row[5]
        hostdesc = row[6]
        identity_file = ""
        is_identity_file = ""
        if iskey == 0:
            is_identity_file="NO"
            identity_file = ""
        else:
            rspkinfo=pemkey_read4db(keypathid)
            if not rspkinfo[0]:
                echo("make sshkey pem file failed,please try again")
                sys.exit(0)
            identity_file = rspkinfo[2]
            is_identity_file="YES"
        htb.add_row(["%d" % hid,"%s" % hostdesc,"%s" % hhport,"%s@%s" % (username,host),"%s" % identity_file])
        echo('\033[1;44;37m','')
        htb.align["description"] = "l"
    echo(htb)
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
        keypathid = row[5]
        hostdesc = row[6]
        if is_key == 0:
            echo('\033[35m','')
            echo("正在尝试登录 ID=%d【%s】 -p%s %s@%s"% (hid,hostdesc, hhport, username, host))
            echo('\033[0m','')
            echo("请稍后...")
            cmd_pwd="ssh -o PubkeyAuthentication=no -p%s %s@%s" % (hhport, username, host)
            os.system(cmd_pwd)
            sys.exit(0)
        else:
            rspkinfo=pemkey_read4db(keypathid)
            if not rspkinfo[0]:
                echo("make sshkey pem file failed,please try again")
                sys.exit(0)
            pk_path_local=rspkinfo[1]
            pk_path_name=rspkinfo[2]
            echo('\033[35m','')
            echo("正在尝试登录 ID=%d【%s】 -p%s %s@%s -i %s" % (hid,hostdesc, hhport, username, host, pk_path_name))
            echo('\033[0m','')
            echo("请稍后...")
            cmd_keypath="ssh -p%s %s@%s -i %s" % (hhport, username, host,pk_path_local)
            os.system(cmd_keypath)
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
    try:
        host=cyinput("please enter hostname(domain or IP):")
        username=cyinput("Please enter username[default:root]:")
        hport=cyinput("Please enter Port[default:22]:")
        hostdesc=cyinput("请输入主机描述:")
        iskeyok=cyinput("是否SSH密钥对登录[default:No]?[Y/N]:")
        iskey=0
        keypath=''
        if len(iskeyok) == 0:
            iskeyok='N'
        iskeyok.lower()
        isUserDefkey=0
        if iskeyok == 'y' or iskeyok== 'yes':
            iskey=1
            isdefkeyok=cyinput("是否使用已保存密钥对[default:Yes]?[Y/N]:")
            if len(isdefkeyok) == 0:
                isdefkeyok='y'
            isdefkeyok.lower()
            if isdefkeyok == 'y' or isdefkeyok== 'yes':
                isUserDefkey=1
                fun_query_sshkey_list()
                keypath=cyinput("请输入密钥对ID:")
                rskid_isnum=is_num_by_except(keypath)
                while not rskid_isnum:
                    keypath=cyinput("请输入正确的密钥对ID:")
                    rskid_isnum=is_num_by_except(keypath)
                    if rskid_isnum:
                        break;
            else:
                keypath=cyinput("请输入ssh密钥对完整路径[包含文件名]:")
        else:
            iskey=0
        while len(host)==0:
            host=cyinput("please enter hostname(domain or IP):")
        if len(username) == 0:
            username='root'
        if len(hport) == 0 :
            hport='22'
        if iskey == 1 and isUserDefkey == 0:
            if not(os.path.isfile(keypath)):
                keypath=cyinput("请输入ssh证书完整路径[包含证书文件名]:")
                keypath_TF=True
                while keypath_TF:
                    if os.path.isfile(keypath):
                        break
                    else:
                        keypath=cyinput("请输入正确的ssh证书完整路径[包含证书文件名]:")
                        if os.path.isfile(keypath):
                            keypath_TF=False
                            break
            pubKeypath = ""
            isdefPubPath = cyinput("请确认公钥路径是否和私钥路径一致[default:Y]?[Y/N]:")
            if len(isdefPubPath) == 0:
                isdefkeyok = 'y'
            isdefkeyok.lower()
            if isdefkeyok == 'y' or isdefkeyok == 'yes':
                pubKeypath = "%s.pub" % keypath
            else:
                pubKeypath = cyinput("请输入公钥证书完整路径[包含证书文件名,通常以.pub结尾,如 ~/.ssh/id_rsa.pub]:")
                if len(pubKeypath) == 0:
                    if not (os.path.isfile(pubKeypath)):
                        pubKeypath = cyinput("请输入ssh密钥对公钥完整路径[包含证书文件名,通常以.pub结尾]:")
                        pubkeypath_TF = True
                        while pubkeypath_TF:
                            if os.path.isfile(pubKeypath):
                                break
                            else:
                                pubKeypath = cyinput("请输入正确的ssh密钥对公钥完整路径[包含证书文件名,通常以.pub结尾]:")
                                if os.path.isfile(pubKeypath):
                                    pubkeypath_TF = False
                                    break
            rs_add=pemkey_write2db(keypath,pubKeypath)
            if rs_add:
                keypath=rs_add
            else:
                echo("add host info failed,please try again")
                sys.exit(0)
        #######commit####
        sql_add = "INSERT INTO sshhostlist(host,username, port, iskey, keypath,hostdesc) VALUES ('%s', '%s', '%s', %s, '%s', '%s' )" % (host, username, hport, iskey, keypath,hostdesc)
        #echo("sql_add:")
        #echo(sql_add)
        try:
            db.execute(sql_add)
            conn.commit()
            echo("add host info success!")
        except:
            conn.rollback()
            echo("add host info is failed!")
    except:
        echo("An abnormal program termination occurred^_^")
########### add one host info end###########
############ update one host info start###########
def update_hostinfo(hostid):
    sql1="select * from sshhostlist where id=%s" % (hostid)
    db.execute(sql1)
    res = db.fetchall()
    for row in res:
        ohid = row[0]
        ohost = row[1]
        ousername = row[2]
        ohhport = row[3]
        ois_key = row[4]
        okeypath = row[5]
        ohostdesc = row[6]
        echo("请输入需要修改的信息，不修改的项留空，直接回车^_^")
        host=cyinput("please enter if update hostname(domain or IP)[%s]:" % (ohost))
        username=cyinput("Please enter if update username[%s]:" % (ousername))
        hport=cyinput("Please enter if update Port[%s]:" % (ohhport))
        ois_key_txt=""
        if ois_key == 0:
            ois_key_txt="当前没有设置SSH证书，是否设置[default:No]?[Y/N]:"
        else:
            ois_key_txt="当前已经有SSH证书，是否重新设置[default:No]?[Y/N]:"
        iskeyok=cyinput("%s" % (ois_key_txt))
        iskey=0
        keypath=''
        if len(iskeyok) == 0:
            iskeyok='N'
        iskeyok.lower()
        isUserDefkey=0
        if iskeyok == 'y' or iskeyok== 'yes': ###重新设置
            iskey=1 #重新设置的标识
            isdefkeyok=cyinput("是否已保存证书[default:Yes]?[Y/N]:")
            isdefkeyok.lower()
            if isdefkeyok == 'y' or isdefkeyok== 'yes':
                isUserDefkey=1 #已保存证书的标识
                fun_query_sshkey_list()
                keypath_id=cyinput("请输入证书ID:")
                keypath = keypath_id
                rskid_isnum=is_num_by_except(keypath_id)
                while not rskid_isnum:
                    keypath_id=cyinput("请输入正确的证书ID:")
                    rskid_isnum=is_num_by_except(keypath_id)
                    if rskid_isnum:
                        keypath = keypath_id
                        break;
            else:
                keypath=cyinput("请输入ssh免密码登录密钥对私钥完整路径[包含文件名,通常为~/.ssh/id_rsa]:")
        else:
            iskey=0
        if len(host) == 0:
            host=ohost
        if len(username) == 0:
            username=ousername
        if len(hport) == 0 :
            hport=ohhport
        if iskey == 1:
            if isUserDefkey == 0:
                if not(os.path.isfile(keypath)):
                    keypath=cyinput("请输入ssh证书完整路径[包含证书文件名]:")
                    keypath_TF=True
                    while keypath_TF:
                        if os.path.isfile(keypath):
                            break
                        else:
                            keypath=cyinput("请输入正确的ssh证书完整路径[包含证书文件名]:")
                            if os.path.isfile(keypath):
                                keypath_TF=False
                                break

                pubKeypath = ""
                isdefPubPath = cyinput("请确认公钥路径是否和私钥路径一致[default:Y]?[Y/N]:")
                if len(isdefPubPath) == 0:
                    isdefkeyok = 'y'
                isdefkeyok.lower()
                if isdefkeyok == 'y' or isdefkeyok == 'yes':
                    pubKeypath = "%s.pub" % keypath
                else:
                    pubKeypath = cyinput("请输入公钥证书完整路径[包含证书文件名,通常以.pub结尾,如 ~/.ssh/id_rsa.pub]:")
                    if len(pubKeypath) == 0:
                        if not (os.path.isfile(pubKeypath)):
                            pubKeypath = cyinput("请输入ssh密钥对公钥完整路径[包含证书文件名,通常以.pub结尾]:")
                            pubkeypath_TF = True
                            while pubkeypath_TF:
                                if os.path.isfile(pubKeypath):
                                    break
                                else:
                                    pubKeypath = cyinput("请输入正确的ssh密钥对公钥完整路径[包含证书文件名,通常以.pub结尾]:")
                                    if os.path.isfile(pubKeypath):
                                        pubkeypath_TF = False
                                        break

                rs_add=pemkey_write2db(keypath,pubKeypath)
                if rs_add:
                    keypath=rs_add
                else:
                    echo("add host info failed,please try again")
                    sys.exit(0)
        else:
            keypath=okeypath
        hostdesc=cyinput("please enter if update Host description[%s]:" % (ohostdesc))
        if len(hostdesc) == 0 :
            hostdesc=ohostdesc
        #######commit####
        sql_update = "update sshhostlist set host='%s',username='%s', port='%s', iskey=%s, keypath='%s',hostdesc='%s' where id=%s" % (host, username, hport, iskey, keypath,hostdesc,hostid)
        try:
            db.execute(sql_update)
            conn.commit()
            echo("update host[ID=%s] info success!" % (hostid))
        except:
            conn.rollback()
            echo("update host[ID=%s] info is failed!" % (hostid))
########### update one host info end###########
########### fun delete host by id start########
def delhostbyid(hid):
    #判断是否为数字
    del_isnum=is_num_by_except(hid)
    if del_isnum:
        sql_del="delete from sshhostlist where id=%d" % (string2int(hid))
        #echo(sql_del)
        try:
            db.execute(sql_del)
            conn.commit()
            echo("delete host[ID=%s] success!"% (hid))
        except:
            conn.rollback()
            echo("delete host info is failed!")
    else:
        echo("ERROR：Please enter a number^_^")
########### fun delete host by id end########
########### fun delete sshkey by id start########
def delsshkeyfilebyid(kid):
    #判断是否为数字
    del_isnum=is_num_by_except(kid)
    if del_isnum:
        sql_delkcount="select count(*) from sshhostlist where keypath=%d" % (string2int(kid))
        db.execute(sql_delkcount)
        keycount4hostdb = db.fetchall()[0]
        if keycount4hostdb > 0 :
            echo("ERROR: The key already exist host list!")
            sys.exit(0)
        sql_delk="delete from sshkeylist where id=%d" % (string2int(kid))
        echo(sql_delk)
        try:
            db.execute(sql_delk)
            conn.commit()
            echo("delete sshkeyinfo[ID=%s] success!" % (kid))
        except:
            conn.rollback()
            echo("delete sshkey pem is failed!")
    else:
        echo("ERROR：Please enter a number^_^")
########### fun delete sshkey by id end########
########### function:syncPubKey2RemoteHost begin###############
def syncPubKey2RemoteHost(keyid,port,user,host):
    sql1="select publickey,keyname,privatekey from sshkeylist where id=%d" % (string2int(keyid))
    db.execute(sql1)
    res = db.fetchall()
    now_user = getpass.getuser()
    pvkdir=''
    if now_user == 'root':
        pvkdir='/root/.cyssh/'
    else:
        pvkdir='/home/%s/.cyssh/' % now_user
    if not os.path.exists(pvkdir):
        os.makedirs(pvkdir)
    #pvkpath="/tmp/hlinfosshpvkey-%s.pem" % now_user
    for row in res:
        publickey = row[0]
        keyname = row[1]
        privatekey = row[2]
        #fi = open(pvkpath, "w+")
        privatePath = pvkdir + keyname + keyid
        with open(privatePath, 'w+') as fi:
            o = fi.write(privatekey)
        pvkpath = pvkdir + keyname + keyid + ".pub"
        with open(pvkpath, 'w+') as fi:
            o = fi.write(publickey)
        if not PY3V:
            o=1
        if o > 0:
            os.system("chmod 600 %s" % privatePath)
            os.system("chmod 600 %s" % pvkpath)
            sshcopyid="/usr/bin/ssh-copy-id -i %s -p %s %s@%s" % (pvkpath,port,user,host)
            rsstatus = os.system(sshcopyid)
            return rsstatus
        else:
            return -1
########### function:syncPubKey2RemoteHost  END ###############
########### function:syncPubKeyQueryKey begin###############
def syncPubKeyQueryKey(hostid):
    sql = "select * from sshhostlist where id=%s" % (hostid)
    # db.execute('select * from sshhostlist where hid=%d',hostid)
    db.execute(sql)
    res = db.fetchall()
    for row in res:
        hid = row[0]
        host = row[1]
        username = row[2]
        hhport = row[3]
        is_key = row[4]
        keypathid = row[5]
        hostdesc = row[6]

        fun_query_sshkey_list()
        keypath_id = cyinput("请输入密钥对ID:")
        sshkeyid = keypath_id
        resultKey = checkIdentityFile(sshkeyid)
        while not resultKey:
            keypath_id = cyinput("请输入正确的密钥对ID:")
            resultKey = checkIdentityFile(keypath_id)
            if resultKey:
                sshkeyid = keypath_id
                break;
        rsok = syncPubKey2RemoteHost(sshkeyid,hhport,username,host)
        if rsok == 0:
            sql_update = "update sshhostlist set iskey=%s, keypath='%s' where id=%s" % (1, sshkeyid, hostid)
            try:
                db.execute(sql_update)
                conn.commit()
                echo("sync host[ID=%s] public identity_file success!" % (hostid))
            except:
                conn.rollback()
                echo("sync host[ID=%s] public identity_file failed!" % (hostid))
########### function:syncPubKeyQueryKey  END ###############
############### help start ##########################
def _help():
    echo("Usage: %s [Options]" % (sys.argv[0]))
    echo("Options:")
    echo("    -?,-h,-help,--help \t :this help")
    echo("    -add,add \t :add a host info")
    echo("    -d,del \t :del One host info By ID")
    echo("    -m \t :modify One host info By ID")
    echo("    -q \t :query All  host list")
    echo("    -k \t :query All ssh identity_file list")
    echo("    -ka \t :add identity_file info")
    echo("    -kd \t :delete identity_file info")
    echo("    -kr \t :sync public identity_file to remote host")
############### help end ##########################
def main():
    if argvlen==1:
        fun_query_list()
        inputid_queryone()
    else:
        for ii in range(1,argvlen):
            #echo("args:%s" % (sys.argv[ii]))
            if sys.argv[ii] == '-?' or sys.argv[ii] == '-h' or sys.argv[ii] == '-help' or sys.argv[ii] == '--help' :
                _help()
            elif sys.argv[ii] == '-add' or sys.argv[ii] == 'add':
                dbis_writable()
                add_hostinfo()
            elif sys.argv[ii] == '-d' or sys.argv[ii] == '-del' or sys.argv[ii] == 'del':
                fun_query_list()
                del_hostid=cyinput("请输入需要删除的主机ID号:")
                #######
                #判断是否为数字
                rsdel_isnum=checkHostExists(del_hostid)
                if rsdel_isnum:
                    dbis_writable()
                    delhostbyid(del_hostid)
                else:
                    echo("ERROR：Please enter a number^_^")
            elif sys.argv[ii] == '-m' or sys.argv[ii] == 'update' or sys.argv[ii] == 'modify':
                dbis_writable()
                fun_query_list()
                update_hostid=cyinput("请输入需要修改的主机ID号:")
                #######
                #判断是否为数字
                #rsup_isnum=is_num_by_except(update_hostid)
                rsup_isnum=checkHostExists(syncHostId)
                if rsup_isnum:
                    update_hostinfo(update_hostid)
                else:
                    echo("ERROR：Please enter real host ID^_^")
            elif sys.argv[ii] == '-q':
                fun_query_list()
            elif sys.argv[ii] == '-k':
                fun_query_sshkey_list()
            elif sys.argv[ii] == '-ka':
                dbis_writable()
                fun_sshkey_file_add()
            elif sys.argv[ii] == '-kd':
                dbis_writable()
                fun_query_sshkey_list()
                delKeyId=cyinput("请输入需要删除的密钥对ID号:")
                #######
                #判断是否为数字
                rsdel_isnum=checkIdentityFile(delKeyId)
                if rsdel_isnum:
                    #echo("输入是数字")
                    delsshkeyfilebyid(delKeyId)
                else:
                    echo("ERROR：Please enter a number^_^")
            elif sys.argv[ii] == '-kr':
                dbis_writable()
                fun_query_list()
                syncHostId = cyinput("请输入需要同步密钥的主机ID号:")
                rs = checkHostExists(syncHostId)
                if rs:
                    syncPubKeyQueryKey(syncHostId)
                else:
                    echo("ERROR：请输入正确的主机ID号^_^")
            elif is_num_by_except(sys.argv[ii]):
                rsIsHost = checkHostExists(sys.argv[ii])
                if rsIsHost:
                    fun_queryoneById(sys.argv[ii])
                else:
                    fun_query_list()
                    inputid_queryone()
            else:
                echo("you can usage: %s -h lookup the help" % (sys.argv[0]))
                fun_query_list()
                inputid_queryone()
#################
if __name__ == "__main__":
    main()

db.close()
conn.close()
