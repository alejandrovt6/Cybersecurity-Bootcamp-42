# 👀 Iron_dome 🆘
📝 Description
Iron_dome program is a monitor of folder and files. This program detects any modification that occurs within the selected folder and will write information to var/log/irondome.log.

* It will be developed for Linux.
* The program only execute when launched as root user.
* The program will run in the background as a daemon or service.
* The program will monitor a critical zone in perpetuity. This route must be indicated
as an argument.
* If more than one argument is provided, these will correspond to the file extensions
to be observed. Otherwise, all files will be monitored.
* The program will detect disk read abuse.
* The program will detect intensive use of cryptographic activity.
* The program will detect changes in the entropy of the files.
* The program should never exceed 100 MB of memory in use.

🛠️ Usage
Run the program

```
python iron_dome.py
```

Modify the critical zone: create folders or files, move location, delete files...
Lock irondome.log and check if the reports are written correctly.

💡 Examples
![Logs](/iron_dome/logs.PNG)