# -*- coding: UTF-8 -*-
__author__ = 'Hejing'


import requests
from bs4 import BeautifulSoup
import re

class SOJ:
        def __init__(self):
            self.sojUrl = 'http://soj.sysu.edu.cn/'
            self.promblemNum = 0
            self.solutionUrl = ''
            self.problemUrl = ''

        def getSoj(self):
            self.promblemNum = raw_input("Please input the problem number:")
            session = requests.Session()
            self.setUrl()
            self.getProblemContent(session)
            self.getProblemSolution(session)
        
        def setUrl(self):
            self.solutionUrl = "http://soj.sysu.edu.cn/post.php?pid=%d&catalog=solution" % (int(self.promblemNum))
            self.problemUrl = "http://soj.sysu.edu.cn/%d" % (int(self.promblemNum))

        def getProblemContent(self,session):
            response = requests.get(self.problemUrl).content


        def getProblemSolution(self, session):
            response = requests.get(self.solutionUrl).content
            soup = BeautifulSoup(response)
            solutionList = soup.find_all("div","post_body post_content")
            for i in solutionList:
                i = unicode(i.string).replace(u'&nbsp;',u' ').replace(u'&quot;',ur'"').replace(u"&lt;",u"<").replace(u"&gt;",u">")
            
            
if __name__ == '__main__':
    a = SOJ()
    a.getSoj()

