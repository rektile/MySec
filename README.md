# MySec
The purpose of this repository is to recreate commonly used penetration testing tools in order to gain a deeper understanding of how they work. While these tools are often used by penetration testers, some individuals may not fully understand the underlying mechanics. By remaking these tools, this repository aims to provide a hands-on and in-depth exploration of the tools' functionality and ultimately improve proficiency and effectiveness in their usage.


# Scanners

## MyNetScan
This simple scanner scans a single ip for the specified open ports.

### How to use ?

```bash
# Move to MyNetScan directory
cd ./MySec/Scanners/MyNetScan

# Install requirements for script
pip install -r requirements.txt

# Run script with parameters
python3 MyNetScan.py -i {IP} -p {PORT}
```

### Arguments
-i: The ip you want to scan e.g. 192.168.0.1  
-p: The port you want to scan, this can be a single int or a range e.g 80 or 0-1000


## MyArpScan
Scans for devices on network **WIP**

# MITM

## ARP Poisoning
Poison arp cache to redirect traffic to my pc **WIP**
