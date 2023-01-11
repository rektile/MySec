import socket
import re
from classes.Address import Address
from classes.Port import Port
from tabulate import tabulate

class MyNetScan:

    def __init__(self, _chosenIp, _chosenPort, _verbose):

        self.chosenIp = _chosenIp
        self.chosenPort = _chosenPort
        self.verbose = _verbose

        self.ipPattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        self.portRange = re.compile("([0-9]+)-([0-9]+)")

        self.addressList = []
        self.MINPORT = None
        self.MAXPORT = None
        self.MINPORTALLOWED = 0
        self.MAXPORTALLOWED = 65535

    def validatePort(self):
        if self.chosenPort.isdigit():
            self.MINPORT = self.MAXPORT = int(self.chosenPort)
        else:
            validRange = self.portRange.search(self.chosenPort.replace(" ", ""))
            if validRange:
                self.MINPORT, self.MAXPORT = int(validRange.group(1)), int(validRange.group(2))
            else:
                return False

        if self.MINPORT < self.MINPORTALLOWED or self.MAXPORT > self.MAXPORTALLOWED:
            return False

        return True

    def validateIp(self):
        validIp = self.ipPattern.search(self.chosenIp.replace(" ", ""))
        return validIp

    def checkValid(self):

        # Parse port
        if not self.validatePort():
            return False

        # Parse ip
        if not self.validateIp():
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

        print("[*] Starting scan...\n")

        # Init address
        address = Address(self.chosenIp)

        # Loop trough port range
        for port in range(self.MINPORT, self.MAXPORT + 1):

            if self.verbose:
                print(f"[*] Scanning port {port}")

            # Init socket we are going to use to connect to the ports
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set a timeout for faster result -> inconsistent
            s.settimeout(0.5)

            # Init current port obj and assign scanned port
            curPort = Port()
            curPort.portNum = port

            # Connect to port
            result = s.connect_ex((self.chosenIp, port))

            # Check if port is open
            if result == 0:
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