# MySec
This repo is made for me to make tools which a lot of pentesters use in the real world.
We might use these tools but some of us dont actually know what is going on under the hood.
Here i try to remake some tools i have a better understanding of what's going on.


# Scanners

## MyNetScan
This simple scanner scans a single ip for the specified open ports.

This is not made to be efficient, it is just a POC.  
That's why it doesnt use threading.

### How to use ?

```bash
# Move to MyNetScan directory
cd ./MySec/Scanners/MyNetScan

# Install requirements for script
pip install -r requirements.txt

# Run script with parameters
python3 MyNetScan.py {IP} {PORT}
```

### Arguments
IP: The ip you want to scan e.g. 192.168.0.1  
PORT: The port you want to scan, this can be a single int or a range e.g 80 or 0-1000


## MyArpScan
Scans for devices on network **WIP**

# MITM

## ARP Poisoning
Poison arp cache to redirect traffic to my pc **WIP**
