def readSequence():

    valueRecieved = ""
    returningValue = 0
    readingFlag = True

    while (valueRecieved != "="):
        valueRecieved = input("Insert a value or command:\n")

        if valueRecieved.lower() == 'off':
            readingFlag = False

        elif valueRecieved.lower() == 'on' and readingFlag == False:
            readingFlag = True

        elif valueRecieved.isnumeric() and readingFlag == True:
            returningValue += int(valueRecieved)

        else:
            if valueRecieved != "=":
                print('Invalid input!')

    return returningValue


def main():

    print(readSequence())


main()
