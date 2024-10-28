# C S 378 - Command and Control Project (Donald and Vincent)

Currently implements:
* Remote shell access (However, commands don't persist across different calls)
* Authentification (symmetric key encryption)
* Persistence (cronjob that activates every reboot)

## Set Up

### Configure IP (IMPORTANT)

Edit the IP addresses in the **_config.py_** file to match the IP address of the attacker and target machine. Can also set which port number the attacker machine will use to listen.

### Creating executables

To create the attacker and backdoor executable things, run the make file. One file named 'attacker'
and another file named 'backdoor' should be created.

### Setting Up and Running Backdoor 

#### Installing necessary packages (on week 4)

Run the following commands:

sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*

sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

sudo yum install -y python3

python3 -m pip install pexpect

python3 -m pip install -U pip setuptools

python3 -m pip install cryptography

#### Creating reboot cronjob 

Place the 'backdoor' executable in the /bin directory of the target machine.

Run **_chmod +x backdoor_** to give execute permissions.

Run the command **_sudo crontab -e_**

Scroll to the bottom (after all #) and add the line: **_@reboot python3 /bin/backdoor &_**

Reboot the system (**_sudo reboot_**), cronjob should run every restart. Backdoor should call out
to attacker machine every 10 seconds (can edit this amount of time in **_config.py_**).

### Setting Up and Running Attacker

Place the 'attacker' executable on the attack machine.

Run **_chmod +x attacker_** to give execute permissions.

Run **_./attacker_** in the command line to run the file and wait for the connection to be initiated by the target machine.

Once connection is made, we should be running as the root user and are in root's directory (at least when testing on Kali machine as target)

## Still Need to Work On:

* Evading detection
* Write-up
* Need to fix the prompt format being sent over
* Maybe figure out how to fix remote shell (or maybe ask Dr. Hintz if what we have is okay)
* Detection script (extra credit, but maybe not that hard?)
* Sometimes connection breaks in certain situations, fix these bugs
  * like when running **_cat /bin/ls_** Looks like something is wrong with trying to encode/decode the characters in the file

