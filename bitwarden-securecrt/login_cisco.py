# $language = "Python3"
# $interface = "1.0"
from dataclasses import fields
import json
import subprocess
from subprocess import PIPE
from urllib.parse import uses_netloc
st_inf = subprocess.STARTUPINFO()
st_inf.dwFlags = st_inf.dwFlags | subprocess.STARTF_USESHOWWINDOW

tab_name = crt.Window.Caption # get the active tab name
tab_name=tab_name[:-11] # strip the " - SecureCRT" from the tab name
activetab = crt.GetActiveTab() # get the active tab SecureCRT Object

#Start powershell process and get session using Bitwarden CLI
session=subprocess.run(
    ['C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe','Get-Content $env:LOCALAPPDATA\\bitwarden-cli\\session.txt'] , stdout=subprocess.PIPE, startupinfo=st_inf)
session=session.stdout
session=str(session.decode("utf-8"))

#Start powershell process and get username, password and enable using Bitwarden CLI
cmd_username='powershell bw get username ' + tab_name + ' --raw --session ' +  session
cmd_password='powershell bw get password ' + tab_name +' --raw --session ' +  session
cmd_enable='powershell bw get item ' + tab_name + ' --raw --session ' + session
commands = [cmd_username,cmd_password,cmd_enable]
processes = [subprocess.Popen(cmd,stdout=subprocess.PIPE, startupinfo=st_inf) for cmd in commands]

for p in processes: 
    p.wait()
username=processes[0]
username=username.communicate()
username=username[0].decode("utf-8")

password=processes[1]
password=password.communicate()
password=password[0].decode("utf-8")

enable=processes[2]
enable=enable.communicate()
enable=enable[0].decode("utf-8")
enable=json.loads(enable)
if 'fields' in enable.keys():
    enable=enable['fields'][0]['value']
else:
    enable=''

string=activetab.Screen.ReadString('sername:', 1)
string2=activetab.Screen.Get(2, 1, 2, 9)

if "name" in string or "name" in string2 and username !='':
    activetab.Screen.Send(username)
    activetab.Screen.Send('\r')
else:
    activetab.Screen.Send('\r')
    activetab.Screen.WaitForStrings("sername:")
    activetab.Screen.Send(username)
    activetab.Screen.Send('\r')

string3=activetab.Screen.ReadString('ser:', 1)
string4=activetab.Screen.Get(6, 1, 6, 7)
if "ser" in string3 or "ser" in string4:
    activetab.Screen.Send(username)
    activetab.Screen.Send('\r')      


activetab.Screen.Send(password)
activetab.Screen.Send('\r')
activetab.Screen.WaitForStrings(">")

if enable != '':
    activetab.Screen.Send("enable")
    activetab.Screen.Send('\r')
    activetab.Screen.WaitForStrings("assword:")
    activetab.Screen.Send(enable)
    activetab.Screen.Send('\r')