#!/usr/bin/python3

from ldap3 import Server, Connection, ALL, MODIFY_DELETE

# Importing the Config Files
from config import config

class LDAPConnection(object):

    # Initialize a connection with the LDAP Server
    def __init__(self):
        server = Server(environ['SERVER_URL'],use_ssl=False)
        self.ldap = Connection(server,environ['USERNAME'],environ['PASSWORD'])
        self.ldap.bind()

    # Close the connection with the LDAP Server
    def __del__(self):
        self.ldap.unbind()
