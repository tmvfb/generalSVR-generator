#! usr/bin/env/python3
'''
Python script to parse texts from telegram posts.
'''
import json
import re


def loader(filepath):
    with open(filepath) as file:
        return json.load(file)


def parser(file, result=[]):
    if result == []:
        memory = file
        result.append(' ')
    for key, value in file.items():
        if key == 'text' and value:
            if not isinstance(value, list):
                result.append(str(value)
                              .replace('\xa0', ' ')
                              .replace('\n', ' ')
                              .strip())
            elif isinstance(value[0], str):
                result.append(str(value[0])
                              .replace('\xa0', ' ')
                              .replace('\n', ' ')
                              .strip())
        elif isinstance(value, dict):  # initiate tree search
            parser(value, result)
    try:  # execute this at the end of tree search
        if file == memory:
            reg = re.compile(r'^.*[Дд]орогие')  # remove ad posts from dataset
            result = list(filter(reg.search, result))
            return result
    except UnboundLocalError:
        pass


def main(filepath='./data.json'):
    file = loader(filepath)
    result_string = parser(file)
    result_string = json.dumps(result_string, ensure_ascii=False)
    with open('parsed_data.json', 'w') as newfile:
        newfile.write(result_string)


if __name__ == '__main__':
    main()
