#### AutoIP

###### A few days ago I started hosting the apps I develop on my Raspberry PI
###### But, as I have a dynamic IP, the settings of each domain I own should be updated each time the IP changes
###### Is this reason good enough to build a script that does it automatically?
###### Maybe not, but I wanted to do it anyway

The script loads the configurations from the .env file

Multiple configurations can be provided, but each row should have the following structure
```
CONF_#=domain#provider#username#password

e.g
CONF_0=example.com#namecheap#username1#password1
CONF_1=example2.com#godaddy#username2#password2
```
Configuration indexes start at 0
