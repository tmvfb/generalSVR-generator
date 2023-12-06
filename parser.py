#! usr/bin/env/python3
'''
Python script to parse texts from telegram posts.
'''
import json
import re


DATAPATH = 'data/'


def loader(filepath):
    with open(filepath) as file:
        return json.load(file)


def parser(file):
    result = []
    for element in file:  # navigating through list of dicts
        for key, value in element.items():
            if key == 'text' and value:  # getting posts content
                if not isinstance(value, list):
                    result.append(str(value)
                                  .replace('\xa0', ' ')
                                  .replace('\n', ' ')
                                  .replace('  ', ' ')
                                  .strip())
                elif isinstance(value[0], str):
                    result.append(str(value[0])
                                  .replace('\xa0', ' ')
                                  .replace('\n', ' ')
                                  .replace('  ', ' ')
                                  .strip())
    # remove ad posts from dataset
    # because all posts contain the same word
    reg = re.compile(r'^.*[Дд]орогие')
    result = list(filter(reg.search, result))
    return result


def main():
    file = loader(DATAPATH + 'data.json')
    result_string = parser(file["messages"])
    result_string = json.dumps(result_string, ensure_ascii=False)
    with open(DATAPATH + 'parsed_data.json', 'w') as newfile:
        newfile.write(result_string)


if __name__ == '__main__':
    main()
