# Password-manager

## Overview
The goal of this project is to build app to manage my passwords of services and websites. 
You can create account only by passing login and/or email. 
Each account contains only one additional field - salt, which is used to encrypt / decrypt passwords. 

The following information about each application is stored in the database:
- Application name
- Application url
- Login
- Registration email
- Encrypted password

For data storage, you enter the master password (it can be different for each app), which, in combination with the user salt, is used to encrypt / decrypt the password.
Then, the only way to view the app password is to enter the master password that was used to register the app data.
You can also generate a customized strong password in this app and edit or delete password details.

## Requirements
* python 3.9
* mongo db
* pyqt5
* cryptography
