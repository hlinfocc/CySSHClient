# CySSHClient
基于Linux系统终端ssh命令的ssh客户端，方便在Linux系统使用ssh命令登录主机，不用记很多主机地址,直接一个命令就可以登录远程主机，省去输入主机地址的麻烦！
## 使用示例
1.	运行install.sh安装程序，安装完毕后的命令是cyssh（此命令可以在install.sh中修改）。
2.	了解参数运行`cyssh -h`，`cyssh -add`增加一条记录，`cyssh -d`删除一条记录
3.	运行cyssh 选择主机，输入密码即可登录，如果是免密码SSH证书可直接登录。  
显示帮助：
![cyssh help](https://hlinfocc.github.io/images/cyssh/cyssh-h.png)
查询：
![cyssh help](https://hlinfocc.github.io/images/cyssh/cyssh-q.png)
在终端直接输入cyssh命令，然后输入主机ID即可登录主机：
![cyssh help](https://hlinfocc.github.io/images/cyssh/cyssh-login.png)
增加SSH证书：
![cyssh help](https://hlinfocc.github.io/images/cyssh/cyssh-ka.png)
增加主机：
![cyssh help](https://hlinfocc.github.io/images/cyssh/cyssh-add1.png)
增加主机，使用SSH证书：
![cyssh help](https://hlinfocc.github.io/images/cyssh/cyssh-add2.png)

