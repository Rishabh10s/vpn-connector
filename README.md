# vpn-connector
A python3 script to connect/disconnect vpn using two factor authentication.

Requirement:
    * LINUX OS
    * pyotp package is required to run this script
      >>pip3 install pyotp
    * Config secret, vpn name and password

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

=================================================================================
    ____  _      __          __    __    _____ __                              
   / __ \(_)____/ /_  ____ _/ /_  / /_  / ___// /_  ____ __________ ___  ____ _
  / /_/ / / ___/ __ \/ __ `/ __ \/ __ \ \__ \/ __ \/ __ `/ ___/ __ `__ \/ __ `/
 / _, _/ (__  ) / / / /_/ / /_/ / / / /___/ / / / / /_/ / /  / / / / / / /_/ / 
/_/ |_/_/____/_/ /_/\__,_/_.___/_/ /_//____/_/ /_/\__,_/_/  /_/ /_/ /_/\__,_/  

=================================================================================


