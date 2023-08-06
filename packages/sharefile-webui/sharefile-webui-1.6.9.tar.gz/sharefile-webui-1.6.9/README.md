# sharefile-webui

Simple and lightweight responsive web app for sharing files via URL link. Supports drag&drop chunk upload of large files, basic file and directory operations.
Application is based on Python Flask, Flask-Restful and React for simple file 
administration. It can be comfortebly run on Raspberry Pi.

## Usage
```bash
sharefile-webui --help
usage: sharefile-webui [-h] [-o HOST] [-p PORT] [-u ADD_USER] [-r REMOVE_USER] [-l] [-t] [-c] share_directory

Share Files WEB UI v1.5.0

positional arguments:
  share_directory       Directory where shares are stored.

optional arguments:
  -h, --help            show this help message and exit
  -o HOST, --host HOST  APP server host
  -p PORT, --port PORT  APP server port
  -u ADD_USER, --add-user ADD_USER
                        Add admin user in user@password format.
  -r REMOVE_USER, --remove-user REMOVE_USER
                        Remove admin user from users list.
  -l, --list-users      List existing admin users
  -t, --list-tokens     List file tokens into stdout
  -c, --clear-tokens    Clear file tokens database
```
Example:
```bash
sharefile-webui -u username@password
sharefile-webui -p 5555 /tmp
```
This example will share `/tmp` directory on http://localhost:5555
By requesting this URL you will be prompted to fill user and password 
to access admin UI to manage file sharing. For each file of directory you can 
generate secure token. When secure token is generated file could be shared
via URL link like this http://localhost:5555/share/directory-name/file-name?token=12345.

## Instalation
```bash
pip3 install sharefile-webui
```

### systemd configuration
```bash
PORT=5555
SHARE_DIR=/tmp
echo "[Unit]
Description=ShareFileWebUI

[Service]
ExecStart=/bin/bash -c \"/usr/local/bin/sharefile-webui -p ${PORT} ${SHARE_DIR}  >> /var/log/sharefile-webui.log 2>&1 &\"
ExecStop=killall sharefile-webui
ExecRestart=/bin/bash -c \"killall sharefile-webui && /usr/local/bin/sharefile-webui  -p ${PORT} ${SHARE_DIR} >> /var/log/sharefile-webui.log 2>&1 &\"
ExecStatus=ps -ax | grep sharefile-webui
Type=forking

[Install]
WantedBy=multi-user.target
" > /lib/systemd/system/sharefile-webui.service
systemctl enable sharefile-webui.service
```
after that is possible to use
```bash
systemctl start sharefile-webui.service
```

### Build it by your own
#### JS
Build JS production version is not nessesry, because it is already buid in `sharefile_webui/static/js` directory.
But if you want to change something in UI, lets do it by running:
```bash
sudo apt update
sudo apt install nodejs npm
cd sharefile_webui_js
npm run build
```
or for comfortable local development
```bash
npm run watch
```
with auto build feature if any file is changed.
### Py
```bash
cd sharefile_webui
python3 setup.py build
```
or local installation
```bash
cd sharefile_webui
python3 setup.py install
```

## Screenshot
![sharefile-webui screenshot](https://gitlab.com/alda78/sharefile-webui/-/raw/master/sharefile-webui.png)
