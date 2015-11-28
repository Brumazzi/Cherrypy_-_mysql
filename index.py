#!/usr/bin/env python
# *-* coding:utf-8 *-*

import MySQLdb as mysql
import cherrypy

conn = mysql.connect("127.0.0.1", "root", "daniel21")
conn.select_db("cherrypy")

class Server(object):
    @cherrypy.expose
    def index(self, login=None, passwd=None):
        file = open("form.html","r")
        form = file.read()
        file.close()

        check = None

        if login != None and passwd != None:
            check = self.check_login(login, passwd)

        if(check == False):
            return form.replace("{{err}}", "Usuario ou senha incorretos")

        if(check == None):
            return form.replace("{{err}}", "")

        return "<center><h1>Logado com sucesso!</h1></center>"

    def check_login(self, log, pas):
        c = conn.cursor()
        if "'" in log or "'" in pas:
            return False
        c.execute("select * from users where login='%s' and passwd='%s';" %(log, pas))
        data = c.fetchone()
        if data == None:
            return False
        return data

cherrypy.quickstart(Server())
