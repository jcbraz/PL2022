from prettytable import PrettyTable
import matplotlib.pyplot as plt
plt.style.use('_mpl-gallery')

def parseFile(filename: str):
    content = open(filename, "r")
    headers = content.readline().strip().split(",")
    
    structure = []

    for line in content:
        data = line.strip().split(",")

        row = {}

        for i in range(len(headers)):
            row[headers[i]] = data[i]

        structure.append(row)

    return structure

def sexDistribution(dataStructure: list[object]):

    genders = {'Male': 0, 'Female': 0}
 
    for dataSet in dataStructure:
        if dataSet.get('temDoença', 'Property not found') == '1':
            if dataSet['sexo'] == 'M':
                genders['Male'] += 1
            elif dataSet['sexo'] == 'F':
                genders['Female'] += 1
            else:
                print('Something went wrong')

    return genders


def ageSicknessDistribution(dataStructure):
    ages = []
    for dataSet in dataStructure:
        ages.append(int(dataSet['idade']))

    maxAge = max(ages)

    #  The 0 format specifier means "format the value as an integer and pad it with zeros if necessary to fill at least one character". In this case, it has the effect of setting the initial value of the dictionary to 0, as desired.
    ageIntervals = {f"{i}-{i+4}": 0 for i in range(30,maxAge,4)}

    for age in ages:
        if age < 0:
            break
        for interval in ageIntervals:
            start, end = map(int, interval.split("-"))
            if start <= age <= end:
                ageIntervals[interval] += 1

    # for interval, count in ageIntervals.items():
    #     print(f"{interval}: {count}")

    return ageIntervals


def cholesterolDistribution(dataStructure):
    cholesterolValues = []
    for dataSet in dataStructure:
        cholesterolValues.append(int(dataSet['colesterol']))

    minValue = min(cholesterolValues)
    maxValue = max(cholesterolValues)

    valueIntervals = {f"{i}-{i+10}": 0 for i in range(minValue,maxValue,10)}

    for value in cholesterolValues:
        if value < 0:
            break
        for interval in valueIntervals:
            start, end = map(int, interval.split("-"))
            if start <= value <= end:
                valueIntervals[interval] += 1

    # for interval, count in valueIntervals.items():
    #     print(f"{interval}: {count}")

    return valueIntervals

def makeDistributionTable(dic: dict, subject: str):

    table = PrettyTable(["Interval", subject])

    for interval, count in dic.items():
        table.add_row([interval, count])

    # print(table)
    return table

def makeDistributionGraph(dic: dict, subject: str):

    plt.bar(dic.keys(), dic.values())
    plt.xlabel('Intervals')
    plt.ylabel(subject)
    plt.title(f"Distribution related to {subject}")

    plt.show()


# print(sexDistribution(parseFile("myheart.csv")))
# print(ageSicknessDistribution(parseFile("myheart.csv")))
print(makeDistributionGraph(ageSicknessDistribution(parseFile("myheart.csv")), "Age"))