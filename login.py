# -*- coding: UTF-8 -*-
__author__ = 'Hejing'

import jwxt
import glxt
import mail
import time
import time

#软件登录的界面设计
class GNYM():
    def __init__(self):
        #软件登录管理系统的创建
        self.glxtLogin = glxt.GLXT()

    def menu(self):
        #登陆系统并返回用户名
        username = self.glxtLogin.menu()
        if username == -1:
            #back返回上一级
            return
        elif username == None:
            #用户名不为空，进入主界面
            return self.menu()
        self.chooseFunction(username)
        return self.menu()

    #选择功能
    def chooseFunction(self,username):
        text=(
            "",
            "*--Welcome to the learning helper--*",
            "*--Please input number to choose function--*",
            "*--1.about jwxt--*",
            "*--2.about email--*",
            "*--3.keep login in SYSU wifi--*",
            "*--4.log out--*",
            ""
            )
        self.printText(text)
        choose = raw_input()
        if choose == '1':
            #登录教务系统，参数为当前用户
            jwxtLogin = jwxt.JWXT(username)
            jwxtLogin.menu()
        elif choose == '2':
            #收取163的邮箱的邮件附件
            text=(
            "",
            "*--To get all mail attachment--*",
            "*--We only support the 163 mail now--*",
            "*--Please check your input carefully or the programme may break down--*",
            ""
            )
            self.printText(text)
            #输入邮箱地址和密码
            mailAddress = raw_input('Please input your mail address.')
            mailPassword = raw_input('Please input your mail password.')
            #下载邮件附件
            getAttachment = mail.MAIL(mailAddress, mailPassword)
            getAttachment.getMailAttachment()
        elif choose == '3':
            #保持登录wifi
            text = (
                "",
                "*--Keep login in SYSU wifi and auto reconnect--*",
                "*--However this function still has many bug, what a pity!--*",
                ""
            )
            self.printText(text)
            #输入netid和密码
            netId = raw_input('Please input your Netid.')
            netIdPassword = raw_input('Please input your password.')
            #保持登录wifi
            keepWifiLogin = KWLI(netId, netIdPassword)
            keepWifiLogin.keepLogin()
        elif choose == '4':
            #注销当前用户
            self.glxtLogin.logout();
            return self.menu()
        else:
            #非法输入
            print 'Your input is not legal.'

    def printText(self,text,sleepTime = 0.1):
        for string1 in text:
            time.sleep(sleepTime)
            print string1.center( 70 )

if __name__ == '__main__':      
    gnym = GNYM()
    gnym.menu()


