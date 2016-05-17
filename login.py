# -*- coding: UTF-8 -*-
__author__ = 'Hejing'

import jwxt
import glxt

class GNYM():
    def __init__(self):
        self.glxtLogin = glxt.GLXT()

    def menu(self):
        username = self.glxtLogin.menu()
        if username == None:
            return self.menu()
        self.chooseFunction(username)

    def chooseFunction(self,username):
        print 'Welcome to the learning helper'
        print 'Please input number to choose function'
        print '1.about jwxt'
        print '2.about email'
        print '3.log out'
        choose = raw_input()
        if choose == '1':
             jwxtLogin = jwxt.JWXT(username)
             jwxtLogin.menu()
        elif choose == '2':
            print 'mail'
        elif choose == '3':
            self.glxtLogin.logout();
            return menu
        else:
            print 'Your input is not legal.'

if __name__ == '__main__':      
    gnym = GNYM()
    gnym.menu()


