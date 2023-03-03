import re
import os

def readFile(filename):

    with open(filename) as file:
        lines = file.readlines()

    return lines


def correctData(lines: list[str]) -> list[str]:

    new_lines: list[str] = []
    expressionFlag = re.compile(r'[\s\.]\s\s')

    for line in lines:
        match = re.search(expressionFlag, line)
        if match:
            start_index = match.start()
            end_index = match.end()
            id = line[:3]
            date = line[5:14]
            previous_line = line[:start_index].rstrip()
            new_line = id + "::" + date + "::" + line[end_index:].rstrip() + "::"
            new_line = re.sub(r'\s\s\s', os.linesep, new_line)
            new_lines.append(previous_line)
            new_lines.append(new_line)
        else:
            new_lines.append(line.rstrip())

    return new_lines




# def parseInfo(line: list[str]):

#     pattern = re.compile(
#         r'(?P<id>\d*)::(?P<date>\d{4}-\d{2}-\d{2})::(?P<names>.*)(?=(::::\s?|,|\.))(?P<family_grade>,[^\.]*)?(?:(?=\.Proc))?(?:\.\s?Proc\.)?(?P<process>\d+)?(?:[\.::|::::])')
    
#     data = pattern.search(line).groupdict()
#     print(data['id'])
    
def parseInfo(lines: list[str]):

    data = dict()

    pattern = re.compile(
        r'(?P<id>\d*)::(?P<date>\d{4}-\d{2}-\d{2})::(?P<names>.*)(?=(::::\s?|,|\.))(?P<family_grade>,[^\.]*)?(?:(?=\.Proc))?(?:\.\s?Proc\.)?(?P<process>\d+)?(?:\.::|::::)')
    
    for line in lines:
        match = re.search(pattern, line)
        if match:
            data = match.groupdict()
        else:
            print("fds")


parseInfo(correctData(readFile('processos.txt')))