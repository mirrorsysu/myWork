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
        username = self.glxtLogin.menu()
        if username == -1:
            return
        elif username == None:
            return self.menu()
        self.chooseFunction(username)
        return self.menu()

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
             jwxtLogin = jwxt.JWXT(username)
             jwxtLogin.menu()
        elif choose == '2':
            text=(
            "",
            "*--To get all mail attachment--*",
            "*--We only support the 163 mail now--*",
            ""
            )
            self.printText(text)
            mailAddress = raw_input('Please input your mail address.')
            mailPassword = raw_input('Please input your mail password.')
            getAttachment = mail.MAIL(mailAddress, mailPassword)
            getAttachment.getMailAttachment()
        elif choose == '3':
            text = (
                "",
                "*--Keep login in SYSU wifi and auto reconnect--*",
                "*--However this function still has many bug, what a pity!--*",
                ""
            )
            self.printText(text)
            netId = raw_input('Please input your Netid.')
            netIdPassword = raw_input('Please input your password.')
            keepWifiLogin = KWLI(netId, netIdPassword)
            keepWifiLogin.keepLogin()
        elif choose == '4':
            self.glxtLogin.logout();
            return self.menu()
        else:
            print 'Your input is not legal.'

    def printText(self,text,sleepTime = 0.1):
        for string1 in text:
            time.sleep(sleepTime)
            print string1.center( 70 )

if __name__ == '__main__':      
    gnym = GNYM()
    gnym.menu()


