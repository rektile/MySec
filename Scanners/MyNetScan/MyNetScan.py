from classes.MyNetScan import MyNetScan
import argparse


parser = argparse.ArgumentParser(description='Scans network for open ports')

parser.add_argument("-i",
                    "--ip",
                    help="The ip you want to scan.",
                    nargs="?",
                    required=True)

parser.add_argument("-p",
                    "--port",
                    help="Port or range of ports you want to scan e.g. 0-1000.",
                    nargs="?",
                    required=True)


parser.add_argument("-w",
                    "--workers",
                    help="The the amount of concurrent workers.",
                    type=int)

parser.add_argument("-v",
                    "--verbose",
                    help="Show verbose output",
                    action='store_true')


args = parser.parse_args()

scanner = MyNetScan(args.ip, args.port, args.verbose, args.workers)

scanner.run()





