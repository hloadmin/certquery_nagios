#!/usr/bin/python3.8
from credlib import credential
#format credentials("login_url","username","password","permissions(boolean)")
qualys_prod = credential("https://gateway.qgx.apps.qualys.com/auth", "username", "password","false")
