import socket
import re
from classes.Address import Address
from classes.Port import Port
from tabulate import tabulate

class MyNetScan:

    def __init__(self, _chosenIp, _chosenPort):

        self.chosenIp = _chosenIp
        self.chosenPort = _chosenPort

        self.ipPattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        self.portRange = re.compile("([0-9]+)-([0-9]+)")

        self.addressList = []
        self.MINPORT = 0
        self.MAXPORT = 65535


    def checkValid(self):

        # Parse port
        if self.chosenPort.isdigit():
            self.MINPORT = int(self.chosenPort)
            self.MAXPORT = int(self.chosenPort)
        else:
            # Validate the port range
            validRange = self.portRange.search(self.chosenPort.replace("", ""))
            if validRange:
                self.MINPORT = int(validRange.group(1))
                self.MAXPORT = int(validRange.group(2))
            else:
                return False

        # Parse ip
        validIp = self.ipPattern.search(self.chosenIp.replace(" ",""))
        if not validIp:
            return False

        return True



    def run(self):
        # Check if the arguments are valid
        if not self.checkValid():
            print("[!] Bad arguments!")
            exit()

        # Run the ip scanner
        self.scanIp()

        # Show the open ports
        self.showFound()

    def scanIp(self):

        print("Starting scan...\n")

        # Init address
        address = Address(self.chosenIp)

        # Loop trough port range
        for port in range(self.MINPORT, self.MAXPORT + 1):

            # Init socket we are going to use to connect to the ports
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set a timeout for faster result -> inconsistent
            s.settimeout(0.5)

            # Init current port obj and assign scanned port
            curPort = Port()
            curPort.portNum = port

            # Connect to port
            result = s.connect_ex((self.chosenIp, port))
            print(port)
            # Check if port is open
            if result == 0:
                print("open")
                curPort.isOpen = True
                try:
                    # Grab banner
                    curPort.banner = s.recv(1024)
                except TimeoutError as E:
                    curPort.banner = "/"

            else:
                curPort.isOpen = False

            # Add current scanned port to address
            address.ports[port] = curPort

            s.close()
        # Add address to scanned address list
        self.addressList.append(address)


    def showFound(self):

        # Set header for the table
        tableHeaders = ["PORT", "STATUS", "BANNER"]

        for address in self.addressList:

            print(f"------{address.ip}------\n")

            # Create table
            table = tabulate([[p.portNum, "open", p.banner] for k, p in address.ports.items() if p.isOpen],
                             headers=tableHeaders)

            print(table)

        print()