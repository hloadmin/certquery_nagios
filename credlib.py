#!/usr/bin/python3.8
#cred mapping class. 
class credential:
    def __init__(self, hostname, username, password, permissions):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.permissions = permissions
