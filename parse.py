#!/usr/bin/env python
import sys
import re
import json
from bs4 import BeautifulSoup


def cleanws(text):
    return re.sub(r'\s+', ' ', text)


def table_rows(table):
    header = None

    for tr in table.find_all('tr'):
        cells = tr.find_all('td')
        assert len(cells)
        first = cells[0]

        if first.strong:
            header = cleanws(first.strong.text)
            cells = cells[1:]
        elif first.has_attr('class') and first['class'] == ['em']:
            header = cleanws(first.text)
            cells = cells[1:]

        yield [header] + [cleanws(td.text) for td in cells]


def merge_rows(rows):
    index = {}

    for row in rows:
        if len(row) == 1:
            pass
        elif len(row) == 2:
            index.setdefault(row[0], []).append(row[1])
        else:
            index.setdefault(row[0], []).append(row[1:])
        #elif len(row) == 3:
        #    index.setdefault(row[0], {})[row[1]] = row[2]
        #elif len(row) == 4:
        #    index.setdefault(row[0], {}).setdefault(row[1], {})[row[2]] = row[3]
        #else:
        #    assert False

    return index


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s infile' % sys.argv[0]
        sys.exit(1)

    with open(sys.argv[1]) as f:
        html = BeautifulSoup(f, 'html.parser')

    index = {}

    for div in html.find_all('div', 'par-div'):
        name = cleanws(div.h3.contents[0])
        #print 'name:', name
        #print merge_rows(table_rows(div.table))
        index[name] = merge_rows(table_rows(div.table))

    json.dump(index, sys.stdout)
