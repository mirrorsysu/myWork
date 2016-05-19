# -*- coding: UTF-8 -*-
__author__ = 'Hejing'


import poplib
import cStringIO
import email
import base64
import os
from email import parser
#pop3 get email
class MAIL:
    def __init__(self,username,password):
        self.mail = poplib.POP3_SSL('pop.163.com')
        self.username = username
        self.password = password

    def getMailAttachment(self):
        self.connect_mail()
        self.getMailContent();

    def connect_mail(self):
        self.mail.user(self.username)
        self.mail.pass_(self.password)

    def getMailContent(self):
        attachmentNum = 0
        mailNumber = len(self.mail.list()[1])
#number of emails
        for i in range(0,mailNumber):
            print 'The ',i,' of ',mailNumber, 'Attahment number :' , attachmentNum
            mailContent = self.mail.retr(i+1)
            mailContent = "\n".join(mailContent[1])
            message = parser.Parser().parsestr(mailContent)
            for part in message.walk():
                filename = part.get_filename()
                if filename:
                #save
                    attachmentNum += 1
                    filename = filename.replace('/','_')
                    f = open(os.getcwd()+"/attachment/mail%d.%s" % (i+1,filename),'wb')
                    f.write(base64.decodestring(part.get_payload()))
                    f.close()

if __name__ == '__main__':
    print os.getcwd()
    a = MAIL("844912709@qq.com","773175hejing")
    a.getMailAttachment()


