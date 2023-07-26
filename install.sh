#!/bin/bash

if [ $(id -u) != "0" ];then
  echo "ERROR,You must use root user to run^_^"
  exit 1
fi
_exists(){
  cmd="$1"
  if [ -z "$cmd" ] ; then
    echo "Usage: _exists cmd"
    return 1
  fi
  if type command >/dev/null 2>&1 ; then
    command -v $cmd >/dev/null 2>&1
  else
    type $cmd >/dev/null 2>&1
  fi
  ret="$?"
    return $ret
}
lang_num=0
Get_OS_Type()
{
  if grep -Eqi "CentOS" /etc/issue || grep -Eq "CentOS" /etc/*-release; then
    OSTYPE='CentOS'
    PM='yum'
  elif grep -Eqi "Red Hat Enterprise Linux Server" /etc/issue || grep -Eq "Red Hat Enterprise Linux Server" /etc/*-release; then
    OSTYPE='RHEL'
    PM='yum'
  elif grep -Eqi "Aliyun" /etc/issue || grep -Eq "Aliyun" /etc/*-release; then
    OSTYPE='Aliyun'
    PM='yum'
  elif grep -Eqi "Fedora" /etc/issue || grep -Eq "Fedora" /etc/*-release; then
    OSTYPE='Fedora'
    PM='yum'
  elif grep -Eqi "Debian" /etc/issue || grep -Eq "Debian" /etc/*-release; then
    OSTYPE='Debian'
    PM='apt'
  elif grep -Eqi "Ubuntu" /etc/issue || grep -Eq "Ubuntu" /etc/*-release; then
    OSTYPE='Ubuntu'
    PM='apt'
  elif grep -Eqi "Raspbian" /etc/issue || grep -Eq "Raspbian" /etc/*-release; then
    OSTYPE='Raspbian'
    PM='apt'
  else
    OSTYPE='unknow'
  fi
}
check_os_locale_lang()
{
  langarr=(
  en_US.UTF-8 UTF-8
  zh_CN.UTF-8 UTF-8
  zh_CN.GBK GBK
  zh_CN GB2312
  )
  langlenth=${langarr[@]}
  for (( i=0; i<$langlenth; i++ ))
  do
    if [ `grep -c "${langarr[$i]}" $1` -eq '0' ];then
      echo '${langarr[$i]}' >> $1
      lang_num=$[$lang_num+1]
    fi
  done
}
#################Check the system is supports Chinese begin ####################
Get_OS_Type
if [[ "$OSTYPE" -eq "CentOS" ]];then
  echo $OSTYPE
elif [[ "$OSTYPE" -eq "Debian" ]];then
  check_os_locale_lang /etc/locale.gen
elif [[ "$OSTYPE" -eq "Ubuntu" ]];then
  sudo apt-get install language-pack-zh-hans -y
  check_os_locale_lang /var/lib/locales/supported.d/local
fi
##################Check the system is supports Chinese end #####################
if [ command -v pip > /dev/null 2>&1 ]
then
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python get-pip.py
fi
if _exists pip3 ; then
  pip3 install prettytable
  pip3 install pysqlite3
  pip3 install argparse
fi
#if [ ! python -c "import PrettyTable" >/dev/null 2>&1 ]
#then
#  if _exists pip ; then
#    pip install prettytable
#  else
#    echo "请手动安装：pip install prettytable"
#  fi
#fi

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

python3 /usr/local/CySSHClient/init.py

ln -sf /usr/local/CySSHClient/CySSHClient.py /usr/bin/cyssh
echo "install CySSHClient successful!"
echo "you can use command 'cyssh' or use command 'cyssh -h' show help"

if [ "$lang_num" -gt "0" ];then
  echo "Warning, Installing Chinese Language Support Needs to Restart the Operating System!"
fi
