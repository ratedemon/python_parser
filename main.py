from parser import OwnParser
import argparse

def main():
    arg_parser = argparse.ArgumentParser(description='Coinmarketcap parser')
    arg_parser.add_argument('-p', help='Specify number of threads to be used', default=20, type=int)
    args = arg_parser.parse_args()

    parser = OwnParser('https://coinmarketcap.com', args.p)
    parser.start()

if __name__ == '__main__':
    main()
