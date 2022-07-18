from classes.MyNetScan import MyNetScan
import argparse


parser = argparse.ArgumentParser(description='Scans network for open ports')

parser.add_argument("IP", help='The ip you want to scan')
parser.add_argument("PORT", help='Port or range of ports you want to scan e.g. 0-1000')


args = parser.parse_args()

scanner = MyNetScan(args.IP, args.PORT)

scanner.run()





