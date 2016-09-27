#!/usr/bin/env python
import sys
import json


def getid(name):
    return name.replace(' ', '_')


short_resource = {
    'Science': 'Sc',
    'Compendium': 'Com',
    'Blueprint': 'Bl',
    'Manuscript': 'Man',
    'Time Crystal': 'TC'
}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s infile' % sys.argv[0]
        sys.exit(1)

    with open(sys.argv[1]) as f:
        index = json.load(f)

    print 'digraph tech {'
    print 'node [shape=record]'

    for tech, data in index.iteritems():
        costs = [v + ' ' + short_resource.get(k, k) for k, v in data['Cost']]
        print '%s [label="{%s|{%s}}"]' % (getid(tech), tech, '|'.join(costs))

    for tech, data in index.iteritems():
        for unlock in data.get('Unlocks', []):
            print getid(tech), '->', getid(unlock)

    print '}'
