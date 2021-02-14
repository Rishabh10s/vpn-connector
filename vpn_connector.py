"""
A python script to connect/disconnect vpn using two factor authentication.

Requirement:
    * LINUX OS
    * pyotp package is required to run this script
      >>pip3 install pyotp
    * Config secret, vpn names and password

Extras:
    * For better visuals, install pyfiglet
      >>pip3 install pyfiglet

Usage:

    1. Install the required packages: pyotp, pyfiglet(Optional)

    2. Edit the vpn configuration mentioned below

    For connecting to a vpn
    python3 vpn_connector.py --connect <vpn_name>

    For disconnecting a vpn
    python3 vpn_connector.py --disconnect <vpn_name>
"""

import pyotp
import subprocess
import os
import argparse
import sys

####### CHANGE THESE VALUES #######

# DO NOT DELETE/COMMENT VPN SECRETS OR VPN NAMES. IF NOT IN USE, KEEP THEM UNCHANGED. 

# Add base32 secrets.
VPN_SECRET = 'KZIE4ICJKMQE4T2UEBBU6TSGJFDVKUSFIQ======'

# Pass for vpn. Add your password here
PASSWORD = 'BCDEDASD'

# change these names according to the vpn names configured on your system.
VPN_NAME = 'NOT CONFIGURED'
###################################


# Initiate the parser
parser = argparse.ArgumentParser()

parser.add_argument("--connect", "-c", help="Connect to vpn. A vpn name is required")
parser.add_argument("--disconnect", "-d", help="Disconnect vpn. A vpn name is required")

class VPN():
    def __init__(self, vpn_name, secret, password):
        self.vpn_name = vpn_name
        self.secret = secret
        self.password = password
        self.pass_file_path = "/var/tmp/{}_pass".format(vpn_name)
    
    def generate_otp(self):
        '''
        It generates totp just like google authenticator
        '''
        totp = pyotp.TOTP(self.secret)
        return totp.now()

    def save_pass(self):
        '''
        This function creates a file and adds a readable password for nmcli
        '''
        if not self.password:
            sys.exit('Password not provided')
        try:
            otp = self.generate_otp()
        except:
            sys.exit('Unable to generate otp. Please check your secret string.')
        new_pass = self.password + otp
        pass_format = "vpn.secrets.password:{}\n"
        try:
            with open(self.pass_file_path, "w") as fp:
                fp.write(pass_format.format(new_pass))
        except Exception as ex:
            sys.exit("Failed to create password: {}".format(ex))

    def print_message(self, msg):
        '''
        This is for displaying a good message.. :)
        '''
        try:
            import pyfiglet
            print(pyfiglet.figlet_format(msg, font="slant"))
        except:
            print(msg)
    
    def is_active(self):
        '''
        This function checks the status of vpn using nmcli.
        Returns True if vpn is currently active
        '''
        try:
            status = subprocess.check_output(['nmcli', '-f', 'GENERAL.STATE', 'con', 'show', self.vpn_name]).decode('utf-8')
            status = status.rstrip()
            is_active = status.split(' ')[-1] 
            if is_active == "activated":
                return True
        except:
            sys.exit("Failed to check VPN status")
        return False
        
    def connect(self):
        '''
        This function lets us connect to the vpn using nmcli with password specified in a file.
        '''
        # check if the password file exists
        if not os.path.isfile(self.pass_file_path):
            sys.exit("Failed to connect to the VPN. Password file not found!")

        # check if vpn is already active
        if self.is_active():
            sys.exit("Already connected to {}".format(self.vpn_name))
            
        try:
            print("Connecting to {}...".format(self.vpn_name))
            subprocess.check_output(['nmcli', 'con', 'up', 'id', self.vpn_name, 'passwd-file', self.pass_file_path])
        except:
            sys.exit("Failed to connect to the VPN")
        self.print_message("Connected to {}".format(self.vpn_name))
    
    def disconnect(self):
        '''
        Disconnect VPN.
        '''
        # check if vpn is already disconnected
        if not self.is_active():
            sys.exit("Already disconnected from {}".format(self.vpn_name))
        
        try:
            subprocess.check_output(['nmcli', 'con', 'down', 'id', self.vpn_name])
        except:
            sys.exit("An error occurred while disconnecting from {}".format(self.vpn_name))
        self.print_message("Disconnected ! !")
        
args = parser.parse_args()

if args.connect:
    # Connect to a vpn
    try:
        if args.connect == VPN_NAME:
            v = VPN(VPN_NAME, VPN_SECRET, PASSWORD)
        else:
            sys.exit("Please provide a valid vpn name: {}".format(VPN_NAME))
    except Exception as ex:
        sys.exit("VPN configuration is invalid!")
    v.save_pass()
    v.connect()
elif args.disconnect:
    # disconnect vpn.
    try:
        if args.disconnect == VPN_NAME:
            v = VPN(VPN_NAME, VPN_SECRET, PASSWORD)
        else:
            sys.exit("Please provide a valid vpn name: {}".format(VPN_NAME))
    except Exception as ex:
        sys.exit("VPN configuration is invalid!")
    v.disconnect()
else:
    parser.print_help()
