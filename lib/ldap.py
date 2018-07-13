#!/usr/bin/python3

from json import dumps, loads
from ldap3 import Server, Connection, ALL, MODIFY_DELETE

# Importing the Config Files
from config import config

class LDAPConnection(object):

    # Initialize a connection with the LDAP Server
    def __init__(self,**kwargs):
        self.folder = kwargs['folder']
        self.filename = kwargs['filename']
        server = Server(config['LDAPSERVER'],use_ssl=False)
        self.ldap = Connection(server,kwargs['LDAPADMIN'],kwargs['LDAPPASS'])
        self.ldap.bind()

    # Close the connection with the LDAP Server
    def __del__(self):
        self.ldap.unbind()

    # Save the file inside the disk
    def save(self,sbase,sfilter):
        rst = self.ldap.search(search_base=sbase,search_filter=sfilter)
        if rst:
            with open(self.folder + self.filename,'w') as stream:
                stream.write(json.dumps(rst))
        else:
            return False

    # Load the file to restore a backup
    def upload(self):
        with open(self.folder + self.filename,'w') as stream:
            rst = loads(stream.read())
        return self.ldap.add(self.cn,self.objectClass,rst)

    # Delete a entry before try to restore
    def delete(self):
        return self.ldap.delete(cn)

class Account(LDAPConnection):

    objectClass = []
    cn = ""

    def __init__(self):
        pass
