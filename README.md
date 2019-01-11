# Steam Account Manager

#### Console client only, for now...
Written with Python 3.7.2

Built to easily switch between multiple steam accounts. 

[python]: https://www.python.org/downloads/
[autoit]: https://www.autoitscript.com/site/autoit/downloads/
[jessicar98]: https://github.com/Jessecar96/SteamDesktopAuthenticator

## Read me

##### Use as a startup program
The script will log-in to the last selected account on execute.  
Use this script as an alternative startup program for Steam.exe

##### Security Issue
This script writes account credentials in plain-text. Encryption will be added in future builds

## Requirements
##### Supported only on Windows, No support for Linux / MacOS
- `Python 3`
- `PyAutoit`


## Installing

##### Install the latest version of [Python 3][python] :

```
https://www.python.org/downloads/
```

##### PyAutoIt is required for Steam Guard Mobile Authenticator :

```
pip install -U https://github.com/jacexh/pyautoit/archive/master.zip
```

##### To install the desktop version of [AutoIt][autoit] :

```
https://www.autoitscript.com/site/autoit/downloads/
```

## Steam Guard Mobile Authenticator
#### This script can automatically generate a mobile auth code
You can optionally add your Steam Guard Mobile Authenticator to the script

This will be prompted during account creation

#### maFile
Import your Account.maFile from your `rooted` Android devices

Alternatively, you can create one with [Jessecar96's SteamDesktopAuthenticator][jessicar98]

#### Shared Secret
I only need a valid `shared_secret` from your Account.maFile
##### Example maFile : 
`I've inserted some random data to this maFile and it does not correspond to any steam user account`
```
{ "shared_secret":"Adra+1Asfd/aadd/AADadA=", "serial_number":"345346346353534535", "revocation_code":"R12121", "uri":"otpauth://totp/Steam:coolstar?secret=LR453KGGGGG44AAAA3DDDD&issuer=Steam", "server_time":1422312312, "account_name":"coolstar", "token_gid":"43243524a22224", "identity_secret":"r35DDAA432/XdddaA324aAdd/U=", "secret_1":"H+DD324aDDDaA+ADD324asaaa=", "status":1,"device_id":"android:43wsad-2dd2-faad-dga3-435s4324fD", "fully_enrolled":true, "Session":{ "SessionID":"2334sf324gfgfg33g2221", "SteamLogin":"711111111111111111%2A%324A6GFG777AAAA55545AAAAAAA111111111111", "SteamLoginSecure":"711111111111111111%2A%4JHUHGGGGGJJJ43345SAAAA111111111DDD", "WebCookie":"654648DDDDDAAAAAA213213DDDD44444FGFFFFFFFFFF", "OAuthToken":"hfgh5456j7h8h98hhhhhhh92222222h2222", "SteamID":711111111111111111 } }
```
##### The only code i need in this case is :
```
Adra+1Asfd/aadd/AADadA=
```
Paste your `shared_secret` in the promt during account creation

## Futute Support
* User Interface
* Encryption



