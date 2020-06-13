#!/usr/bin/python3.8
from credlib import credential
#format credentials("login_url","username","password","permissions(boolean)")
qualys_prod = credential("https://gateway.qgx.apps.qualys.com/auth", "username", "pass","false")
#Ensure the URL is correct to your region or custom URL.
#permission value is best set to true, again check with your qualys administrator for advanced information.
