# vpn-connector
A python3 script to connect/disconnect vpn using two factor authentication.

Requirement:
    1. LINUX OS
    2. pyotp package is required to run this script
      >>pip3 install pyotp
    3. Config secret, vpn name and password

Extras:
    1. For better visuals, install pyfiglet
      >>pip3 install pyfiglet

Usage:

    1. Install the required packages: pyotp, pyfiglet(Optional)

    2. Edit the vpn configuration section mentioned in the python script
    
    For connecting to a vpn
    python3 vpn_connector.py --connect <vpn_name>

    For disconnecting a vpn
    python3 vpn_connector.py --disconnect <vpn_name>
