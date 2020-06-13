# certquery_nagios

Nagios NRPE plugin, (Can also be used a standalone Python module)

## Requirements:
  1. Qualys Cert View Account Username and Password. 
            Note: Account Setup and access control restrictions are not explained here. More information can be found [here](https://www.qualys.com/documentation/)
  2. Ubuntu 20.04+ with Python 3.8. Tested with 20.4 and Python 3~, it works. Might work with Python 2, but not tested.
  3. NRPE Server and utils installed on Linux source server and reachable from Nagios/iCinga server on port tcp 5666. Tested and works with NRPE v3 and above. Follow along this [link](https://www.binarycomputer.solutions/installing-nrpe-in-ubuntu) and update IP and permissions as per your local environment.

## Installation.
Clone the git under your python3.8 working directory. If using Nagios NRPE, create a symlink:
cd /path/to/working/directoty
ln -s certexpirynotice.py /usr/lib/nagios/plugins/certexpirynotice.py
if using 64 bit NRPE, path may be /usr/lib64/nagios/plugins.

Note, setup of Nagios NRPE client is not covered here. Check for 3 things:
1. In /etc/nagios/nrpe.cfg - In allowed hosts, ensure Nagios server IP is listed. 
2. In netstat ensure port 5666 is listening. (or custom port which you are using for NRPE)
3. NAGIOS user have sudo access, add in ViSUDO.
"nagios          ALL=(ALL) NOPASSWD: /usr/lib/nagios/plugins/certexpirynotice.py"

For moreinformation, refer this [link](https://www.digitalocean.com/community/tutorials/how-to-create-nagios-plugins-with-python-on-centos-6)

## Qualys API:
  Qualys API authentication is performed with Username and Password and all further API interaction need JWT Tokens. The tokens are generally valid for 2-3 hours. The script checks the age of token, if above 2 hours (120 minutes), then performs token refresh. This value is adjustable in the script. 

  To build search queries, refer [this](https://www.qualys.com/docs/qualys-certview-api-user-guide.pdf) documentation. The best way to build query is to login to Qualys, and copy the search string from the dashboard. Ensure to place it within the 'single quotes' in main() function, within query_cert_Exp.py

## NRPE
  certexpirynotice.py is the Nagios plugin, which pulls others Python code which interacts with Qualys cert view. I have created a symlink of this file under /usr/lib/nagios/plugins for the import statements to work. Again, not the best way to do this probablt, pardon my amateur approach.

## How to understand the code. 
  Start with certexpirynotice.py file and follow along the comments.
