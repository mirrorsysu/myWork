# -*- coding: UTF-8 -*-
__author__ = 'Hejing'


import poplib
import cStringIO
import email
import base64
import os
from email import parser

#利用pop3模组下载邮件附件
class MAIL:
    def __init__(self,username,password):
        #163邮箱pop3地址
        self.mail = poplib.POP3_SSL('pop.163.com')
        #邮箱地址以及密码
        self.username = username
        self.password = password

    #连接邮箱并获得邮件内容
    def getMailAttachment(self):
        #连接邮箱
        self.connect_mail()
        #获得邮件内容
        self.getMailContent();

    #连接邮箱
    def connect_mail(self):
        #登录邮箱
        self.mail.user(self.username)
        self.mail.pass_(self.password)

    #获得邮件内容
    def getMailContent(self):
        #已下载附件个数
        attachmentNum = 0
        #邮件数
        mailNumber = len(self.mail.list()[1])
        #遍历所有邮件
        for i in range(0,mailNumber):
            #打印下载信息
            print 'The ',i,' of ',mailNumber, 'Attahment number :' , attachmentNum
            #收取第i封邮件
            mailContent = self.mail.retr(i+1)
            #将两行邮件内容以\n连接
            mailContent = "\n".join(mailContent[1])
            #解析邮件内容
            message = parser.Parser().parsestr(mailContent)
            #遍历邮件内容的所有结点
            for part in message.walk():
                #获得附件名称
                filename = part.get_filename()
                #附件名不为空，即存在附件
                if filename:
                    #下载附件
                    attachmentNum += 1
                    #将不允许出现在文件名中的'/'转化为'_'
                    filename = filename.replace('/','_')
                    f = open(os.getcwd()+"/attachment/mail%d.%s" % (i+1,filename),'wb')
                    f.write(base64.decodestring(part.get_payload()))
                    f.close()



