import pennyBoardWheels
import gmail
from datetime import datetime


def main():
    in_stock = pennyBoardWheels.scanTheSite()

    if len(in_stock) > 0:
        gmail.sendTheEmail(in_stock)
    else:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), ": Nothing in stock...")


if __name__ == "__main__":
    main()
