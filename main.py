from parser import Parser

def main():
    parser = Parser('https://coinmarketcap.com')
    parser.start()

if __name__ == '__main__':
    main()
