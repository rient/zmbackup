#!/usr/bin/python3

from requests import get,post
from yaml import load
from mailbox import Users, Session
from sys import exit

# Loading the configuration
with open("/etc/zmbackup/zmbackup.yml","r") as fp:
    try:
        config = load(fp)
    except yaml.YAMLError as e:
        print("An error ocurred while trying to load the config files")
        print(e)

# This one is to interact with Zimbra's API
class Account(object):

    session = Session()
    url = "https://{0}:7071/home/{1}/?fmt=tgz"

    def __init__(self,**kwargs):
        try:
            self.db = Users(zm_session_id=kwargs['sessionID'],
                            email=kwargs['email'])
            self.session.add(self.db)
            self.commit()
            self.url = self.url.format(conf['MAILHOST'],kwargs['email'])
        except KeyError as e:
            print("BUG - The following field wasn't informed during the call: ")
            print(e)
            exit(1)

    def downloadMailbox(self,inc=False):
        if inc == True:
            pass
        rst = get(self.url,stream=True,auth=(conf['ADMINUSER'],conf['ADMINPASS']))
        with open(self.db.email + '.tgz','wb') as stream:
            for block in rst.iter_content(1024):
                stream.write(block)

    def uploadMailbox(self):
        pass

    def downloadLdap(self):
        pass

    def uploadLdap(self):
        pass
