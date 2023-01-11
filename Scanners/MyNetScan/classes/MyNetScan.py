import socket
import re
from classes.Address import Address
from classes.Port import Port
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor

class MyNetScan:

    def __init__(self):

        self.chosenIp = None
        self.chosenPort = None
        self.verbose = None
        self.maxWorkers = None

        self.ipPattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        self.portRange = re.compile("([0-9]+)-([0-9]+)")

        self.addressList = []
        self.MINPORT = None
        self.MAXPORT = None
        self.MINPORTALLOWED = 0
        self.MAXPORTALLOWED = 65535

    def argumentParser(self, args):
        self.chosenIp = args.ip
        self.verbose = args.verbose
        self.maxWorkers = args.workers
        self.chosenPort = args.port


    def validatePort(self):

        if not self.chosenPort:
            self.MINPORT = self.MINPORTALLOWED
            self.MAXPORT = self.MAXPORTALLOWED
        elif self.chosenPort.isdigit():
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

        with ThreadPoolExecutor(max_workers=None) as executor:
            # Create a list to hold the future results
            futures = []

            # Loop through port range
            for port in range(self.MINPORT, self.MAXPORT + 1):

                # Submit the scanPort method as a task to the executor
                future = executor.submit(self.scanPort, port)
                futures.append(future)

            # Wait for all futures to complete and retrieve the results
            for future in futures:
                curPort = future.result()

                # Add current scanned port to address
                address.ports[curPort.portNum] = curPort

        # Add address to scanned address list
        self.addressList.append(address)

    def scanPort(self, port):

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

        s.close()

        return curPort
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