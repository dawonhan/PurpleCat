![Interface](/src/PurpleCat.png)

# Prerequisite
## T1215 Test:
To run the kernel test, must have Linux-headers installed to compile the kernel module.

### Instructions:
1. Run: `apt update -y && apt upgrade -y && apt dist-upgrade `
*Might take awhile to finish depending on your system.
2. reboot
3. Run: `apt-get install build-essential linux-headers-``uname -r``

# Installation
`cd /opt`

`git clone https://github.com/roninone/PurpleCat`

## Create a symbolic link
`cd /bin`

`ln -s /opt/PurpleCat/purplecat.py PurpleCat`
