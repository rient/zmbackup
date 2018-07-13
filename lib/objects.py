#!/usr/bin/python3

from requests import get,post
from sys import exit

# Importing the User Database
from mailbox import Users

# Importing the Connection with LDAP
from ldap import Account

# Importing the Config Files
from config import config

# This one is to interact with Zimbra's API
class Account(object):
    url = "https://{0}:7071/home/{1}/?fmt=tgz"

    def __init__(self,**kwargs):
        try:
            self.folder = kwargs['folder']
            self.db = Users.find(kwargs) or Users.create(kwargs)
            self.url = self.url.format(conf['MAILHOST'],kwargs['email'])
        except KeyError as e:
            print("BUG - The following field wasn't informed during the call: ")
            print(e)
            exit(1)

    def downloadMailbox(self,inc=False):
        if inc == True:
            pass
        rst = get(self.url,stream=True,auth=(conf['ADMINUSER'],conf['ADMINPASS']))
        if rst.status_code >= 200 and rst.status_code < 300:
            with open(self.folder + self.db.email + '.tgz','wb') as stream:
                for block in rst.iter_content(1024):
                    stream.write(block)
            return True
        else:
            return False

    def uploadMailbox(self):
        with open(self.folder + self.db.email + '.tgz','rb') as stream:
            rst = requests.post(self.url,files={self.db.email + '.tgz':stream})
        if rst.status_code >= 200 and rst.status_code < 300:
            return True
        else:
            return False

    def downloadLdap(self):
        pass

    def uploadLdap(self):
        pass
