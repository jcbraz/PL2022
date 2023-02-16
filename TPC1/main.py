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

    ageIntervals = {f"{i}-{i+4}": 0 for i in range(30, maxAge, 4)}

    for dataSet in dataStructure:
        age = int(dataSet['idade'])
        if age < 0:
            break
        for interval in ageIntervals:
            start, end = map(int, interval.split("-"))
            if start <= age <= end and dataSet['temDoença'] == '1':
                ageIntervals[interval] += 1

    return ageIntervals


def cholesterolDistribution(dataStructure):
    cholesterolValues = []
    for dataSet in dataStructure:
        cholesterolValues.append(int(dataSet['colesterol']))

    minValue = min(cholesterolValues)
    maxValue = max(cholesterolValues)

    valueIntervals = {f"{i}-{i+10}": 0 for i in range(minValue, maxValue, 10)}

    for dataSet in dataStructure:
        value = int(dataSet['colesterol'])
        if value < 0:
            break
        for interval in valueIntervals:
            start, end = map(int, interval.split("-"))
            if start <= value <= end and dataSet['temDoença'] == '1':
                valueIntervals[interval] += 1

    return valueIntervals


def makeDistributionTable(dic: dict, subject: str):

    table = PrettyTable([subject, "Disease presence"])

    for interval, count in dic.items():
        table.add_row([interval, count])

    return table


def makeDistributionGraph(dic: dict, subject: str):

    plt.bar(dic.keys(), dic.values())
    plt.xlabel('Intervals')
    plt.ylabel(subject)
    plt.title(f"Distribution related to {subject}")

    plt.show()


def selectDistributions(data, viewModel: int):
    valueSelected = 1
    subject: str
    while (valueSelected != 0):
        valueSelected = int(input(
            "Select the distribution:\n1 - Disease distribution by sex\n2 - Disease distribution by age\n3 - Disease distribution by cholesterol\n"))
        if valueSelected != 0:
            if valueSelected == 1:
                subject = "Sex"
                if viewModel == 1:
                    print(makeDistributionTable(sexDistribution(data),subject))
                    break
                else:
                    print(makeDistributionGraph(sexDistribution(data),subject))
                    break
            elif valueSelected == 2:
                subject = "Age"
                if viewModel == 1:
                    print(makeDistributionTable(ageSicknessDistribution(data),subject))
                    break
                else:
                    print(makeDistributionGraph(ageSicknessDistribution(data),subject))
                    break
            elif valueSelected == 3:
                subject = "Cholesterol"
                if viewModel == 1:
                    print(makeDistributionTable(cholesterolDistribution(data),subject))
                    break
                else:
                    print(makeDistributionGraph(cholesterolDistribution(data),subject))
                    break
            else:
                print("Something went wrong")
                break


def main():
    data = parseFile("myheart.csv")
    tableOrGraph = 0
    while (tableOrGraph != 1 and tableOrGraph != 2):
        tableOrGraph = int(
            input("Choose the mode to visualize the data:\n1 - Table\n2 - Graph\n"))

    selectDistributions(data, tableOrGraph)


main()