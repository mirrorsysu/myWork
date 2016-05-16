# -*- coding: UTF-8 -*-
__author__ = 'Hejing'

import jwxt
import glxt

if __name__ == '__main__':      
    glxtLogin = glxt.GLXT()
    glxtLogin.menu()
    username = raw_input('Please input your username:')
    password = raw_input('Please input your password:')
    jwxtLogin = jwxt.JWXT(username, password)
    jwxtLogin.login()