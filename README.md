# Bitwarden-SecureCRT Integration

#### DISCLAIMER 
I am not a professional programmer, but I am a network engineer who is approaching the world of automation, I am aware that the code is not perfect and I am open to any advice. I hope somebody will find this useful.

#### Introduction

SecureCRT is an excellent product and is one of the most used tools by a network engineer, but currently does not have a plug-in that meets my need to interface it to an external password manager, avoiding saving credentials within sessions.

The integration works thanks to a mixture of Python and Powershell combined with the official Bitwarden command line and has been designed for connection to Cisco devices but is easily adaptable for other vendors.

#### Operation

When you launch a session on an SSH or Telnet device, SecureCRT launches a python script which in turn launches PowerShell subprocesses that interact with the Bitwarden CLI extracting username and password and enable password. These parameters are automatically sent to the active SecureCRT tab and then complete the login.

<p align="center">
  <img width="800" src="https://user-images.githubusercontent.com/64638740/158028909-02026c8d-7f10-4309-b1d4-217b35726b2a.png">
</p>

## Prerequisites

1. SecureCRT version 9.0 and Python 3.8 installed. Beginning in version 9.0, SecureCRT on the Windows platform supports the use of a third party python v3.8 scripting engine. More information here: https://forums.vandyke.com/showthread.php?t=14295
2. Bitwarden CLI Installed. Download here https://bitwarden.com/help/cli/
   **NOTE:** On my PC I just copied the executable on the bitwarden-securecrt folder but as you can see from the official documentation there are several ways to install it.

## SETUP

**WINDOWS**

```
1. Go to %LOCALAPPDATA%
2. Paste the bitwarden-securecrt folder
3. Add %LOCALAPPDATA%\bitwarden-securecrt\ to the Windows Path variable
```
[(How to set the path and environment variables in Windows)](https://www.computerhope.com/issues/ch000549.htm)

**SecureCrt**

Add Bitwarden session (Powershell local shell)

```
- New Session → Local Shell → C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
  - In "Logon Action" section tick the Automate Logon box and add new string:
  - Expect:>
  - Send: Invoke-Expression "${env:LOCALAPPDATA}\\bitwarden-securecrt\\bwlogin.ps1"
```
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/64638740/158027329-129456ec-b720-48e0-86dd-b34acebec7f6.png">
</p>


Add the SSH Session (example Cisco Router)

```
LOGON ACTIONS
- Paste this in the Logon Script field: %LOCALAPPDATA%\bitwarden-securecrt\login_cisco.py
- Tick Display logon prompts in terminal window
```
<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/64638740/158029066-ee8519a8-504f-464f-aba3-09d021271690.png">
</p>

```
In the SSH2 section make sure that you set the Keyboard Interactive authentication first.
```

<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/64638740/158029132-6020eed4-2d95-4400-aaf4-8c1bee9e1bcd.png">
</p>

**Bitwarden**
```
1. Create the item TEST-LOGIN-DO-NOT-DELETE and set the username to TEST password empty. The bwlogin.ps1 use this to test the SESSION KEY
2. Create the item with the same name as the SSH session previously created on SecureCRT
```
<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/64638740/158029256-fbb191e2-e9a2-49cb-8589-2a8f9240a7e0.png">
</p>
